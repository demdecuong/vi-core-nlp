import torch
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler

from transformers import AdamW, get_linear_schedule_with_warmup

import os
from tqdm import trange

from model import Model

from utils import get_mask, get_useful_ones
from metrics import batch_computeF1

class Trainer(object):
    def __init__(self, args, model, train_data, dev_data, test_data) -> None:
        super().__init__()

        self.args = args
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        if not os.path.exists(args.save_folder):  os.mkdir(args.save_folder)

        self.model = model
        self.model.to(device=self.device)

        self.train_data = train_data
        self.dev_data = dev_data
        self.test_data = test_data

    def train(self):
        train_sampler = RandomSampler(self.train_data)
        train_loader = DataLoader(self.train_data, batch_size=self.args.batch_size, sampler=train_sampler)

        total_steps = len(train_loader) * self.args.num_epochs

        param_optimizer = list(self.model.named_parameters())
        no_decay = ['bias', 'LayerNorm.bias', 'LayerNorm.weight']
        optimizer_grouped_parameters = [
            {'params': [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)],
             'weight_decay_rate': self.args.weight_decay},
            {'params': [p for n, p in param_optimizer if any(nd in n for nd in no_decay)],
             'weight_decay_rate': 0.0}
        ]
        optimizer = AdamW(
            optimizer_grouped_parameters,
            lr=self.args.learning_rate,
            eps=self.args.adam_epsilon
        )
        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=self.args.warmup_steps,
            num_training_steps=total_steps
        )
        loss_func = torch.nn.CrossEntropyLoss(reduction='sum')
        train_loss = 0
        self.model.train()
        for _, batch in enumerate(train_loader):
            # batch = tuple(t.to(self.device) for t in batch)
            input_ids = batch[0].to(self.device)
            attention_mask = batch[1].to(self.device)
            first_subword = batch[2].to(self.device)

            seq_len = batch[3] # B x 1 e.g tensor([[22], [23], .. ])
            
            char_ids = batch[4].to(self.device)

            if not self.args.use_pos and not self.args.use_fasttext:
                pos_ids = None
                fasttext_embs = None
            elif not self.args.use_pos and self.args.use_fasttext:
                pos_ids = None
                fasttext_embs = batch[5].to(self.device)
            elif self.args.use_pos and not self.args.use_fasttext:
                pos_ids = batch[5].to(self.device)
                fasttext_embs = None
            else:
                pos_ids = batch[5].to(self.device)
                fasttext_embs = batch[6].to(self.device)

            inputs = {
                'input_ids': input_ids,
                'attention_mask': attention_mask,
                'first_subword': first_subword,
                'char_ids': char_ids,
                'pos_ids': pos_ids,
                'fasttext_embs': fasttext_embs
            }

            id_sample = batch[-2]
            label = batch[-1].to(self.device)

            # self.model.zero_grad()
            output = self.model(**inputs)
            # print(output.shape)
            optimizer.zero_grad()

            mask = get_mask(max_seq_len=self.args.max_seq_len, seq_len=seq_len)
            mask = mask.to(self.device)

            tmp_out, tmp_label = get_useful_ones(output, label, mask)

            loss = loss_func(tmp_out, tmp_label)

            loss.backward()
            optimizer.step()
            train_loss += loss.item()

            torch.nn.utils.clip_grad_norm_(parameters=self.model.parameters(),
                                            max_norm=self.args.max_grad_norm)
            scheduler.step()
        print('train loss:', train_loss/len(train_loader))

    def eval(self, mode, f1_pre):
        if mode == 'dev':
            dataset = self.dev_data
        elif mode == 'test':
            dataset = self.test_data
        else:
            raise Exception("Only dev and test dataset available")
        
        eval_sampler = SequentialSampler(dataset)
        eval_loader = DataLoader(dataset, batch_size=self.args.batch_size, sampler=eval_sampler)
        
        self.model.eval()
        loss_func = torch.nn.CrossEntropyLoss(reduction='sum')
        eval_loss = 0
        labels, outputs, seq_lens = [], [], []
        for batch in eval_loader:
            input_ids = batch[0].to(self.device)
            attention_mask = batch[1].to(self.device)
            first_subword = batch[2].to(self.device)

            seq_len = batch[3] # B x 1 e.g tensor([[22], [23], .. ])
            
            char_ids = batch[4].to(self.device)
            if not self.args.use_pos and not self.args.use_fasttext:
                pos_ids = None
                fasttext_embs = None
            elif not self.args.use_pos and self.args.use_fasttext:
                pos_ids = None
                fasttext_embs = batch[5].to(self.device)
            elif self.args.use_pos and not self.args.use_fasttext:
                pos_ids = batch[5].to(self.device)
                fasttext_embs = None
            else:
                pos_ids = batch[5].to(self.device)
                fasttext_embs = batch[6].to(self.device)

            inputs = {
                'input_ids': input_ids,
                'attention_mask': attention_mask,
                'first_subword': first_subword,
                'char_ids': char_ids,
                'pos_ids': pos_ids,
                'fasttext_embs': fasttext_embs
            }

            id_sample = batch[-2]
            label = batch[-1].to(self.device)

            with torch.no_grad():
                output = self.model(**inputs)
            seq_lens.append(seq_len)
            mask = get_mask(max_seq_len=self.args.max_seq_len, seq_len=seq_len)
            mask = mask.to(self.device)

            tmp_out, tmp_label = get_useful_ones(output, label, mask)
            labels.append(label)
            outputs.append(output)
            loss = loss_func(tmp_out, tmp_label)
            eval_loss += loss.item()
        labels = torch.cat(labels, dim=0)
        outputs = torch.cat(outputs, dim=0)
        seq_lens = torch.cat(seq_lens, dim=0)
        f1_score, precision, recall = batch_computeF1(labels, outputs, seq_lens)
        result = {
            '{} loss'.format(mode): eval_loss / len(eval_loader),
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score
        }
        print(result)
        if f1_score > f1_pre:
            return f1_score
        else:
            return f1_pre
    
    def save_model(self, f1):
        checkpoint = {'model': self.model,
                      'state_dict': self.model.state_dict(),
                      }
        path = os.path.join(self.args.save_folder,f'checkpoint_{f1}.pth')
        torch.save(checkpoint, path)
