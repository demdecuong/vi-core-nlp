import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from vi_nlp_core.utils.util import read_dict, get_ngram, tokenize, padding_punct
from vi_nlp_core.utils.dep_pattern import get_dep_dict, get_dep_symptoms_dict, get_dep_keys, get_list_of_symps
from vi_nlp_core.utils.preproces import Preprocess


class SymptomMatcher:
    def __init__(self, n_grams=4, threshold=30):

        self.max_n_gram = n_grams

        self.dep_symp_dict = self.get_extend_dep_symp_dict()
        # self.dep_keys = get_dep_keys()
        # self.list_of_symptoms = self.get_list_of_symptoms()

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
            res = self.fuzzy_matching(str, self.threshold)
            res = self.format_output(str, res[0], res[1])
            return res

    def extract_symptoms(self, utterance, input_symptoms= None, input_dep_keys=None, get_dep_keys=False, top_k=3):
        '''
        get_dep_keys : get_dep_keys from utterance
        top_k : use whenever get_dep_keys is True
        '''
        utterance = self.preprocess(utterance).lower()

        if input_symptoms is not None or input_dep_keys is not None:
            input_symptoms = self.unify_input_symptoms(input_symptoms, input_dep_keys) # list

        if input_symptoms is not None:
            symptoms = self.get_symptoms(utterance,input_symptoms=input_symptoms)
            if symptoms != [] and get_dep_keys:
                data = []
                for ent in symptoms:
                    data.append(ent['value'])
                result = self.get_department_from_symptoms(data, input_dep_keys, top_k)
            elif symptoms == []:
                # 'No symptoms are existed or some symptoms are not updated in database'
                result = None
            else:
                result = {}
                result['entities'] = symptoms

            return result
        else:

            symptoms = self.get_symptoms(utterance)
            if symptoms != [] and get_dep_keys:
                data = []
                for ent in symptoms:
                    data.append(ent['value'])
                result = self.get_department_from_symptoms(data, input_dep_keys, top_k)
            elif symptoms == []:
                # 'No symptoms are existed or some symptoms are not updated in database'
                result = None
            else:
                result = {}
                result['entities'] = symptoms

            return result

    def get_symptoms(self, utterance, input_symptoms=None):
        result = []
        history = []
        for i in range(1,self.max_n_gram):
            ngrams = get_ngram(utterance, i)
            for item in ngrams:
                if len(item) > 1:
                    item = ' '.join(item)
                else:
                    item = item[0]
                symptom = self.fuzzy_matching(item, input_symptoms=input_symptoms, threshold=85)
                if symptom != []:
                    symptom = symptom[1]
                    start = utterance.find(item)
                    end = start + len(item)
                    obj = {
                        "start": start,
                        "end": end,
                        "entity": "symptom",
                        "value": symptom,
                        "confidence": 1.0,
                        "extractor": 'fuzzy_matching'
                    }

                    if symptom not in history:
                        result.append(obj)
                        history.append(symptom)
        return result

    def extract_matching(self, str):
        for k, v in self.gender_dict.items():
            for token in v:
                if token in str.split(' '):
                    return (self.keys[k], token)
        return None

    def fuzzy_matching(self, str, input_symptoms=None, threshold=75):
        scores = []
        dep_symp_dict = self.dep_symp_dict
        if input_symptoms is not None:
            dep_symp_dict = {}
            dep_symp_dict['A001'] = input_symptoms

        for k, v in dep_symp_dict.items():
            ratios = [fuzz.ratio(str, value)
                      for value in v]  # ensure both are in string
            scores.append({"key": k, "score": max(ratios),
                           'value': v[ratios.index(max(ratios))]})

        filtered_scores = [
            item for item in scores if item['score'] >= threshold]
        if filtered_scores == []:
            return filtered_scores
        sorted_filtered_scores = sorted(
            filtered_scores, key=lambda k: k['score'], reverse=True)

        return (sorted_filtered_scores[0]['key'], sorted_filtered_scores[0]['value'])

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

    def get_department_from_symptoms(self, symptoms,input_dep_keys=None, top_k=3):
        '''
        symptoms : list of symptoms
        '''
        score_list = []

        dep_symp_dict = self.dep_symp_dict
        if input_dep_keys is not None:
            dep_symp_dict = input_dep_keys

        for i, (dep, dep_symptoms) in enumerate(dep_symp_dict.items()):
            score = self.get_department_score(symptoms, dep_symptoms)
            score_list.append({
                'score': score,
                'key': dep})
        filtered_scores = sorted(
            score_list, key=lambda k: k['score'], reverse=True)

        res = [(item['key'], item['score'])
               for item in filtered_scores[:top_k] if item['score'] != 0]

        return res

    def get_list_of_symptoms(self):
        data = []
        for k, v in self.dep_symp_dict.items():
            data.extend(v)
        
        li_symps = get_list_of_symps()
        data.extend(li_symps)
        data = list(set(data))
        return data

    def preprocess(self, text):
        text = text.replace('\n', '').strip()
        text = re.sub('(?<! )(?=[,!?()])|(?<=[,!?()])(?! )', r' ', text)
        return text

    def get_extend_dep_symp_dict(self):
        d = {}
        d1 = get_dep_dict()
        d2 = get_dep_symptoms_dict()
        for k, v in d1.items():
            d[k] = v
            d[k].extend(d2[k])
        return d

    # def set_list_of_symptoms(self, input_list):
    #     self.list_of_symptoms = input_list

    def set_dep_symp_database(self, input_dict):
        '''
            input_dict = {
                'SP001' : ['sot','buon ngu','chong mat'],
                'SP002' : ['sot','buon ngu','chong mat'],
            }
        '''
        self.dep_symp_dict = input_dict
    
    def unify_input_symptoms(self,input_symptoms=None, input_dep_keys=None):
        res = []
        if input_dep_keys is not None:
            for k, v in input_dep_keys.items():
                res.extend(v)
        if input_symptoms is not None:
            res.extend(input_symptoms)
        res = list(set(res))
        return res