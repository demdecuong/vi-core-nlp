import numpy as np
import pickle
import os
import re

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(WORK_DIR, "weight/LR_model.pkl")

model = pickle.load(open(MODEL_PATH, 'rb'))

def normalize_text(s):
    s = re.sub(r'([a-z])\1+', lambda m: m.group(1), s, flags=re.IGNORECASE)
    s = re.sub(r'([a-z][a-z])\1+', lambda m: m.group(1), s, flags=re.IGNORECASE)
    return s
text = ["hi", normalize_text("đặt lịchhhhh"), "hủy lịch", "đổi lịch", "hủy", "bỏ đi", "dừng lại", "không cần nữa", "làm lại"]
predict = model.predict(text)
confidence = np.max(model.predict_proba(text)[0])
print(predict)
print(confidence)