from vma_nlu.ner.extractor import Extractor

extractor = Extractor(load_dict=False) # True: Load dictionary path

text = "tôi tên là pham hai nam"
print(extractor.extract_person_name(text,'pattern'))

text = "tôi cần đặt bác sĩ tạ biên cương"
print(extractor.extract_person_name(text,'pattern'))

text = "trời hôm nay nhiều mây cực"
print(extractor.extract_person_name(text,'pattern'))

text = "tôi muốn đặt lịch vào ngày 6 tháng 7"
print(extractor.extract_date(text))
# [('None', ['ngày 6 '], ['tháng 7'], 'None')]

text = "tôi sinh vào ngày 21-3-1997"
print(extractor.extract_date(text))
# [('Thứ 6', '21', '3', '1997')]