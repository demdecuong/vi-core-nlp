import re
from datetime import date
import datetime
# from Preprocess import Preprocess

def format():
    format_date = ['(\d+(,|\s|\.|-|\/|_)+\d+(,|\s|\.|-|\/|_)+\d+)', # 21/03/1997  21-03-1997  21.03.1997
                    '((monday|tuesday|wednesday|thursday|friday|saturday|sunday)(,|\s|\.|-|\/|_)\d+(,|\s|\.|-|\/|_)*\d*(,|\s|\.|-|\/|_)*\d*)', # Monday 21 3 
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

        self.week_days=["Thứ 2","Thứ 3","Thứ 4","Thứ 5","Thứ 6","Thứ 7","Chủ nhật"]

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
            return  [(week, day, month, year)]
            #TODO  inference week day month year is None
        else:
            if result_format:
                list_date = [re.split('(,|\s|\.|-|\/|_)', x) for x in result_format]
                day = [x[0] for x in list_date]
                month = [x[2] for x in list_date]
                year = [x[4] for x in list_date]
                wod  = []
                for i in range(len(day)):
                    wod.append(self.week_days[datetime.date(int(year[i]), int(month[i]), int(day[i])).weekday()])
                return [(w, d, m, y) for w, d, m, y in zip(wod, day, month, year)]
            
            if result_non_format:
                # current_date = self._get_current_time()
                return result_non_format

    def _get_current_time(self):
        return str(date.today())
    
    def _map_non_format_to_date(self, result_non_format, current_time):
        current_year, current_month, current_day = current_time.split("-")
        current_time, current_month, current_day = int(current_year), int(current_month), int(current_day)

        for i in result_non_format:
            day = current_day
            month = current_month
            year = current_year
            if re.search("qua", i):
                if re.search("ngày", i) or re.search("hôm", i) or re.search("sáng", i) or re.search("trưa", i) or re.search("chiều", i) or re.search("tối", i):
                    day = str(datetime.date.today() - datetime.timedelta(days=1)).split("-")[2]
                elif re.search("tuần", i):
                    pass
            elif re.search("nay", i):
                pass
            elif re.search("mai", i) or re.search("tới", i) or re.search("sau"):
                pass
            elif re.search("kia", i):
                pass
            else:
                pass
            #TODO inference date for non_format