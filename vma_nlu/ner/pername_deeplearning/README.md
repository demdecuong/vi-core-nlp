# ViMQ

## Usage:

### Tải [model](https://drive.google.com/drive/folders/1T3DzH4wluKwbLvNwzj-yujx-jxdLMU4q?usp=sharing) và một vài file cần thiết cho model. Lưu trữ tại thư mục `vma_nlu/data/`


### Training model 
```
!python main.py
```

### Inference
```
from vma_nlu.ner.extractor import Extractor

extractor = Extractor()
extractor.extract_name_deep_learning('tôi là trần hoàng vũ muốn gặp bác  Huy')

```
