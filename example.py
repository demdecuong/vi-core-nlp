from src.extractor import Extractor

extractor = Extractor(load_dict=False) # True: Load dictionary path

text = "tôi tên là pham hai nam"
print(extractor.extract_person_name(text,'hybrid'))

text = "tôi cần đặt bác sĩ tạ biên cương"
print(extractor.extract_person_name(text,'hybrid'))

text = "trời hôm nay nhiều mây cực"
print(extractor.extract_person_name(text,'hybrid'))