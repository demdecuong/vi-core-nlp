# NER/Intent classification for Vietnamese Appointment Chatbot

# Usage

**Extract Vietnamese phone number**

**Extract person name**
```
import vi_nlp_core
from vi_nlp_core.ner.extractor import Extractor
extractor = Extractor()

text = "tôi cần đặt bác sĩ tạ biên cương"
print(extractor.extract_person_name(text,'pattern'))
```

**Extract Date** 
```
import vi_nlp_core
from vi_nlp_core.ner.extractor import Extractor
extractor = Extractor()

text = "tôi sinh vào ngày 21-3-1997"
extractor.extract_date(text)
```

**Extract Time**
```
import vi_nlp_core
from vi_nlp_core.ner.extractor import Extractor
extractor = Extractor()

text = '14:50 ngày 7 tháng 6'
print(extractor.extract_time(text,return_value=True)) #return value only
```
