from vma_nlu.ner.extractor import Extractor
from vma_nlu.tester import Tester

extractor = Extractor(load_dict=False) # True: Load dictionary path

text = '9h 20 phút '
print(extractor.extract_time(text))

text = 'bs nguyen tung an'
print(extractor.extract_person_name(text))
