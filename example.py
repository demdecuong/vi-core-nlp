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

# text = '7 giờ 20 kém 5 phút sáng thứ ba đầu tiên của tháng sau'

# print(extractor.extract_time(text))

# text = '2 tiếng nữa tại vinmec'
# print(extractor.extract_time(text))

# text = '3 giờ tiếp theo nhưng vào ngày mai'
# print(extractor.extract_time(text))

# text = '3 giờ 20 phút kế tiếp'
# print(extractor.extract_ner(text,'inform'))

text = "ngày mai"
print(extractor.extract_date(text))