# Installation
```
pip install -r requirement.txt
```
# Usage

**Extract Vietnamese phone number**
```
from src.extractor import Extractor

extractor = Extractor()
text = "sdt : 0349933957 ok chua"

print(extractor.extract_phone_num(text))
# 0349933957
```

**Extract person name**
```
from src.extractor import Extractor

extractor = Extractor()
text = "tôi tên là pham hai nam"

print(extractor.extract_person_name(text,'pattern'))
# pham hai nam
```

**Extract Date**
TBD

**Extract Time**
TBD

If you want to use dictionary-based:  
- Download dictionay `fullname.pkl` (5.4GB) in [here](
https://drive.google.com/drive/u/1/folders/1lilHx7coHnCFB-EZoCz32sIn-VEdiniG)  
- Then copy that file into `src/data` and remove comment line in constructor of Extractor class.  
- Minimum requirement : RAM >= 25 GB