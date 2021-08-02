import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process 

from vi_nlp_core.utils.util import read_dict, get_ngram, tokenize
from vi_nlp_core.utils.dep_pattern import get_dep_dict,get_dep_symptoms_dict,get_dep_keys
from vi_nlp_core.utils.preproces import Preprocess

class DepMatcher:
    def __init__(self, threshold=30):
        
        self.dep_dict = get_dep_dict()
        self.keys = get_dep_keys()
        
        # for fuzzy match
        self.threshold = threshold 
        
        self.preprocessor = Preprocess()
    
    def map_dep_to_key(self, str):
        '''
        1. Semi/Extract matching
        2. Fuzzy mathching
        '''
        str = str.lower()
        res = self.extract_matching(str)

        if res != None:
            res = self.format_output(str,res[0],res[1])
            return res
        else:
            res = self.fuzzy_matching(str)
            res = self.format_output(str,res[0],res[1])
            return res
    
    def extract_matching(self, str):
        for k, v in self.dep_dict.items():
            for token in v:
                if token in str.split(' '):
                    return (self.keys[k], token)
        return None
        
    def fuzzy_matching(self, str):
        scores = []
        for k, v in self.dep_dict.items():
            ratios = [fuzz.ratio(str, value)
                      for value in v]  # ensure both are in string
            scores.append({"key": k, "score": max(ratios),'value': v[ratios.index(max(ratios))]})

        filtered_scores = [
            item for item in scores if item['score'] >= self.threshold]
        sorted_filtered_scores = sorted(
            filtered_scores, key=lambda k: k['score'], reverse=True)
        filtered_list_of_dicts = [ item
                                  for item in sorted_filtered_scores]
        return (self.keys[filtered_list_of_dicts[0]['key']], filtered_list_of_dicts[0]['value'])


    def get_keys(self):
        return self.keys

    def get_dict(self):
        return self.dep_dict

    def format_output(self, text, key, value):
        return {
            'key': key,
            'text': text,
            'value': value
        }
