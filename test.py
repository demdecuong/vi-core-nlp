from vi_nlp_core.tester import Tester

tester = Tester()
# tester.test_template()
# print('----------------- Test person name -----------------')
# tester.test_person_name()

# print('----------------- Test time -----------------')
# tester.test_time()

# print('----------------- Test date -----------------')
# tester.test_date()

from vi_nlp_core.ner.extractor import Extractor

extractor = Extractor(load_dict=False) # True: Load dictionary path

text = 'tôi muốn đặt lịch với bs nguyễn nhật lệ lúc 8h sáng ngày 20/7'
print(extractor.extract_ner(text, "book_appt"))

text = '9h 20 phút '
print(extractor.extract_time(text))

text = 'bs nguyen tung an'
print(extractor.extract_person_name(text))
