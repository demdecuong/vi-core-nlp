from vma_nlu.ner.extractor import Extractor
from vma_nlu.tester import Tester
from vma_nlu.ner.pername_deeplearning.inference import Inference

pername_extractor_deeplearning = Inference()
extractor = Extractor(load_dict=False) # True: Load dictionary path

# text = '9h 20 phút '
# print(extractor.extract_time(text))

# text = 'bs nguyen tung an'
# print(extractor.extract_person_name(text))

text = 'tôi muốn đặt lịch với bs nguyễn nhật lệ lúc 8h sáng ngày 20/7'
print(extractor.extract_ner(text, "book_appt"))

x = pername_extractor_deeplearning.inference("đặt lịch với bác sĩ nguyễn huy tưởng lúc 9 giờ sáng mai")
print(x)