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

import threading
import re

from nltk import ngrams
from vma_nlu.utils.pattern import get_time_pattern
from vietnam_number import w2n

class TimeMatcher:
    def __init__(self):
        self.default_hour = 8
        self.default_min = 30
        self.left_shift = 3
        self.right_shift = 4

        self.max_n_grams = 3
        self.absolute_pattern, self.am_pattern, self.pm_pattern = get_time_pattern()

    def extract_time(self, text):
        text = text.replace('tiếng','giờ')
        if text.find('giờ') != -1:
            time_result = self.extract_relative_time(text)
        else:
            time_result = self.extract_absolute_time(text)
        return time_result

    def extract_relative_time(self, text):
        hour = self.default_hour
        minute = self.default_min

        status = self.get_time_status(text)
        
        text = text.split(' ')
        hour_index = text.index('giờ')
        hour_range = text[max(0, hour_index - self.left_shift): hour_index]
        minute_range = text[hour_index +
                            1: min(hour_index + self.right_shift, len(text))]

        hour = self.get_hour(hour_range)
        minute = self.get_minute(minute_range)

        if status == 'pm' and hour < 12:
            hour += 12

        if 'kém' in minute_range:
            hour -= 1
            minute = 60 - minute
        # elif 'nữa' in minute_range:

        start = max(0, hour_index - self.left_shift)
        end = min(hour_index + self.right_shift, len(text))
        
        if start != -1:
            return {
                'entities': [
                    {
                        "start": start,
                        "end": end,
                        "entity": "time",
                        "value": (hour, minute),
                        "confidence": 1.0,
                        "extractor": 'relative_pattern'
                    }]
                }
        else:
            return {
                'entities': []
            }
     
    def extract_absolute_time(self, text):
        hour = self.default_hour
        minute = self.default_min
        status = None
        start = -1
        end = -1

        for pattern in self.absolute_pattern:
            time = re.search(pattern, text)
            if time != None and time.group(1) != None:
                time = time.group(1)
                if '.' in time: 
                    hour, minute = time.split('.')
                elif ':' in time:
                    hour, minute = time.split(':')
                start = text.find(time)
                end = start + len(time)
                break
        # Get status and edit hour
        status = self.get_time_status(text)
        if status == 'pm' and hour < 12:
            hour += 12
        if start != -1:
            return {
                'entities': [
                    {
                        "start": start,
                        "end": end,
                        "entity": "time",
                        "value": (hour, minute),
                        "confidence": 1.0,
                        "extractor": 'absoulte_pattern'
                    }]
                }

        else:
            return {
                'entities': []
            }

    def get_time_status(self, text):
        status = None
        for pattern in self.am_pattern:
            if text.find(pattern) != -1:
                status = 'am'
        if status != None:
            return status
        for pattern in self.pm_pattern:
            if text.find(pattern) != -1:
                status = 'pm'
        if status != None:
            return status
        else:
            return 'Invalid'

    def get_hour(self,hour_range):
        if hour_range[-1].isdigit():
            return hour_range[-1]
        else:
            try:
                hour = w2n(' '.join(hour_range))
            except:
                hour = self.default_hour
            return hour

    def filter_minute_rage(self,minute_range):
        fil = [
            'ngày','phút','tháng','năm','buổi'
        ]
        for i in range(len(minute_range)):
            if minute_range[i] in fil:
                minute_range = minute_range[i-1:]
                return minute_range
        return minute_range
        
    def get_minute(self,minute_range):
        minute_range = self.filter_minute_rage(minute_range)
        if minute_range[0].isdigit():
            return minute_range[0]
        elif 'rưỡi' in minute_range:
            return 30
        else:
            try:
                minute = w2n(' '.join(minute_range))
            except:
                minute = self.default_min
            return minute
            


if __name__ == '__main__':
    matcher = TimeMatcher()
    # text = '14:30 sáng thứ 7 tuần này'
    # print(matcher.extract_absolute_time(text))
    # text = '18:30 tiếng kém mười lăm'
    # print(matcher.extract_absolute_time(text))
    # text = 'ngày 7 tháng 6 lúc 14.15.00 giờ'
    # print(matcher.extract_absolute_time(text))
    
    text = 'lúc 14 giờ 30 ngày 7 tháng 6'
    print(matcher.extract_relative_time(text))

    text = 'mười bốn giờ 30 phút ngày 7 tháng 6'
    print(matcher.extract_relative_time(text))

    text = 'hai mươi ba giờ 30 phút ngày 7 tháng 6'
    print(matcher.extract_relative_time(text))

    text = 'sáu giờ ba mươi phút nữa ngày 7 tháng 6'
    print(matcher.extract_relative_time(text))

    text = 'bảy giờ rưỡi phút nữa ngày 7 tháng 6'
    print(matcher.extract_relative_time(text))

    text = 'hôm nay lúc tám giờ kém mười lăm'
    print(matcher.extract_relative_time(text))

    text = 'bây giờ nên làm gì'
    print(matcher.extract_relative_time(text))

    # text = 'bảy rưỡi mùng 10 tháng 3'
    # print(matcher.extract_relative_time(text))