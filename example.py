from vma_nlu.ner.extractor import Extractor

extractor = Extractor(load_dict=False) # True: Load dictionary path

text = "tôi tên là pham hai nam"
print(extractor.extract_person_name(text,'pattern'))

text = "tôi tên là Nam"
print(extractor.extract_person_name(text,'pattern'))

text = "tôi cần đặt bác sĩ tạ biên cương"
print(extractor.extract_person_name(text,'pattern'))

text = "tao 653216565489421"
print(extractor.extract_person_name(text,'pattern'))

text = "216565489421"
print(extractor.extract_person_name(text,'pattern'))

text = "xin cái điện chỉ nhà thằng Văn"
print(extractor.extract_person_name(text,'pattern'))

text = "không biết hôm nay trời mưa không"
print(extractor.extract_person_name(text,'pattern'))

text = "trời hôm nay nhiều mây cực"
print(extractor.extract_person_name(text,'pattern'))

text = "tôi muốn đặt lịch vào ngày 6 tháng 7"
print(extractor.extract_date(text))
# [('None', ['ngày 6 '], ['tháng 7'], 'None')]

text = "tôi sinh vào ngày 21-3-1997"
print(extractor.extract_date(text))
# [('Thứ 6', '21', '3', '1997')]