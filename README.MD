# Installation
```
pip install -r requirements.txt
```
# Usage

**Extract Vietnamese phone number**
```
from vma_nlu.extractor import Extractor

extractor = Extractor()
text = "sdt : 0349933957 ok chua"

print(extractor.extract_phone_num(text))
# 0349933957
```
Inference time :  0.00015s

**Extract person name**
```
from vma_nlu.extractor import Extractor

extractor = Extractor()

text = "tôi tên là pham hai nam"
print(extractor.extract_person_name(text,'pattern'))

text = "tôi cần đặt bác sĩ tạ biên cương"
print(extractor.extract_person_name(text,'pattern'))

text = "trời hôm nay nhiều mây cực"
print(extractor.extract_person_name(text,'pattern'))
```
The expected output should be:
```
{'entities': [{'start': 11, 'end': 23, 'entity': 'person_name', 'value': 'Pham Hai Nam', 'confidence': 1.0, 'extractor': 'pattern'}]}
{'entities': [{'start': 19, 'end': 32, 'entity': 'person_name', 'value': 'Tạ Biên Cương', 'confidence': 1.0, 'extractor': 'pattern'}]}
{'entities': []}
```
Inference time :  
 - dictionary :  0.00015s
 - pattern :  0.00014s
 - dictionary + pattern :  0.00017s  
 
Ditionary Load Time :  22.21s  

**Extract Date** 
```
from vma_nlu.extractor import Extractor

extractor = Extractor()

text = "tôi muốn đặt lịch vào ngày 6 tháng 7"
extractor.extract_date(text)
# [('None', ['ngày 6 '], ['tháng 7'], 'None')]


text = "tôi sinh vào ngày 21-3-1997"
extractor.extract_date(text)
# [('Thứ 6', '21', '3', '1997')]
```
Inference time : 4.76e-07  
**Extract Time**
TBD

If you want to use dictionary-based:  
- Download dictionay `fullname.pkl` (5.4GB) in [here](
https://drive.google.com/drive/u/1/folders/1lilHx7coHnCFB-EZoCz32sIn-VEdiniG)  
- Then copy that file into `vma_nlu/data` and set load_dict=True when init Extractor class for using dictionary-based.  
- Minimum requirement : RAM >= 25 GB