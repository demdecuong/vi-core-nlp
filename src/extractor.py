import re
from underthesea import ner
from src.utils.util import read_dict, get_ngram, tokenize
from src.utils.pattern import get_person_pattern, get_phone_pattern

class Extractor:
    def __init__(self,n_gram = 4,dict_path='./src/data/fullname.pkl'):

        self.max_n_gram = n_gram
        # self.fullname_dict = read_dict(dict_path)

        self.phone_regex = get_phone_pattern()

        self.person_explicit, self.person_pronoun, self.person_semi_pronoun, self.matches = self.build_person_name_pattern()

    def extract_time(self,input):
        pass

    def extract_date(self,input):
        pass

    def extract_date_time(self,input):
        pass
    
    def extract_person_name(self,utterance,mode='pattern'):
        '''
        1. Extract ngrams from (max_ngram,2)
        2. Check each ngram is in dictionary (aho-corasik)
        Input:
            utterance  - string
            mode - string
                dictionary : dictionary-based
                pattern : pattern matching
                hybrid : dictionary + pattern
        Return:
            string      :   persone name
            'Invalid'   :   otherwise
        '''
        assert mode in ['dictionary','pattern','hybrid']

        if mode == 'dictionary':
            # Aho-corasik searching
            dict_result = self.extract_person_name_dict(utterance)
            return dict_result
        elif mode == 'pattern':
            # Pattern matching
            pattern_result = self.extract_person_name_pattern(utterance)
            return pattern_result
        else:
            # Dictionay + pattern matching
            result = []
            dict_result = self.extract_person_name_dict(utterance)
            pattern_result = self.extract_person_name_pattern(utterance)
            result.extend(dict_result)
            result.extend(pattern_result)
            result = list(set(result))
            return result

    def extract_person_name_dict(self,utterance):
        '''
        1. Extract ngrams from (max_ngram,2)
        2. Check each ngram is in dictionary (aho-corasik)
        Input:
            utterance  - string
        Return:
            list      :   list of persone name
            'Invalid'   :   otherwise
        '''
        result = []
        for i in range(self.max_n_gram,2,-1):
            ngrams = get_ngram(utterance.lower(),i)
            for item in ngrams:
                item = ' '.join(item)
                if self.get_name(item) != 'not_exists':
                    result.append(item)
        if result != []:         
            return result   
        else:
            return "Invalid"
            
    def extract_person_name_pattern(self,utterance):
        '''
        Logic flow : 
            Pronoun --> semi pronoun --> explicit
        Input:
            utterance  - string
        Return:
            stirng      :   persone name
            'Invalid'   :   otherwise
        '''
        utterance = tokenize(utterance).lower()
        if any(x in utterance for x in self.matches):
            for pattern in self.person_pronoun:
                pronoun = pattern.search(utterance)
                if pronoun != None and pronoun.group(1) != None:
                    return pronoun.group(1)
            semi_pronoun = self.person_semi_pronoun.search(utterance)

            if semi_pronoun != None and semi_pronoun.group(1) != None:
                return semi_pronoun.group(1)
            else:
                return 'Invalid' 
        else:
            explicit = self.person_explicit.search(utterance)
            if explicit != None:
                return explicit.group(1)
            else:
                return 'Invalid'

    def get_name(self,s):
        return self.fullname_dict.get(s,'not_exists')

    def extract_phone_num(self,utterance):
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

    def build_person_name_pattern(self):
        '''
        Input: 
            None
        Return:
            List of regex format pattern
        '''
        person_explicit, format_pronoun, person_semi_pronoun, matches = get_person_pattern()
        
        person_pronoun = [0]*len(format_pronoun)

        person_explicit = "|".join(person_explicit)
        person_semi_pronoun = "|".join(person_semi_pronoun)

        person_explicit = re.compile(person_explicit)
        person_semi_pronoun = re.compile(person_semi_pronoun)

        for i,pattern in enumerate(format_pronoun):
            person_pronoun[i] = re.compile("|".join(pattern))

        return person_explicit, person_pronoun, person_semi_pronoun, matches