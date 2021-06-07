from src.extractor import Extractor
extractor = Extractor()

text = "tôi muốn đặt lịch vào ngày 6 tháng 7"
print(extractor.extract_date(text))
text = "tôi sinh vào ngày 21-3-1997"
print(extractor.extract_date(text))
text = "ông pham hai nam"
print(extractor.extract_person_name(text,'pattern'))
