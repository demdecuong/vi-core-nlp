import re
from datetime import date
import datetime
# from src.utils.Preprocess import Preprocess

def format():
    format_date = ['(\d+(,|\s|\.|-|\/|_)+\d+(,|\s|\.|-|\/|_)+\d+)', # 21/03/1997  21-03-1997  21.03.1997
                    '((monday|tuesday|wednesday|thursday|friday|saturday|sunday)(,|\s|\.|-|\/|_)\d+(,|\s|\.|-|\/|_)*\d*(,|\s|\.|-|\/|_)*\d*)', # Monday 21 3 
                    ] 
    wod = ['(monday|tuesday|wednesday|friday|saturday|sunday)']
    wod_vn = ['(thứ(\s+|\.+)*[2-8])|(thuws(\s+|\.+)*[2-8])|(thu(\s+|\.+)*[2-8])|(thứ(\s+|\.+)*(hai|ba|tư|tu|bốn|bon|năm|nam|lăm|lam|sáu|say|bảy|bay|chủ nhật|chu nhat|cn))']

    day_vn = ['(ngày(\s+|\.+)*(\d\d|\d)($|\s))|(ngay(\s+|\.+)*(\d\d|\d)($|\s))|(ngafy(\s+|\.+)*(\d\d|\d)($|\s))']

    month = ['(january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|october|oct|november|nov|december|dec)']
    month_vn = ['(tháng(\s+|\.+)*(\d\d|\d)($|\s))|(thang(\s+|\.+)*(\d\d|\d)($|\s))|(thasng(\s+|\.+)*(\d\d|\d)($|\s))|(((tháng)|(thang))(\s+|\.+)*(một|mot|hai|ba|bốn|bon|tư|tu|năm|nam|lăm|lam|sáu|bảy|bay|tám|tam|chín|chin|mười|muoi|mười một|muoi mot|mười hai|muoi hai|giêng|gieng|chạp|chap))']

    year = ['('+'|'.join([str(i) for i in list(range(1900, 2050))])+')']

    return format_date, wod, wod_vn, day_vn, month, month_vn, year

def non_format():
    short_time = ['(ngày\s(hôm\s)*qua)|(sáng\s(hôm\s)*qua)|(trưa\s(hôm\s)*qua)|(chiều\s(hôm\s)*qua)|(tối\s(hôm\s)*qua)|(ngày\s(hôm\s)*nay)|(sáng\s(hôm\s)*nay)|(trưa\s(hôm\s)*nay)|(chiều\s(hôm\s)*nay)|(tối\s(hôm\s)*nay)|(ngày\s(hôm\s)*mai)|(sáng\s(hôm\s)*mai)|(trưa\s(hôm\s)*mai)|(chiều\s(hôm\s)*mai)|(tối\s(hôm\s)*mai)|(ngày\s(hôm\s)*mốt)|(sáng\s(hôm\s)*mốt)|(trưa\s(hôm\s)*mốt)|(chiều\s(hôm\s)*mốt)|(tối\s(hôm\s)*mốt)|(ngày\s(hôm\s)*kia)|(sáng\s(hôm\s)*kia)|(trưa\s(hôm\s)*kia)|(chiều\s(hôm\s)*kia)|(tối\s(hôm\s)*kia)|(buổi\ssáng)|(buổi\strưa)|(buổi\schiều)|(buổi\stối)']

    long_time = ['(tuần\snày)|(tuần\ssau)|(tuần\squa)|(tuần\stới)|(tháng\snày)|(tháng\ssau)|(tháng\squa)|(tháng\stới)']
    
    return short_time, long_time


class PatternMatching(object):
    def __init__(self) -> None:
        super().__init__()

        self.format_date, self.wod, self.wod_vn, self.day_vn, self.month, self.month_vn, self.year = format()
        self.format_date = "|".join([x for x in self.format_date])

        self.wod = "|".join([self.wod[0], self.wod_vn[0]])
        self.day = self.day_vn[0]
        self.month = "|".join([self.month[0], self.month_vn[0]])
        self.year = self.year[0]

        self.short_time, self.long_time = non_format()
        self.non_format = "|".join([self.short_time[0], self.long_time[0]])

        self.week_days=["Thứ 2","Thứ 3","Thứ 4","Thứ 5","Thứ 6","Thứ 7","Chủ nhật"]

        # self.pre_process = Preprocess()

    def extract_date(self, text):
        # text = self.pre_process.preprocess(text)
        result_non_format = [x.group() for x in re.finditer(self.non_format, text)]
        result_format = [x.group() for x in re.finditer(self.format_date, text)]

        if not result_non_format and not result_format:
            wod = [x.group() for x in re.finditer(self.wod, text)]
            day = [x.group() for x in re.finditer(self.day, text)]
            month = [x.group() for x in re.finditer(self.month, text)]
            year = [x.group() for x in re.finditer(self.year, text)]
            tmp = max(len(wod), len(day), len(month), len(year))
            if tmp == 0:
                return "Invalid"
            if not wod:
                wod = ["None"]*tmp
            if not day:
                day = ["None"]*tmp
            if not month:
                month = ["None"]*tmp
            if not year:
                year = ["None"]*tmp
            return  [(w, d, m, y) for w, d, m, y in zip(wod, day, month, year)]
            #TODO  inference week day month year is None
        else:
            result = []
            if result_format:
                list_date = [re.split('(,|\s|\.|-|\/|_)', x) for x in result_format]
                day = [x[0] for x in list_date]
                month = [x[2] for x in list_date]
                year = [x[4] for x in list_date]
                wod  = []
                for i in range(len(day)):
                    wod.append(self.week_days[datetime.date(int(year[i]), int(month[i]), int(day[i])).weekday()])
                result.extend([(w, d, m, y) for w, d, m, y in zip(wod, day, month, year)])
            if result_non_format:
                result.extend(self._map_non_format_to_date(result_non_format=result_non_format))
            return result

    def _get_day(self, timedelta, mode = "sub"):
        if mode == "add":
            return str(date.today() + datetime.timedelta(days=timedelta))
        elif mode == "sub":
            return str(date.today() - datetime.timedelta(days=timedelta))
    
    def _map_non_format_to_date(self, result_non_format):
        result = []
        for i in result_non_format:
            if re.search("qua", i):
                if re.search("(ngày)|(ngay)|(ngayf)", i) or re.search("(hôm)|(hom)", i) or re.search("(sáng)|(sang)", i) or re.search("(trưa)|(trua)", i) or re.search("(chiều)|(chieu)", i) or re.search("(tối)|(toi)", i):
                    get_date = self._get_day(1, mode="sub").split("-")
                    day = get_date[2]
                    month = get_date[1]
                    year = get_date[0]
                    wod = self.week_days[datetime.date(int(year), int(month), int(day)).weekday()]
                elif re.search("(tuần)|(tuan)", i):
                    get_date = self._get_day(7, mode="sub").split("-")
                    day = get_date[2]
                    month = get_date[1]
                    year = get_date[0]
                    wod = self.week_days[datetime.date(int(year), int(month), int(day)).weekday()]
                elif re.search("(tháng)|(thang)", i):
                    get_date = self._get_day(30, mode="sub").split("-")
                    day = get_date[2]
                    month = get_date[1]
                    year = get_date[0]
                    wod = self.week_days[datetime.date(int(year), int(month), int(day)).weekday()]
            elif re.search("(này)|(nay)", i):
                get_date = self._get_day(0).split("-")
                day = get_date[2]
                month = get_date[1]
                year = get_date[0]
                wod = self.week_days[datetime.date(int(year), int(month), int(day)).weekday()]
            elif re.search("mai", i) or re.search("tới", i) or re.search("sau", i):
                if re.search("(ngày)|(ngay)|(ngayf)", i) or re.search("(hôm)|(hom)", i) or re.search("(sáng)|(sang)", i) or re.search("(trưa)|(trua)", i) or re.search("(chiều)|(chieu)", i) or re.search("(tối)|(toi)", i):
                    get_date = self._get_day(1, mode="add").split("-")
                    day = get_date[2]
                    month = get_date[1]
                    year = get_date[0]
                    wod = self.week_days[datetime.date(int(year), int(month), int(day)).weekday()]
                elif re.search("(tuần)|(tuan)", i):
                    get_date = self._get_day(7, mode="add").split("-")
                    day = get_date[2]
                    month = get_date[1]
                    year = get_date[0]
                    wod = self.week_days[datetime.date(int(year), int(month), int(day)).weekday()]
                elif re.search("(tháng)|(thang)", i):
                    get_date = self._get_day(30, mode="add").split("-")
                    day = get_date[2]
                    month = get_date[1]
                    year = get_date[0]
                    wod = self.week_days[datetime.date(int(year), int(month), int(day)).weekday()]
            elif re.search("kia", i):
                get_date = self._get_day(2).split("-")
                day = get_date[2]
                month = get_date[1]
                year = get_date[0]
                wod = self.week_days[datetime.date(int(year), int(month), int(day)).weekday()]
            result.append((wod, day, month, year))
        return result
            #TODO inference date for non_format