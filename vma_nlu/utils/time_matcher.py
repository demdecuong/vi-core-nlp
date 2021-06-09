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
from pattern import get_time_pattern
from vietnam_number import w2n

class TimeMatcher:
    def __init__(self):
        self.default_hour = 0
        self.default_min = 0
        self.left_shift = 2
        self.right_shift = 4

        self.max_n_grams = 3
        self.absolute_pattern, self.am_pattern, self.pm_pattern = get_time_pattern()

    def extract_time(self, text):
        t1 = threading.Thread(target=extract_relative_time, args=(text,))
        t2 = threading.Thread(target=extract_absolute_time, args=(text,))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        print('Done')

    def extract_relative_time(self, text):
        hour = self.default_hour
        minute = self.default_min
        text = text.split(' ')
        hour_index = text.index('giờ')
        hour_range = text[max(0, hour_index - self.left_shift): hour_index]
        minute_range = text[hour_index +
                            1: min(hour_index + self.right_shift, len(text))]

        hour = self.get_hour(hour_range)
        print(hour,minute_range)
        # minute = self.get_minute(minute_range)


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
                hour = 0
            return hour

    def filter_minute_rage(self,minute_range):
        fil = [
            'ngày','phút','tháng','năm','buổi'
        ]
        # for token

    def get_minute(self,minute_range):
        pass

    def time2text(self, text):
        pass

    def text2time(self, text):
        pass


if __name__ == '__main__':
    matcher = TimeMatcher()
    text = '14:30 sáng thứ 7 tuần này'
    print(matcher.extract_absolute_time(text))
    text = '18:30 tiếng kém mười lăm'
    print(matcher.extract_absolute_time(text))
    text = 'ngày 7 tháng 6 lúc 14.15.00 giờ'
    print(matcher.extract_absolute_time(text))
    
    text = 'lúc 14 giờ 30 ngày 7 tháng 6'
    print(matcher.extract_relative_time(text))

    text = 'mười bốn giờ 30 phút ngày 7 tháng 6'
    print(matcher.extract_relative_time(text))

    text = 'bống bẩy giờ 30 phút ngày 7 tháng 6'
    print(matcher.extract_relative_time(text))

    text = 'sáu giờ 30 phút nữa ngày 7 tháng 6'
    print(matcher.extract_relative_time(text))

    text = 'hôm nay lúc tám giờ kém mười lăm'
    print(matcher.extract_relative_time(text))