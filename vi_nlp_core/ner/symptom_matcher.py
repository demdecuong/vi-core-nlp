import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from vi_nlp_core.utils.util import read_dict, get_ngram, tokenize
from vi_nlp_core.utils.dep_pattern import get_dep_dict, get_dep_symptoms_dict, get_dep_keys
from vi_nlp_core.utils.preproces import Preprocess


class SymptomMatcher:
    def __init__(self, threshold=30):

        self.dep_symp_dict = get_dep_symptoms_dict()
        self.dep_keys = get_dep_keys()

        # for fuzzy match
        self.threshold = threshold
        self.preprocessor = Preprocess()

    def map_gender_to_key(self, str):
        '''
        1. Semi/Extract matching
        2. Fuzzy mathching
        '''
        str = str.lower()
        res = self.extract_matching(str)

        if res != None:
            res = self.format_output(str, res[0], res[1])
            return res
        else:
            res = self.fuzzy_matching(str)
            res = self.format_output(str, res[0], res[1])
            return res

    def extract_symptoms(self, utterance):
        pass

    def extract_matching(self, str):
        for k, v in self.gender_dict.items():
            for token in v:
                if token in str.split(' '):
                    return (self.keys[k], token)
        return None

    def fuzzy_matching(self, str):
        scores = []
        for k, v in self.gender_dict.items():
            ratios = [fuzz.ratio(str, value)
                      for value in v]  # ensure both are in string
            scores.append({"key": k, "score": max(ratios),
                           'value': v[ratios.index(max(ratios))]})

        filtered_scores = [
            item for item in scores if item['score'] >= self.threshold]
        sorted_filtered_scores = sorted(
            filtered_scores, key=lambda k: k['score'], reverse=True)

        return (self.keys[filtered_list_of_dicts[0]['key']], filtered_list_of_dicts[0]['value'])

    def format_output(self, text, key, value):
        return {
            'key': key,
            'text': text,
            'value': value
        }

    def get_department_score(self, symptoms, dep_symptoms):
        cnt = 0
        for item in symptoms:
            if item.lower() in dep_symptoms:
                cnt += 1
        return cnt/len(symptoms)

    def get_department_from_symptoms(self, symptoms, top_k=3):
        '''
        symptoms : list of symptoms
        '''
        score_list = []

        for i, (dep, dep_symptoms) in enumerate(self.dep_symp_dict.items()):
            score = self.get_department_score(symptoms, dep_symptoms)
            score_list.append({
                'score': score,
                'key': dep})
        filtered_scores = sorted(
            score_list, key=lambda k: k['score'], reverse=True)

        res = [(self.dep_keys[item['key']],item['score']) for item in filtered_scores[:top_k]]

        return res
