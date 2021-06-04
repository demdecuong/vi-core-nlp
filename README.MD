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