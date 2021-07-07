from vma_nlu.ner.extractor import Extractor
from vma_nlu.tester import Tester

extractor = Extractor(load_dict=False) # True: Load dictionary path

# text = '9h 20 phút '
# print(extractor.extract_time(text))

# text = 'bs nguyen tung an'
# print(extractor.extract_person_name(text))

text = 'tôi muốn đặt lịch với bs nguyễn nhật lệ lúc 8h sáng ngày 20/7'
print(extractor.extract_ner(text, "book_appt"))
