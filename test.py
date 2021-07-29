from vma_nlu.tester import Tester

tester = Tester()
# tester.test_template()
# print('----------------- Test person name -----------------')
# tester.test_person_name()

# print('----------------- Test time -----------------')
# tester.test_time()

# print('----------------- Test date -----------------')
# tester.test_date()

# tester.unit_test('time')


# VLSP-2016 TESTSET
# tester.test_person_name_vlsp('train')
# tester.test_person_name_vlsp('dev')
# tester.test_person_name_vlsp('test')

from vma_nlu.ner.extractor import Extractor

extractor = Extractor(load_dict=False) # True: Load dictionary path

text = 'tôi muốn đặt lịch với bs nguyễn nhật lệ lúc 8h sáng ngày 20/7'
print(extractor.extract_ner(text, "book_appt"))

text = '9h 20 phút '
print(extractor.extract_time(text))

text = 'bs nguyen tung an'
print(extractor.extract_person_name(text))
