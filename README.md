# NER for Vietnamese Medical Appointment Chatbot

# Usage

`from vi_nlp_core.ner.extractor import Extractor`

**Extract person name**

```
text = "tôi cần đặt bác sĩ tạ biên cương"
print(extractor.extract_person_name(text)
```

```
{'entities': [{'start': 19, 'end': 32, 'entity': 'person_name', 'value': 'Tạ Biên Cương', 'confidence': 1.0, 'extractor': 'pattern'}]}
```

**Extract Date**  
the value is the timestamp value

```
text = "tôi sinh vào ngày 21-3-1997"
extractor.extract_date(text)
```

```
{'entities': [{'start': 0, 'end': 5, 'entity': 'time', 'value': 1628562600.0, 'confidence': 1.0, 'extractor': 'absolute_pattern'}]}
```

**Extract Time**

```
text = '14:50 ngày 7 tháng 6'
print(extractor.extract_time(text,return_value=True)) #return value only
```

```
{'entities': [{'start': 7, 'end': 9, 'entity': 'time', 'value': 1628560800.0, 'confidence': 1.0, 'extractor': 'absolute_pattern'}]}
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

def extract_symptoms(self, utterance, input_symptoms= None, input_dep_keys=None, get_dep_keys=False, top_k=3):

- utterance : input string
- input_symptoms (optional): list of symptoms (e.g: ['đau bụng', 'sốt', 'ho', 'ói', 'nôn'])
- input_dep_keys (optional) : dict of department keys-keywords that you want to extract immediately
- get_dep_keys (optional) : whether return list of (dep-keys,value) only\
- top_k (optional) : return top_k answer (symptoms or dep_keys)
```
e.g:
    input_dict = {
        'A001': ['đau bụng', 'sốt', 'ho', 'ói', 'nôn', 'chóng mặt'],
        'A004': ['khó thở', 'đau ngực', 'sốt', 'nôn', 'ho'])
        )

```

Example :
- Common usage
```
text = "dạo này tôi thấy trong người mệt mỏi, thần kinh căng thẳng do cách ly covid quá lâu"
res = extractor.extract_symptoms(text)

{'entities': [{'start': 29, 'end': 32, 'entity': 'symptom', 'value': 'mệt', 'confidence': 1.0, 'extractor': 'fuzzy_matching'}, {'start': 39, 'end': 48, 'entity': 'symptom', 'value': 'thần kinh', 'confidence': 1.0, 'extractor': 'fuzzy_matching'}, {'start': 49, 'end': 59, 'entity': 'symptom', 'value': 'căng thẳng', 'confidence': 1.0, 'extractor': 'fuzzy_matching'}]}
```

- Extract Department Keys directly
```
res = extractor.extract_symptoms(text,get_dep_keys=True,top_k=3)

[('SP012', 1.0), ('SP001', 0.0), ('SP002', 0.0)]
```

- Extracting with given list of symptoms
```
text = "dạo này tôi thấy trong người mệt mỏi, thần kinh căng thẳng do cách ly covid quá lâu"
res = extractor.extract_symptoms(text, input_symptoms=['mệt mỏi', 'covid'])

{'entities': [{'start': 71, 'end': 76, 'entity': 'symptom', 'value': 'covid', 'confidence': 1.0, 'extractor': 'fuzzy_matching'}, {'start': 29, 'end': 36, 'entity': 'symptom', 'value': 'mệt mỏi', 'confidence': 1.0, 'extractor': 'fuzzy_matching'}]}
```

- Extracting with input_dep_keys
```
# CASE 1:
res = extractor.extract_symptoms(text, input_dep_keys=input_dict, get_dep_keys=True)

# CASE 2:
extractor.set_dep_symp_database(input_dict)
res = extractor.extract_symptoms(text, get_dep_keys=True)
```

**Search department from list of symptoms**
```
text = ['ho', 'sổ mũi', 'đau họng', 'đau đầu', 'nghẹt mũi']
res = extractor.get_department_from_symptoms(text,top_k=3)

[('SP018', 1.0), ('SP006', 0.6), ('SP009', 0.4)]
```
