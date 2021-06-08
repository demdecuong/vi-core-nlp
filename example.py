from src.extractor import Extractor
extractor = Extractor()

text = "tôi muốn đặt lịch vào ngày 6 tháng 7"
print(extractor.extract_date(text))
text = "tôi sinh vào ngày 21-3-1997"
print(extractor.extract_date(text))
text = "tôi tên là pham hai nam"
print(extractor.extract_person_name(text,'pattern'))
text = "tôi cần đặt bác sĩ tạ biên cương"
print(extractor.extract_person_name(text,'pattern'))
text = "trời hôm nay nhiều mây cực"
print(extractor.extract_person_name(text,'pattern'))
# abs_pattern =  [
#     "(?:0?[1-9]|1[0-2])(?!\d| (?![ap]))[:.]?(?:(?:[0-5][0-9]))",
#     "(?=((?: |^)[0-2]?\d[:. ]?[0-5]\d(?:[:. ]?[0-5]\d)?(?:|$)))"
# ]

# text = 'sang 8:30 giờ chiều thu 7'
# for pattern in abs_pattern:
#     p = re.search(pattern,text)
#     if p != None:
#         print(p.group(0))