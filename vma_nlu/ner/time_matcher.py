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
import datetime
import threading
import re

from nltk import ngrams
from vma_nlu.utils.pattern import get_time_pattern
from vietnam_number import w2n

class TimeMatcher:
    def __init__(self):
        self.default_hour = 0
        self.default_min = 0
        self.left_shift = 3
        self.right_shift = 4

        self.max_n_grams = 3
        self.absolute_pattern, self.am_pattern, self.pm_pattern = get_time_pattern()

    def extract_time(self, text):
        text = text.replace('tiếng','giờ')

        time_result = self.extract_absolute_time(text)
        if time_result[2] != 0 and time_result[3] != 0:
            return self.output_format(time_result,'absolute_pattern')
        else:
            time_result = self.extract_relative_time(text)        
        return self.output_format(time_result,'relative_pattern')

    def extract_relative_time(self, text):
        hour = self.default_hour
        minute = self.default_min
        start = 0
        end = 0
        status = self.get_time_status(text)
        try:
            text = text.split(' ')
            hour_index = text.index('giờ')
            hour_range = text[max(0, hour_index - self.left_shift): hour_index]
            minute_range = text[hour_index +
                                1: min(hour_index + self.right_shift, len(text))]

            hour = self.get_hour(hour_range)
            minute = self.get_minute(minute_range)

            hour, minute = self.refine_hour_minute(hour,minute,status)
            
            start = max(0, hour_index - self.left_shift)
            end = min(hour_index + self.right_shift, len(text))
            return start,end, hour, minute
        except:
            return start,end, hour, minute

     
    def extract_absolute_time(self, text):
        status = self.get_time_status(text)
        hour = self.default_hour
        minute = self.default_min
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
                elif 'h' in time:
                    hour, minute = time.split('h')
                elif 'g' in time:
                    hour, minute = time.split('g')
                start = text.find(time)
                end = start + len(time)
                break

        hour, minute = self.refine_hour_minute(hour,minute,status)

        return start, end, hour, minute

    def get_time_status(self, text):
        '''
        Return:
            result - tuple (A,B,C)
                A : am(0) or pm(1)
                B : kém(-1) or hơn(1)
                C : có nữa/tiếp theo/kế tiếp/lát/lát nữa không ? (0/1)
        '''
        c_pattern = ['nữa','tiếp theo','kế tiếp','lát','lát nữa','kế','sắp tới']
        result = [0,0,0]
        status = 'am'

        for pattern in self.am_pattern:
            if text.find(pattern) != -1:
                result[0] = 0 #'am'
                break
        for pattern in self.pm_pattern:
            if text.find(pattern) != -1:
                result[0] = 1 #'pm'
                break

        if text.find('kém') != -1:
            result[1] = -1
        elif text.find('hơn') != -1: 
            result[1] = 1

        for pattern in c_pattern:
            if text.find(pattern) != -1:
                result[2] = 1 #yes

        return result

    def refine_hour_minute(self,hour,minute,status):
        
        # Check hour/minute is valid
        if hour==0 and minute == 0:
            return hour, minute

        if status[0] == 1 and hour < 12:
            hour += 12
        
        if status[1] == -1:
            hour = int(hour)
            hour -= 1
            minute = 60 - int(minute)

        if status[2] == 1:
            now = datetime.datetime.now()
            hour = now.hour + int(hour)
            minute = now.minute + int(minute)
        return hour, minute

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
            
    def output_format(self,time_result,extractor):
        if time_result[0] == -1:
            return {
                'entities' : []
            }
        else:
            return {
                'entities':[{
                    'start' : time_result[0],
                    'end' : time_result[1],
                    'entity' : 'time',
                    'value' : (time_result[2],time_result[3]),
                    'confidence' : 1.0,
                    'extractor' : extractor
                }]
            }

        
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
    # text = 'ba tiếng nữa'
    # print(matcher.extract_relative_time(text))