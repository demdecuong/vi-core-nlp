import re
import os

# from underthesea import ner
from vi_nlp_core.ner import date_matcher
from vi_nlp_core.utils.util import read_dict, get_ngram, tokenize
from vi_nlp_core.utils.pername_pattern import get_person_pattern, get_phone_pattern
from vi_nlp_core.utils.preproces import Preprocess
from vi_nlp_core.ner.date_matcher import DateMatcher
from vi_nlp_core.ner.time_matcher import TimeMatcher
from vi_nlp_core.ner.pername_matcher import PernameMatcher
from vi_nlp_core.ner.gender_matcher import GenderMatcher
from vi_nlp_core.ner.dep_matcher import DepMatcher
from vi_nlp_core.ner.symptom_matcher import SymptomMatcher

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
NAME_PATH = os.path.join(ROOT_DIR, 'data/fullname.pkl')
SW_PATH = os.path.join(ROOT_DIR, 'data/stopwords.pkl')
DATE_PATH = os.path.join(ROOT_DIR, 'data/dictionary_normalize_date.json')


class Extractor:
    def __init__(self, n_gram=4, load_dict=False):

        self.max_n_gram = n_gram

        self.phone_regex = get_phone_pattern()

        self.patternmatching_date = DateMatcher(DATE_PATH)

        self.time_extractor = TimeMatcher()

        self.gender_matcher = GenderMatcher()
        
        self.dep_matcher = DepMatcher()
        
        self.pername_extractor = PernameMatcher(
            n_gram, NAME_PATH, SW_PATH, load_dict)

        self.symptom_matcher = SymptomMatcher()

        self.preprocessor = Preprocess()

        # self.pername_extractor_deeplearning = Inference()
    def extract_ner(self, utterance):
        '''
        Extract NER based on given intent
        Input:
            utterance   -   string
            return_value    return value only 
        Return
        '''
        result = []
        person_name = self.extract_person_name(utterance)['entities']

        if person_name != []:
            result.extend(person_name)
        time = self.extract_time(utterance)['entities']
        if time != []:
            result.extend(time)
        date = self.extract_date(utterance)['entities']
        if date != []:
            result.extend(date)
        return result

    def extract_ner_old(self, utterance, intent):
        '''
        Extract NER based on given intent
        Input:
            utterance   -   string
            intent      -   string 
        Return
        '''
        #assert intent in ['greet','goodbye','thank','book_appt','change_appt','cancel_appt','inform','agree','disagree']
        try:
            if intent in ['inform', 'book_appt', 'change_appt', 'cancel_appt']:
                result = []
                person_name = self.extract_person_name(utterance)['entities']
                print(person_name)
                if person_name != []:
                    result.extend(person_name)
                time = self.extract_time(utterance)['entities']
                print(time)
                if time != []:
                    result.extend(time)
                date = self.extract_date(utterance)['entities']
                print(date)
                if date != []:
                    result.extend(date)
                return result
                # return {
                #         'entities' : result
                #     }
            else:
                return []
        except Exception as ex:
            print(ex)
            return []

    def extract_time(self, utterance, return_value = False):
        '''
        Input:
            utterance :  string
            return_value : return value only
        Output:
            return value of (hour,minute)
        '''
        result = self.time_extractor.extract_time(utterance)
        if return_value:
            final_result = []
            for ent in result['entities']:
                final_result.append(ent['value'])
            return final_result
        return result

    def extract_date(self, utterance, return_value = False):
        '''
        Input:
            utterance : input string
            return_value : return value only
        Output:
            return tuple of (dow,dd,mm,yyyy)
        '''
        result = self.patternmatching_date.extract_date(utterance)
        if return_value:
            final_result = []
            for ent in result['entities']:
                final_result.append(ent['value'])
            return final_result
        return result

    def extract_person_name(self, utterance, return_value= False):
        '''
        Input:
            input string
        Output:
            return a json with 'value' is a string 
        '''
        result = self.pername_extractor.extract_person_name(utterance)
        if return_value:
            final_result = []
            for ent in result['entities']:
                final_result.append(ent['value'])
            return final_result
        return result

    def extract_phone_num(self, utterance):
        '''
        Use regex for pattern matching (nha mang + remain numbers)
        Input:
            utterance  - string
        Return:
            string      :   phone number
            'Invalid'   :   otherwise
        '''
        result = re.findall(self.phone_regex, utterance)
        if result == []:
            return 'Invalid'
        else:
            nha_mang = result[0][0]
            remain = result[0][1]
            return nha_mang + remain
    
    def extract_all(self, utterance):
        time = self.extract_time(utterance)
        date = self.extract_date(utterance)

        person_name = self.extract_person_name(utterance)
        return time, date, person_name  

    def map_gender_to_key(self, str):
        return self.gender_matcher.map_gender_to_key(str)

    def map_dep_to_key(self, str):
        return self.dep_matcher.map_dep_to_key(str)

    def get_department_from_symptoms(self, symptoms):
        return self.symptom_matcher.get_department_from_symptoms(symptoms)

    def extract_symptoms(self, utterance, get_dep_keys=False, top_k=3):
        return self.symptom_matcher.extract_symptoms(utterance, get_dep_keys=get_dep_keys, top_k=top_k)