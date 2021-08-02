from vi_nlp_core.ner.extractor import Extractor
from vi_nlp_core.tester import Tester
# from vi_nlp_core.ner.pername_deeplearning.inference import Inference

# pername_extractor_deeplearning = Inference()
extractor = Extractor(load_dict=False) # True: Load dictionary path

text = '9h 20 phút '
print(extractor.extract_time(text))

text = 'bs nguyen tung an'
print(extractor.extract_person_name(text))

text = 'tôi muốn đặt lịch với bs nguyễn nhật lệ lúc 8h sáng ngày 20/7'
print(extractor.extract_ner(text))

text = 'rai'
res = extractor.map_gender_to_key(text)
print(res)
text = 'tiêu hóa'
res = extractor.map_dep_to_key(text)
print(res)