import json
import re
import torch

from torch import nn
from transformers import AutoTokenizer

from vma_nlu.ner.pername_deeplearning.utils import load_model, initializeFolder, download_model
from vma_nlu.ner.pername_deeplearning.config import Config
from vma_nlu.ner.pername_deeplearning.model.model import Model
# from utils import load_model
# from config import Config

if torch.cuda.is_available():
    torch.cuda.empty_cache()
class Inference(object):
    def __init__(self) -> None:
        super().__init__()

        args = Config()

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self.tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path)

        self.model = Model(args)
        checkpoint, label_set_path, char_vocab_path = download_model()

        print("Loading model .....")
        self.model.load_state_dict(torch.load(checkpoint, map_location=torch.device('cpu')))
        # self.model = load_model(args.checkpoint)

        self.model.to(device=self.device)
        self.model.eval()
        

        self.max_seq_len = args.max_seq_len
        self.max_char_len = args.max_char_len

        with open(label_set_path, 'r', encoding='utf-8') as f:
            self.label_set = f.read().splitlines()
        self.label_set = {i: w for i, w in enumerate(self.label_set)}

        with open(char_vocab_path, 'r', encoding='utf-8') as f:
            self.char_vocab = json.load(f)

        self.softmax = nn.Softmax(dim=2)


    def inference(self, text):
        input_ids, attention_mask, first_subword, char_ids, seq_len = self.preprocessing(text)
        input_ids = input_ids.unsqueeze(0)
        input_ids = input_ids.to(self.device)
        attention_mask = attention_mask.unsqueeze(0)
        attention_mask = attention_mask.to(self.device)
        first_subword = first_subword.unsqueeze(0)
        first_subword = first_subword.to(self.device)
        char_ids = char_ids.unsqueeze(0)
        char_ids = char_ids.to(self.device)
        seq_len = seq_len.unsqueeze(0)
        inputs = {
                'input_ids': input_ids,
                'attention_mask': attention_mask,
                'first_subword': first_subword,
                'char_ids': char_ids,
                'pos_ids': None,
                'fasttext_embs': None
            }
        with torch.no_grad():
            output = self.model(**inputs)
        result = []
        for i in range(len(output)):
            pred = output[i]
            true_len = seq_len[i].item()
            pred = pred[:true_len, :true_len]
            pred = self.prop(pred)
            _, cate_pred = pred.max(dim=-1)
            pred_entity = self.get_entity(cate_pred, pred)
            result.append(pred_entity)
        result = self.output_format(text, result)
        result = self.revised_output(result, text)
        
        return result

    def preprocessing(self, text):
        # segmentation word using u
        sentence = text.split(' ')
        char_seq = []
        for word in sentence:
            character = self.get_character(word, self.max_char_len)
            char_seq.append(character)
        seq_len = len(sentence)
        seq_len = torch.tensor([seq_len])
        input_ids, attention_mask, firstSWindices = self.preprocess(self.tokenizer, sentence, self.max_seq_len)
        char_ids = self.char2id(char_seq=char_seq, max_seq_len=self.max_seq_len)
        return input_ids, attention_mask, firstSWindices, char_ids, seq_len

    def get_character(self, word, max_char_len):
        word_seq = []
        for i in range(max_char_len): #20
            try:
                char = word[i]
            except:
                char = 'PAD'
            word_seq.append(char)
        return word_seq

    def preprocess(self, tokenizer, sentence, max_seq_len, mask_padding_with_zero=True): # sentence_embedding

        input_ids = [tokenizer.cls_token_id]
        firstSWindices = [len(input_ids)]

        for w in sentence:
            word_token = tokenizer.encode(w)
            input_ids += word_token[1: (len(word_token) - 1)]
            firstSWindices.append(len(input_ids))

        firstSWindices = firstSWindices[: (len(firstSWindices) - 1)]
        input_ids.append(tokenizer.sep_token_id)

        attention_mask = [1 if mask_padding_with_zero else 0] * len(input_ids)

        if len(input_ids) > max_seq_len:
            input_ids = input_ids[:max_seq_len]
            attention_mask = attention_mask[:max_seq_len]
            firstSWindices = firstSWindices[:max_seq_len]
        else:
            attention_mask = attention_mask + [0 if mask_padding_with_zero else 1] * (max_seq_len - len(input_ids))
            input_ids = input_ids + [tokenizer.pad_token_id] * (max_seq_len - len(input_ids))
            firstSWindices = firstSWindices + [0]*(max_seq_len - len(firstSWindices))

        return torch.tensor(input_ids), torch.tensor(attention_mask), torch.tensor(firstSWindices)

    def char2id(self, char_seq, max_seq_len): # char - embedding
        char_ids = []
        for word in char_seq:
            word_char_ids = []
            for char in word:
                if char not in self.char_vocab:
                    word_char_ids.append(self.char_vocab.get("UNK"))
                else:
                    word_char_ids.append(self.char_vocab.get(char))
            char_ids.append(word_char_ids)
        if len(char_ids) < max_seq_len:
            char_ids += [[self.char_vocab.get("PAD")]*self.max_char_len]*(max_seq_len - len(char_ids))
        else:
            char_ids = char_ids[:max_seq_len]
        return torch.tensor(char_ids)

    def get_entity(self, input_tensor, pred):
        entity = []
        for i in range(len(input_tensor)):
            for j in range(i,len(input_tensor)):
                if input_tensor[i][j] > 0:
                    tmp = [i, j, self.label_set[int(input_tensor[i][j])], float(pred[i][j][int(input_tensor[i][j])])]
                    entity.append(tmp)
        return entity
    def prop(self, pred):
        return self.softmax(pred)
    def output_format(self, text, output):
        if not output[0]:
            return {
                'entities': []
            }
        else:
            tmp = []
            tokens = text.split()
            output = output[0]
            for span in output:
                start = len(" ".join(tokens[:span[0]]))
                if start != 0:
                    start += 1
                tmp.append({
                    'start': start,
                    'end': len(" ".join(tokens[:span[1]+1])),
                    'entity': 'person_name',
                    'value': " ".join(tokens[span[0]: span[1]+1]),
                    'confidence': span[3] #
                })
            return {
                'entities': tmp
            }
               
    def revised_output(self, result, text):
        result = result['entities']
        if not result:
            return {
                'entities': []
            }
        else:
            revised = []
            for span in result:
                value = span['value']
                start = span['start']
                end = span['end']
                confidence = span['confidence']
                entity = span['entity']
                tmp = re.search('((bs\s+)|(BS\s+)|(Bs\s+)|(bS\s+))', value)
                if tmp:
                    value = value[tmp.span()[1]:]
                    start = start + tmp.span()[1]
                tmp = re.search('^((sỹ)|(Sỹ)|(SỸ)|(sỸ)|(sy)|(Sy)|(sY)|(SY))\s+', value)
                if tmp:
                    tmp_2 = re.search('((bác)|(Bác)|(bÁc)|(báC)|(BÁc)|(BáC)|(bÁC)|(BÁC)|(bac)|(Bac)|(bAc)|(baC)|(BAc)|(BaC)|(bAC)|(BAC))$', text[:start])
                    if tmp_2:
                        value = value[tmp.span()[1]:]
                        start = start + tmp.span()[1]
                revised.append({
                    'start': start,
                    'end': end,
                    'entity': entity,
                    'value': value,
                    'confidence': confidence
                })
        return {
            'entities': revised
        }

initializeFolder()