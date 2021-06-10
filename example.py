from vma_nlu.ner.extractor import Extractor

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

text = "tôi muốn đặt lịch vào ngày 6 tháng 7"
print(extractor.extract_date(text))
# [('None', ['ngày 6 '], ['tháng 7'], 'None')]

text = "vào sáng 1 tuần sau ngày 2.3"
print(extractor.extract_date(text))
# [('Thứ 6', '21', '3', '1997')]

# text = 'lúc 14 giờ 30 ngày 7 tháng 6'
# print(extractor.extract_time(text))

# text = 'mười bốn giờ 30 phút ngày 7 tháng 6'
# print(extractor.extract_time(text))

# text = 'hai mươi ba giờ 30 phút ngày 7 tháng 6'
# print(extractor.extract_time(text))

# text = 'ngày 7 tháng 6 lúc 14.15.00 giờ'
# print(extractor.extract_time(text))

# text = '18:30 tiếng kém mười lăm'
# print(extractor.extract_time(text))

