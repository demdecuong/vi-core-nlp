# NER for Vietnamese Medical Appointment Chatbot

# Usage

**Extractor NER**
```
import vi_nlp_core
from vi_nlp_core.ner.extractor import Extractor
extractor = Extractor()
text = 'tôi muốn đặt lịch với bs nguyễn nhật lệ lúc 8h sáng ngày 20/7'
print(extractor.extract_ner(text))
```
```
[{'start': 25, 'end': 44, 'entity': 'person_name', 'value': 'Nguyễn Nhật Lệ Lúc ', 'confidence': 1.0, 'extractor': 'pattern'}, {'start': 44, 'end': 46, 'entity': 'time', 'value': (8, 0), 'confidence': 1.0, 'extractor': 'absolute_pattern'}, {'start': 57, 'end': 61, 'entity': 'date_time', 'value': [(None, 20, 7, None)], 'confidence': 1.0, 'extractor': 'date_matcher'}]
```
**Extract person name**
```
text = "tôi cần đặt bác sĩ tạ biên cương"
print(extractor.extract_person_name(text)
```
```
{'entities': [{'start': 19, 'end': 32, 'entity': 'person_name', 'value': 'Tạ Biên Cương', 'confidence': 1.0, 'extractor': 'pattern'}]}
```

**Extract Date** 
```
text = "tôi sinh vào ngày 21-3-1997"
extractor.extract_date(text)
```
```
{'entities': [{'start': 18, 'end': 27, 'entity': 'date_time', 'value': [('thứ 6', 21, 3, 1997)], 'confidence': 1.0, 'extractor': 'date_matcher'}]}
```
**Extract Time**
```
text = '14:50 ngày 7 tháng 6'
print(extractor.extract_time(text,return_value=True)) #return value only
```
```
[(14, 50)]
```

**Map department/gender to keys**
```
text = 'rai'
res = extractor.map_gender_to_key(text)
print(res)
# {'key': 'GEN01', 'text': 'rai', 'value': 'trai'}
text = 'tiêu hóa'
res = extractor.map_dep_to_key(text)
print(res)
# {'key': 'SP008', 'text': 'tiêu hóa', 'value': 'tiêu hóa'}
```

**From symptoms to Department**
```
text = "dạo này tôi thấy trong người mệt mỏi, thần kinh căng thẳng do cách ly covid quá lâu"
res = extractor.extract_symptoms(text)
```
```
{'entities': [{'start': 29, 'end': 32, 'entity': 'symptom', 'value': 'mệt', 'confidence': 1.0, 'extractor': 'fuzzy_matching'}, {'start': 39, 'end': 48, 'entity': 'symptom', 'value': 'thần kinh', 'confidence': 1.0, 'extractor': 'fuzzy_matching'}, {'start': 49, 'end': 59, 'entity': 'symptom', 'value': 'căng thẳng', 'confidence': 1.0, 'extractor': 'fuzzy_matching'}]}
```
Extract Department Keys directly
```
res = extractor.extract_symptoms(text,get_dep_keys=True,top_k=3) 
```
```
[('SP012', 1.0), ('SP001', 0.0), ('SP002', 0.0)]
```
**Search department from list of symptoms**
```
text = ['ho', 'sổ mũi', 'đau họng', 'đau đầu', 'nghẹt mũi']
res = extractor.get_department_from_symptoms(text,top_k=3)
```
```
[('SP018', 1.0), ('SP006', 0.6), ('SP009', 0.4)]
```