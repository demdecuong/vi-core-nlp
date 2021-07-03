from os import path
from config import Config

from transformers import AutoTokenizer

from dataset import MyDataSet
from trainer import Trainer
from model import Model
from utils import load_model

import fasttext

import json

def main(args):
    tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path)
    if args.use_fasttext:
        fasttext_model = fasttext.load_model(args.fasttext_path)
    else:
        fasttext_model = None
    
    if args.use_pretrained:
        print(f'Use pretrained model from checkpoint {args.checkpoint}')
        model = load_model(args.checkpoint)
        print(f'Model is loaded weights from checkpoint')
    else:
        print(f'Initialize Name Entity Recognition as Dependence Parsing .  ..  ...')
        model = Model(args)

    dev_data = MyDataSet(path=args.dev_data, 
                        args=args, 
                        tokenizer=tokenizer, 
                        fasttext_model=fasttext_model)
    test_data = MyDataSet(path=args.test_data, 
                        args=args, 
                        tokenizer=tokenizer, 
                        fasttext_model=fasttext_model)
    f1_pre = 0
    for i in range(1, args.iteration + 1):
        print(f'Training model on iteration {i} ...')
        train_data = MyDataSet(path=args.train_data, 
                        args=args, 
                        tokenizer=tokenizer, 
                        fasttext_model=fasttext_model)
        for e in range(1, args.num_epochs + 1):
            print(f'Training model on epoch {e} of iteration {i}')
            trainer = Trainer(args=args,
                            model=model,
                            train_data=train_data,
                            dev_data=dev_data,
                            test_data=test_data)
            if args.do_train:
                trainer.train()
                f1_score = trainer.eval('test',f1_pre)
                if f1_score > f1_pre:
                    trainer.save_model(f1_score)
                    f1_pre = f1_score
                else:
                    f1_pre = f1_pre
            if args.do_eval:
                _ = trainer.eval('test', f1_pre)
                break

if __name__ == "__main__":
    args = Config()
    main(args)
