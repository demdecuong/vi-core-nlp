import re

from underthesea import ner
from vma_nlu.utils.util import read_dict, get_ngram, tokenize
from vma_nlu.utils.pattern import get_person_pattern, get_phone_pattern, get_time_pattern
from vma_nlu.utils.PMdate import PatternMatching
from vma_nlu.utils.Preprocess import Preprocess

class Extractor:
    def __init__(self,n_gram = 4, dict_path='./vma_nlu/data/fullname.pkl',load_dict=False):

        self.max_n_gram = n_gram
        if load_dict:
            self.fullname_dict = read_dict(dict_path)
        else:
            self.fullname_dict = None

        self.phone_regex = get_phone_pattern()

        self.person_explicit, self.person_pronoun, self.person_semi_pronoun, self.matches = self.build_person_name_pattern()

        self.patternmatching_date = PatternMatching()

        self.time_absolute, self.am_pattern, self.pm_pattern = get_time_pattern()

        self.preprocessor = Preprocess()
        
    def extract_time(self,utterance):
        '''
        1. Get hour and minute
        2. Get AM/PM
        Input:
            input string
        Return:
            tuple of (hour,minute,AM/PM)
        '''
        pass
        # utterance = tokenize(utterance).lower()

        # if utterance.find('giờ') != -1:
        #     list_of_words = utterance.split(' ')
        #     key_index = list_of_words.index('giờ')
        #     pot_num = 2
        #     potential_range = list_of_words[max(0,key_index - pot_num):min(key_index + pot_num,len(list_of_words))]
        #     # for token in potential_range:
        # else:
        #     # Get raw form in hour/minute
        #     for pattern in self.time_absolute:
        #         time = re.search(pattern,utterance)
        #     if '.' in time:
        #         hour,minute = time.split('.')
        #     elif ':' in time:
        #         hour,minute = time.split(':')

        # Get AM/PM       
        
    def extract_date(self,utterance):
        '''
        Input:
            input string
        Output:
            return tuple of (dow,dd,mm,yyyy)
        '''
        result = self.patternmatching_date.extract_date(utterance)
        return result

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
        # Normalize Uncicode
        # utterance = self.preprocessor.preprocess(utterance)
        utterance = tokenize(utterance).lower()
        if mode == 'dictionary':
            assert self.fullname_dict != None
            # Aho-corasik searching
            dict_result = self.extract_person_name_dict(utterance)
            return self.output_format(
                    output = dict_result, 
                    utterance = utterance,
                    extractor = mode,
                    entity = 'person_name'
                )
        elif mode == 'pattern':
            # Pattern matching
            pattern_result = self.extract_person_name_pattern(utterance)
            if pattern_result != 'Invalid':
                pattern_result = [pattern_result]
            return self.output_format(
                    output = pattern_result, 
                    utterance = utterance,
                    extractor = mode,
                    entity = 'person_name'
                )
        else:
            # Dictionay + pattern matching
            result = []
            dict_result = self.extract_person_name_dict(utterance)
            pattern_result = self.extract_person_name_pattern(utterance)
            if dict_result != 'Invalid':
                result.append(dict_result)
            if pattern_result != 'Invalid':
                result.append(pattern_result)
            result = list(set(result))
            if result != []:
                return  self.output_format(
                        output = result, 
                        utterance = utterance,
                        extractor = mode,
                        entity = 'person_name'
                    )
            else:
                return  self.output_format(
                        output = 'Invalid',
                        utterance = utterance,
                        extractor = mode,
                        entity = 'person_name'
                    )

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
        assert self.fullname_dict != None # Can not empty dictionary
        result = []
        for i in range(self.max_n_gram,2,-1):
            ngrams = get_ngram(utterance.lower(),i)
            for item in ngrams:
                item = ' '.join(item)
                if self.get_name(item) != 'not_exists' and item not in result:
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
        if any(x in utterance for x in self.matches):
            for pattern_list in self.person_pronoun:
                for pattern in pattern_list:
                    pronoun = re.search(pattern,utterance)
                    if pronoun != None and pronoun.group(1) != None:
                        return pronoun.group(1)
            semi_pronoun = self.person_semi_pronoun.search(utterance)
            try:
                if semi_pronoun != None and semi_pronoun.group(1) != None:
                    return semi_pronoun.group(1)
            except:
                return 'Invalid' 
        else:
            explicit = self.person_explicit.search(utterance)
            try:
                if explicit != None and explicit.group(1) != None:
                    return explicit.group(1)
            except:
                return 'Invalid'

    def get_name(self,s):
        try:
            return self.fullname_dict.get(s,'not_exists')
        except:
            print('Your dictionary is now empty')
            print('Ensure you have load the vocabulary for fullname_dict ! Otherwise you can run self.load_dict() update the dictionary .')
            return 'not_exists'
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

        return person_explicit, format_pronoun, person_semi_pronoun, matches
    
    def output_format(self,output,utterance,extractor,entity):
        if entity == 'person_name':
            if output == 'Invalid':
                return {
                    'entities' : []
                }
            else:
                entities = []
                for ent in output:
                    entities.append(self.output_person_format(ent,utterance,extractor))
                return {
                    'entities' : entities
                }

    def output_person_format(self,output,utterance,extractor):
        '''
        1. Get start/end index
        2. Capitalize entity
        Input:
            output - string
                person name entity
            utterance - string
                raw input string from user
            extractor - string in ['dictionary','pattern','hybrid']
                method of extractor 
        '''
        start = utterance.find(output)
        end = start + len(output)

        output = output.split(' ')
        value = ' '.join([x.capitalize() for x in output])
        
        return {
                "start": start,
                "end": end,
                "entity": "person_name",
                "value": value,
                "confidence": 1.0,
                "extractor": extractor
                }

    def load_dict(self,dict_path='./vma_nlu/data/fullname.pkl'):
        print('Loading person name vocabulary ...')
        self.fullname_dict = read_dict(dict_path)