import time
from src.extractor import Extractor
extractor = Extractor()

start = time.time()
text2 = "tôi tên là pham hai nam"
print(extractor.extract_person_name(text2,'pattern'))
print(time.time() - start) 
# pattern : 0.00014662742614746094
# dict + pattern : 0.0001785755157470703