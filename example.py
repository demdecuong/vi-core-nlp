from vma_nlu.ner.extractor import Extractor
from vma_nlu.tester import Tester

extractor = Extractor(load_dict=False) # True: Load dictionary path

text = 'tôi là hoàng vũ'

print(extractor.extract_person_name(text))

text = 'khoảng 7 den 8 giờ'
print(extractor.extract_time(text))

text = 'khoảng 7-8 giờ chiều mai'
print(extractor.extract_time(text))

text = 'ngày thứ 2 tuần sau vào lúc 9h30'
print(extractor.extract_time(text))

text = 'đặt lịch hôm nay, 20h'
print(extractor.extract_time(text))

text = 'đặt lịch hôm nay, 25h'
print(extractor.extract_time(text))

# text = "khoảng đầu chiều mai"
# text = "khoảng đầu buổi chiều được ạ"
# text = "khoảng đầu buổi chiều được ạ"
text = 'tầm cuối buổi sáng'
print(extractor.extract_time(text))