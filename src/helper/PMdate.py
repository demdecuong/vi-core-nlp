import re
from Preprocess import Preprocess

def format():
    format_date = ['(\d+(-|_|\/|\.)+\d+(-|_|\/|\.)+\d+)', # 21/03/1997  21-03-1997  21.03.1997
                    '((monday|tuesday|wednesday|thursday|friday|saturday|sunday)(,|\s|\.|-|\/)\d+(,|\s|\.|-|\/)*\d*(,|\s|\.|-|\/)*\d*)', # Monday 21 3 
                    ] 
    week = ['(monday|tuesday|wednesday|friday|saturday|sunday)']
    week_vn = ['(thứ(\s+|\.+)[2-8])|(thứ(\s+|\.+)(hai|ba|tư|bốn|năm|lăm|sáu|bảy|chủ nhật|cn))']

    day_vn = ['(ngày(\s+|\.+)(\d\d|\d)($|\s))']

    month = ['(January|February|March|April|May|June|July|August|September|October|November|December)']
    month_vn = ['(tháng(\s+|\.+)(\d\d|\d)($|\s))|(tháng(\s+|\.+)(một|hai|ba|bốn|tư|năm|lăm|sáu|bảy|tám|chín|mười|mười một|mười hai|giêng|chạp))']

    year = ['('+'|'.join([str(i) for i in list(range(1900, 2050))])+')']

    return format_date, week, week_vn, day_vn, month, month_vn, year

def non_format():
    short_time = ['(ngày\s(hôm\s)*qua)|(sáng\s(hôm\s)*qua)|(trưa\s(hôm\s)*qua)|(chiều\s(hôm\s)*qua)|(tối\s(hôm\s)*qua)|(ngày\s(hôm\s)*nay)|(sáng\s(hôm\s)*nay)|(trưa\s(hôm\s)*nay)|(chiều\s(hôm\s)*nay)|(tối\s(hôm\s)*nay)|(ngày\s(hôm\s)*mai)|(sáng\s(hôm\s)*mai)|(trưa\s(hôm\s)*mai)|(chiều\s(hôm\s)*mai)|(tối\s(hôm\s)*mai)|(ngày\s(hôm\s)*mốt)|(sáng\s(hôm\s)*mốt)|(trưa\s(hôm\s)*mốt)|(chiều\s(hôm\s)*mốt)|(tối\s(hôm\s)*mốt)|(ngày\s(hôm\s)*kia)|(sáng\s(hôm\s)*kia)|(trưa\s(hôm\s)*kia)|(chiều\s(hôm\s)*kia)|(tối\s(hôm\s)*kia)|(buổi\ssáng)|(buổi\strưa)|(buổi\schiều)|(buổi\stối)']

    long_time = ['(tuần\snày)|(tuần\ssau)|(tuần\squa)|(tuần\stới)|(tháng\snày)|(tháng\ssau)|(tháng\squa)|(tháng\stới)']
    
    return short_time, long_time


class PatternMatching(object):
    def __init__(self) -> None:
        super().__init__()

        self.format_date, self.week, self.week_vn, self.day_vn, self.month, self.month_vn, self.year = format()
        self.format_date = "|".join([x for x in self.format_date])

        self.week = "|".join([self.week[0], self.week_vn[0]])
        self.day = self.day_vn[0]
        self.month = "|".join([self.month[0], self.month_vn[0]])
        self.year = self.year[0]

        self.short_time, self.long_time = non_format()
        self.non_format = "|".join([self.short_time[0], self.long_time[0]])


        # pre_process = Preprocess()
    def extract_date(self, text):
        # text = pre_process.preprocess(text)
        result_non_format = [x.group() for x in re.finditer(self.non_format, text)]
        result_format = [x.group() for x in re.finditer(self.format_date, text)]
        if not result_non_format and not result_format:
            week = [x.group() for x in re.finditer(self.week, text)]
            day = [x.group() for x in re.finditer(self.day, text)]
            month = [x.group() for x in re.finditer(self.month, text)]
            year = [x.group() for x in re.finditer(self.year, text)]
            if not week:
                week = "None"
            if not day:
                day = "None"
            if not month:
                month = "None"
            if not year:
                year = "None"
            if week == "None" and day == "None" and month == "None" and year == "None":
                return "Invalid"
            return  (week, day, month, year)
        else:
            result_non_format.extend(result_format)
            #parse format date

            return {
                "not_fotmat": result_non_format
                }
