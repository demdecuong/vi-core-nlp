import numpy as np
import pickle
import os

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(WORK_DIR, "weight/LR_model.pkl")

model = pickle.load(open(MODEL_PATH, 'rb'))

text = ["hi", "đặt lịch", "hủy lịch", "đổi lịch", "hủy", "bỏ đi", "dừng lại", "không cần nữa", "làm lại"]
predict = model.predict(text)
confidence = np.max(model.predict_proba(text)[0])
print(predict)
print(confidence)