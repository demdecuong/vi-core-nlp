'''
tám giờ rưỡi
tám giờ ba mươi phút
tám ba mươi phút

mười bốn giờ
tám giờ kém mười lăm
tám giờ kém 15
8 giờ kém 15

2 tiếng nữa
'''

'''
[VALUE1] [giờ|tiếng] [kém|nữa] [VALUE2]

VALUE1 : 3 ITEM
(?:một|hai|ba|bốn|tư|tứ|năm|sáu|bảy|tám|chín|mười|mươi|mốt) (?:một|hai|ba|bốn|tư|tứ|năm|sáu|bảy|tám|chín|mười|mươi|mốt) (?:một|hai|ba|bốn|tư|tứ|năm|sáu|bảy|tám|chín|mười|mươi|mốt)(?= giờ|tiếng)
VALUE1 : 2 ITEM
(?:một|hai|ba|bốn|tư|tứ|năm|sáu|bảy|tám|chín|mười|mươi|mốt) (?:một|hai|ba|bốn|tư|tứ|năm|sáu|bảy|tám|chín|mười|mươi|mốt)(?= giờ|tiếng)
VALUE1 : 1 ITEM
(?:một|hai|ba|bốn|tư|tứ|năm|sáu|bảy|tám|chín|mười|mươi|mốt)(?= giờ|tiếng)
'''

import re

class TimeConvertor:
    def __init__(self):
        self.default_hour = 0
        self.default_min = 0
        self.left_shift = 3
        self.right_shift = 4

        self.max_n_grams = 3 

    def extract_time(self,text):
        hour = self.default_hour
        minute = self.default_min
        text = text.split(' ')
        hour_index = text.index('giờ')

        hour_range = text[max(0,hour_index - self.left_shift): hour_index]

        minute_range = text[hour_index + 1: min(hour_index + self.right_shift, len(text))]
        

    def time2text(self,text):  
        pass

    def text2time(self,text):
        pass