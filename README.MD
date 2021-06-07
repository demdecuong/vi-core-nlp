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
from src.extractor import Extractor

extractor = Extractor()

text = "tôi muốn đặt lịch vào ngày 6 tháng 7"
extractor.extract_date(text)
# [('None', ['ngày 6 '], ['tháng 7'], 'None')]


text = "tôi sinh vào ngày 21-3-1997"
extractor.extract_date(text)
# [('Thứ 6', '21', '3', '1997')]
```

## TODO predict date if missing 