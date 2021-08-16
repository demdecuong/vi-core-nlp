from vi_nlp_core.ner.extractor import Extractor
# from vi_nlp_core.tester import Tester
# from vi_nlp_core.ner.pername_deeplearning.inference import Inference

# pername_extractor_deeplearning = Inference()
extractor = Extractor(load_dict=False)  # True: Load dictionary path

text = '9h 20 phút '
print(extractor.extract_time(text))

text = 'bs nguyen tung an'
print(extractor.extract_person_name(text))

text = 'tôi muốn đặt lịch với bs nguyễn nhật lệ lúc 8h sáng ngày 20/7'
print(extractor.extract_ner(text))

text = 'rai'
res = extractor.map_gender_to_key(text)
print(res)
text = 'tiêu hóa'
res = extractor.map_dep_to_key(text)
print(res)

text = ['ho', 'sổ mũi', 'đau họng', 'đau đầu', 'nghẹt mũi']
res = extractor.get_department_from_symptoms(text)
print(res)

text = "dạo này tôi thấy trong người mệt mỏi, thần kinh căng thẳng do cách ly covid quá lâu"
res = extractor.extract_symptoms(text)
print(res)

text = "dạo này tôi thấy trong người mệt mỏi, thần kinh căng thẳng do cách ly covid quá lâu"
res = extractor.extract_symptoms(text, input_symptoms=['mệt mỏi', 'covid'])
print(res)

input_dict = {
    'A001': [
        'đau bụng', 'sốt', 'ho', 'ói', 'nôn', 'chóng mặt', 'đau ngực', 'đau khớp', 'mất'
        'ngủ', 'lo âu', 'khó thở', 'tăng huyết áp', 'giảm huyết áp', 'cao huyết áp',
        'đau họng,' 'đau khớp', 'mỏi vai gáy', 'mỏi vai', 'tiểu đường', 'mệt',
    ],
    'A002': [
        'ngứa', 'nổi sẩn', 'da dày sừng', 'bong vảy', 'mụn nước', 'bóng nước', 'chảy dịch',
        'mụn mủ', 'loét', 'mụn trứng cá', 'ngứa da', 'ngứa âm đạo', 'vảy nến',
        'dị ứng', 'phát ban', 'nổi bóng nước', 'phù mặt', 'khó thở', 'mụn', 'nám',
        'mụn cóc', 'đỏ da', 'phát ban', 'dị ứng', 'loét', 'áp-xe', 'hoại tử ', 'nổi nốt', ],
    'A003': ['béo', 'gầy', 'mập', 'nhẹ cân',
             'thiếu cân', 'ốm', 'tăng cân', 'suy dinh dưỡng'],
    'A004': ['khó thở', 'đau ngực', 'sốt', 'nôn', 'ho']
}
res = extractor.extract_symptoms(
    text, input_dep_keys=input_dict, get_dep_keys=True)
print(res)

extractor.set_dep_symp_database(input_dict)
res = extractor.extract_symptoms(
    text, get_dep_keys=True)
print(res)

text = 'ngày 28 tháng 4 năm 1999'
print(extractor.extract_date(text))
text = 'khoảng 9h em qua nha bác sĩ '
print(extractor.extract_time(text))
text = '2021/13/31'
res = extractor.extract_date(text)
print(res)

# extract symptoms by list of keywords

# set symptoms database

# extract_symptoms , get_dep_keys = True  || by user database
# set_dep_keys
#
