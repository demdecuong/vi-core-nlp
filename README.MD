# Installtion

# Usage

**Extract Vietnamese phone number**
```
from src.extractor import Extractor

extractor = Extractor()
text = "sdt : 0349933957 ok chua"

print(extractor.extract_phone_num(text))
# 0349933957
```

**Extract date**
```
from helper.PMdate import PatternMatching

extractor = PatternMatching()
text = "tôi muốn đặt lịch vào ngày mai"

print(extractor.extract_date(text))
# ngày mai

text = "tôi muốn sinh vào ngày 21-03-1997"
print(extractor.extract_date(text))
# 21-03-1997
```