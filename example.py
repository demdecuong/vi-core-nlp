from vma_nlu.ner.extractor import Extractor
from vma_nlu.tester import Tester

extractor = Extractor(load_dict=False) # True: Load dictionary path

# text = "tôi tên là pham hai nam"
# print(extractor.extract_person_name(text,'pattern'))

# text = "tôi tên là Nam"
# print(extractor.extract_person_name(text,'pattern'))

# text = "tôi cần đặt bác sĩ tạ biên cương"
# print(extractor.extract_person_name(text,'pattern'))

# text = "tao 653216565489421"
# print(extractor.extract_person_name(text,'pattern'))

# text = "216565489421"
# print(extractor.extract_person_name(text,'pattern'))

# text = "xin cái điện chỉ nhà thằng Văn"
# print(extractor.extract_person_name(text,'pattern'))

# text = "không biết hôm nay trời mưa không"
# print(extractor.extract_person_name(text,'pattern'))

# text = "trời hôm nay nhiều mây cực"
# print(extractor.extract_person_name(text,'pattern'))

# text = "tôi muốn đặt lịch vào ngày 6 tháng 7"
# print(extractor.extract_date(text))
# # [('None', ['ngày 6 '], ['tháng 7'], 'None')]

# text = "vào sáng 1 tuần sau ngày 2.3"
# print(extractor.extract_date(text))
# # [('Thứ 6', '21', '3', '1997')]

# text = '14:50 ngày 7 tháng 6'
# print(extractor.extract_time(text))

# text = '14h50 ngày 7 tháng 6'
# print(extractor.extract_time(text))

# text = 'lúc 14 giờ 30 ngày 7 tháng 6'
# print(extractor.extract_time(text))

# text = 'mười bốn giờ 30 phút ngày 7 tháng 6'
# print(extractor.extract_time(text))

# text = 'ngày 7 tháng 6 lúc 14.15.00 giờ'
# print(extractor.extract_time(text))

text = 'tôi là hoàng vũ'

print(extractor.extract_person_name(text))

text = 'khoảng 7 den 8 giờ'
print(extractor.extract_time(text))

text = 'khoảng 7-8 giờ chiều mai'
print(extractor.extract_time(text))

text = 'ngày thứ 2 tuần sau vào lúc 9h30'
print(extractor.extract_time(text))

text = 'ngày thứ 2 tuần sau vào lúc 9 giờ 30'
print(extractor.extract_time(text))

# text = "khoảng đầu chiều mai"
# text = "khoảng đầu buổi chiều được ạ"
# text = "khoảng đầu buổi chiều được ạ"
text = 'tầm cuối buổi sáng'
print(extractor.extract_time(text))