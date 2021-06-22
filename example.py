from vma_nlu.ner.extractor import Extractor
from vma_nlu.tester import Tester

extractor = Extractor(load_dict=False) # True: Load dictionary path

text = '6 tháng 8 2000'
print(extractor.extract_time(text))

