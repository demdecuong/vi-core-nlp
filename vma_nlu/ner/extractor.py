import re
import os

# from underthesea import ner
from vma_nlu.ner import date_matcher
from vma_nlu.utils.util import read_dict, get_ngram, tokenize
from vma_nlu.utils.pername_pattern import get_person_pattern, get_phone_pattern
from vma_nlu.utils.preproces import Preprocess
from vma_nlu.ner.date_matcher import DateMatcher
from vma_nlu.ner.time_matcher import TimeMatcher
from vma_nlu.ner.pername_matcher import PernameMatcher

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

        self.pername_extractor = PernameMatcher(
            n_gram, NAME_PATH, SW_PATH, load_dict)

        self.preprocessor = Preprocess()

    def extract_ner(self, utterance, intent):
        '''
        Extract NER based on given intent
        Input:
            utterance   -   string
            intent      -   string 
        Return
        '''
        #assert intent in ['greet','goodbye','thank','book_apt','change_apt','cancel_apt','inform','agree','disagree']
        try:
            if intent in ['inform', 'book_apt', 'change_apt']:
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

    def extract_time(self, utterance):
        '''
        Input:
            input string
        Output:
            return value of (hour,minute)
        '''
        result = self.time_extractor.extract_time(utterance)
        return result

    def extract_date(self, utterance):
        '''
        Input:
            input string
        Output:
            return tuple of (dow,dd,mm,yyyy)
        '''

        result = self.patternmatching_date.extract_date(utterance)
        return result

    def extract_person_name(self, utterance, mode='pattern', rt='relative'):
        '''
        Input:
            input string
        Output:
            return a json with 'value' is a string 
        '''
        result = self.pername_extractor.extract_person_name(utterance)
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
