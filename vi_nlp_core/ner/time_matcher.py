import datetime
import string
import re

from nltk import ngrams
from vi_nlp_core.utils.time_pattern import get_time_pattern
from vi_nlp_core.utils.preproces import Preprocess
from vi_nlp_core.utils.util import convert_time_to_timestamp
from vietnam_number import w2n


class TimeMatcher:
    def __init__(self):
        self.default_hour = -1
        self.default_min = -1
        self.left_shift = 3
        self.right_shift = 4

        self.max_n_grams = 3
        self.absolute_pattern, self.am_pattern, self.pm_pattern = get_time_pattern()

        self.preprocessor = Preprocess()

    def extract_time(self, text):
        text = self.preprocess(text)
        # text = self.preprocessor.preprocess(text)

        text = text.replace('tiếng', 'giờ')

        time_result = self.extract_absolute_time(text)
        if time_result[2] != self.default_hour and time_result[3] != self.default_min:
            return self.output_format_timestamp(time_result, 'absolute_pattern')
        else:
            time_result = self.extract_relative_time(text)
        return self.output_format_timestamp(time_result, 'relative_pattern')

    def extract_relative_time(self, text):
        hour = self.default_hour
        minute = self.default_min
        start = 0
        end = 0
        status = self.get_time_status(text)

        text = text.split(' ')

        if 'giờ' not in text:
            # Maybe it contains 'phut'
            if 'phút' in text or 'phut' in text:
                start, end, hour, minute = self.no_hour_case(text)
                hour, minute = self.refine_hour_minute(hour, minute, status)
                # should be round time
            return start, end, hour, minute

        hour_index = text.index('giờ')
        hour_range = text[max(0, hour_index - self.left_shift): hour_index]
        minute_range = text[hour_index +
                            1: min(hour_index + self.right_shift, len(text))]
        hour = self.get_hour(hour_range)
        minute = self.get_minute(minute_range)

        hour, minute = self.refine_hour_minute(hour, minute, status)
        hour, minute = self.round_hour_minute_to_base(hour, minute)

        start = len(' '.join(text[:hour_index-1]))
        if start != 0:
            start += 1
        if minute == 0:
            end = len(' '.join(text[:hour_index + 1]))
        else:
            end = len(' '.join(text[: hour_index + self.right_shift + 1]))
        return start, end, hour, minute

    def extract_absolute_time(self, text):
        status = self.get_time_status(text)
        hour = self.default_hour
        minute = self.default_min
        start = -1
        end = -1

        if 'giờ' in text.split(' '):
            return start, end, hour, minute

        absolute_pattern = self.absolute_pattern[0]
        times = [(x.group(), x.span())
                 for x in re.finditer(absolute_pattern, text)]
        if times:
            hours = []
            minutes = []
            starts = []
            ends = []
            for time in times:
                [hour, minute] = re.split('[:.hg]', time[0])
                if not re.search('\d', minute):
                    minute = 0
                (start, end) = time[1]
                hour, minute = self.refine_hour_minute(
                    hour, minute, self.get_time_status(text[start: start+10]))
                hour, minute = self.round_hour_minute_to_base(hour, minute)
                hours.append(hour)
                minutes.append(minute)
                starts.append(start)
                ends.append(end)
        # for pattern in self.absolute_pattern: #not have pattern 'giờ' in text
        #     # time = re.search(pattern, text)
        #     time = [(x.group(), x.span()) for x in re.finditer(pattern, text)]
        #     if time != None and time.group(1) != None:
        #         time = time.group(1)
        #         if '.' in time:
        #             hour, minute = time.split('.')
        #         elif ':' in time:
        #             hour, minute = time.split(':')
        #         elif 'h' in time:
        #             hour, minute = time.split('h')
        #         elif 'g' in time:
        #             hour, minute = time.split('g')
        #         else:
        #             hour = time
        #             minute = ''
        #         start = text.find(time)
        #         end = start + len(time) + 5
        #         break
        # # Case 9h -> minute = ''
        # if minute == '':
        #     minute = 0
        # hour, minute = self.refine_hour_minute(hour,minute,status)
        # hour, minute = self.round_hour_minute_to_base(hour,minute)

        return start, end, hour, minute

    def get_time_status(self, text, minunte_range=None):
        '''
        Return:
            result - tuple (A,B,C)
                A : am(0) or pm(1)
                B : kém(-1) or hơn(1)
                C : có nữa/tiếp theo/kế tiếp/lát/lát nữa không ? (0/1)
        '''
        c_pattern = ['nữa', 'tiếp theo', 'kế tiếp', 'lát', 'lát nữa', 'kế',
                     'sắp tới', 'phút sau', 'phút nữa', 'giờ rưỡi sau', 'giờ sau']
        # min_pattern = ['sau']
        result = [0, 0, 0]
        status = 'am'

        for pattern in self.am_pattern:
            if text.find(pattern) != -1:
                result[0] = 0  # 'am'
                break
        for pattern in self.pm_pattern:
            if text.find(pattern) != -1:
                result[0] = 1  # 'pm'
                break

        if text.find('kém') != -1 or text.find('thiếu') != -1:
            result[1] = -1
        elif text.find('hơn') != -1:
            result[1] = 1

        for pattern in c_pattern:
            if text.find(pattern) != -1:
                result[2] = 1  # yes

        return result

    def refine_hour_minute(self, hour, minute, status):
        try:
            hour = int(hour)
            minute = int(minute)
        except:
            return self.default_hour, self.default_min

        if hour != self.default_hour and minute == self.default_min:
            minute = 0
        # Check hour/minute is valid
        if hour == self.default_hour and minute == self.default_min:
            return hour, minute
        if status[0] == 1 and hour < 12:
            hour += 12

        if status[1] == -1:
            hour -= 1
            minute = 60 - int(minute)

        if status[2] == 1:
            now = datetime.datetime.now()
            hour = now.hour + int(hour)
            minute = now.minute + int(minute)

        if minute >= 60:
            minute -= 60
            hour += 1
        hour, minute = self.is_valid(hour, minute)
        return hour, minute

    def is_valid(self, hour, minute):
        if hour > 24 or hour < 0 or minute > 60 or minute < 0:
            return self.default_hour, self.default_min
        return hour, minute

    def get_hour(self, hour_range):
        # refine hour_range : padding punct
        hour_range = self.refine_hour_range(hour_range)

        if hour_range[-1].replace('h', '').replace('g', '').isdigit():
            return hour_range[-1].replace('h', '').replace('g', '')
        else:
            try:
                hour = w2n(' '.join(hour_range))
            except:
                hour = self.default_hour
            return hour

    def filter_minute_rage(self, minute_range):
        fil = [
            'ngày', 'phút', 'tháng', 'năm', 'buổi', 'thứ', 'chiều', 'sáng', 'trưa', 'tối', 'xế'
        ]
        for i in range(len(minute_range)):
            if minute_range[i] in fil:
                minute_range = minute_range[:i]
                return minute_range
        return minute_range

    def get_minute(self, minute_range):
        if minute_range == []:
            return 0
        minute_range = self.filter_minute_rage(minute_range)
        if minute_range == []:
            return 0
        elif minute_range[0].isdigit():
            return minute_range[0]
        elif minute_range[-1].isdigit():
            return minute_range[-1]
        elif 'rưỡi' in minute_range:
            return 30

        else:
            try:
                minute = w2n(' '.join(minute_range))
            except:
                minute = 0
            return minute

    def output_format(self, time_result, extractor):
        if time_result[2] == -1 or time_result[3] == -1:
            return {
                'entities': []
            }
        else:
            return {
                'entities': [{
                    'start': time_result[0],
                    'end': time_result[1],
                    'entity': 'time',
                    'value': (time_result[2], time_result[3]),
                    'confidence': 1.0,
                    'extractor': extractor
                }]
            }

    def output_format_timestamp(self, time_result, extractor):
        if time_result[2] == -1 or time_result[3] == -1:
            return {
                'entities': []
            }
        else:
            return {
                'entities': [{
                    'start': time_result[0],
                    'end': time_result[1],
                    'entity': 'time',
                    'value': convert_time_to_timestamp((time_result[2], time_result[3])),
                    'confidence': 1.0,
                    'extractor': extractor
                }]
            }

    def preprocess(self, text):
        text = text.replace('\n', '').strip()
        text = re.sub('(?<! )(?=[,!?()])|(?<=[,!?()])(?! )', r' ', text)
        return text

    def no_hour_case(self, text):  # list
        hour = self.default_hour
        minute = self.default_min
        start = 0
        end = 0
        for i in range(len(text)):
            if text[i] == 'phút' or text[i] == 'phut':
                minute = self.get_minute(text[max(0, i - self.left_shift):i])
                start = len(" ".join(text[:i-1]).strip())
                if start != 0:
                    start += 1
                end = len(" ".join(text[:i+1]).strip())
                hour = 0
                return start, end, hour, minute
        return start, end, hour, minute

    def refine_hour_range(self, hour_range):
        s = ' '.join(hour_range)
        s = s.translate(str.maketrans(
            {key: " {0} ".format(key) for key in string.punctuation}))
        hour_range = s.split(' ')
        return hour_range

    def round_minute_to_base(self, minute, base):
        '''
            return: a float rounded to the nearest 15min interval
            if base is 15 for example
        '''
        if minute in [0, 15, 30, 60]:
            return minute
        rounded = base * ((minute//base) + 1)

        return rounded

    def round_hour_minute_to_base(self, hour, minute, base=15):
        if hour == self.default_hour and minute == self.default_min:
            return hour, minute
        minute = self.round_minute_to_base(minute, base)
        if minute >= 60:
            minute -= 60
            hour += 1
        return hour, minute


if __name__ == '__main__':
    matcher = TimeMatcher()
    # text = '14:30 sáng thứ 7 tuần này'
    # print(matcher.extract_absolute_time(text))
    # text = '18:30 tiếng kém mười lăm'
    # print(matcher.extract_absolute_time(text))
    # text = 'ngày 7 tháng 6 lúc 14.15.00 giờ'
    # print(matcher.extract_absolute_time(text))

    text = 'tôi cần book lịch gấp vào 1 tiếng rưỡi sau'
    print(matcher.extract_relative_time(text))

    text = '4 tiếng sau họp tại trụ sở CA'
    print(matcher.extract_relative_time(text))
