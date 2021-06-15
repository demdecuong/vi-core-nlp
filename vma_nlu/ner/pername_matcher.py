''' 
    Author : Nguyen Phuc Minh
    Refactor for person name extractor . To be updated .
'''

from vma_nlu.utils.pattern import get_person_pattern, get_phone_pattern, get_time_pattern

class PernameMatcher:
    def __init__(self,n_gram = 4, load_dict=False):
        self.max_n_gram = n_gram
        if load_dict:
            self.fullname_dict = read_dict(NAME_PATH)
        else:
            self.fullname_dict = None
        
        self.stopwords_dict = read_dict(SW_PATH)

        self.person_explicit, self.person_pronoun, self.person_semi_pronoun, self.matches = self.build_person_name_pattern()

        self.preprocessor = Preprocess()
    
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