from src.extractor import Extractor
extractor = Extractor()

text2 = "tôi tên là pham hai nam"
print(extractor.extract_person_name(text2,'pattern'))