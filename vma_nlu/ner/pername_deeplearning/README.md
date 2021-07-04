# ViMQ

## Usage:

### Download pretrained [model](https://drive.google.com/file/d/1-9ycIeCBWLf1oiJ-4Kd8cUuDcYMeIMcL/view?usp=sharing) 

Config checkpoint path `config.py`

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
