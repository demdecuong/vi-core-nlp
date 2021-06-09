import re
from datetime import date
import datetime
from vma_nlu.utils.pattern import get_date_absolute, get_date_relative
# from Preprocess import Preprocess


class PatternMatching(object):
    def __init__(self) -> None:
        super().__init__()

        self.format_date, self.wod, self.wod_vn, self.day_vn, self.month, self.month_vn, self.year = get_date_absolute()
        self.format_date = "|".join([x for x in self.format_date])

        self.wod = "|".join([self.wod[0], self.wod_vn[0]])
        self.day = self.day_vn[0]
        self.month = "|".join([self.month[0], self.month_vn[0]])
        self.year = self.year[0]

        self.short_time, self.long_time, self.semi_format = get_date_relative()
        self.semi_format = self.semi_format[0]
        self.non_format = "|".join([self.short_time[0], self.long_time[0]])

        self.week_days=["Thứ 2","Thứ 3","Thứ 4","Thứ 5","Thứ 6","Thứ 7","Chủ nhật"]



    def extract_date(self, text):
        text = text.lower()

        result_non_format = [x.group() for x in re.finditer(self.non_format, text)]
        result_format = [x.group() for x in re.finditer(self.format_date, text)]

        if not result_non_format and not result_format:
            result = []
            semi_format = [x.group() for x in re.finditer(self.semi_format, text)]
            if semi_format:
                year = datetime.date.today().year
                year = [year] * len(semi_format)
                list_date = [re.split('(,|\s|\.|-|\/|_)', x) for x in semi_format]
                day = [x[0] for x in list_date]
                month = [x[2] for x in list_date]
                wod  = []
                for i in range(len(day)):
                    wod.append(self.week_days[datetime.date(int(year[i]), int(month[i]), int(day[i])).weekday()])
                result.extend([(w, d, m, y) for w, d, m, y in zip(wod, day, month, year)])
            else:
                wod = [x.group() for x in re.finditer(self.wod, text)]
                day = [x.group() for x in re.finditer(self.day, text)]
                month = [x.group() for x in re.finditer(self.month, text)]
                year = [x.group() for x in re.finditer(self.year, text)]
                tmp = max(len(wod), len(day), len(month), len(year))
                if tmp == 0:
                    return "Invalid"
                if not day:
                    day = ['None'] * tmp
                else:
                    try:
                        day = [re.search("\d+", x).group() for x in day]
                    except:
                        day = day
                if not month:
                    month = ['None'] * tmp
                else:
                    try:
                        month = [re.search("\d+", x).group() for x in month]
                    except:
                        month = [re.search("(một)|(mot)|(hai)|(ba)|(bốn)|(bon)|(tư)|(tu)|(năm)|(nam)|(lăm)|(lam)|(sáu)|(bảy)|(bay)|(tám)|(tam)|(chín)|(chin)|(mười)|(muoi)|(mười một)|(muoi mot)|(mười hai)|(muoi hai)|(giêng)|(gieng)|(chạp)|(chap)", x).group() for x in month]
                if not year:
                    year = ['None'] * tmp
                else:
                    year = [re.search("\d+", x).group() for x in year]
                if not wod:
                    try:
                        wod = [self.week_days[datetime.date(int(year[i]), int(month[i]), int(day[i])).weekday()] for i in range(tmp)]
                    except:
                        wod = ["None"] * tmp
                result.extend([(w, d, m, y) for w, d, m, y in zip(wod, day, month, year)])
                #TODO  inference week day month year is None
            return result

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

            if result_non_format: # result_non_format = ['ngày mai', 'tháng này', ... ]
                result.extend(self._map_non_format_to_date(result_non_format=result_non_format))

            return result

    def _map_non_format_to_date(self, result_non_format):

        results = []
        for i in result_non_format:
            if re.search("qua", i):
                
                if re.search("(ngày)|(ngay)|(ngayf)", i) or re.search("(hôm)|(hom)", i) or re.search("(sáng)|(sang)", i) or re.search("(trưa)|(trua)", i) or re.search("(chiều)|(chieu)", i) or re.search("(tối)|(toi)", i):
                    get_date = self._get_day(timedelta=1, mode="sub")
                    day = [get_date[2]]
                    month = [get_date[1]]
                    year = [get_date[0]]
                    wod = [self.week_days[datetime.date(int(year[i]), int(month[i]), int(day[i])).weekday()] for i in range(len(day))]
                    result = [(w, d, m, y) for w, d, m ,y in zip(wod, day, month, year)]
                
                elif re.search("(tuần)|(tuan)", i):
                    result = self._get_week(mode="sub")

                elif re.search("(tháng)|(thang)", i):
                    get_date = self._get_month("sub")
                    day = get_date[2]
                    month = get_date[1]
                    year = get_date[0]
                    wod = [self.week_days[datetime.date(int(year[i]), int(month[i]), int(day[i])).weekday()] for i in range(len(day))]
                    result = [(w, d, m, y) for w, d, m ,y in zip(wod, day, month, year)]
            
            elif re.search("(này)|(nay)", i):

                if re.search("(ngày)|(ngay)|(ngayf)", i) or re.search("(hôm)|(hom)", i) or re.search("(sáng)|(sang)", i) or re.search("(trưa)|(trua)", i) or re.search("(chiều)|(chieu)", i) or re.search("(tối)|(toi)", i):
                    get_date = self._get_day(timedelta=0, mode="add")
                    day = [get_date[2]]
                    month = [get_date[1]]
                    year = [get_date[0]]
                    wod = [self.week_days[datetime.date(int(year[i]), int(month[i]), int(day[i])).weekday()] for i in range(len(day))]
                    result = [(w, d, m, y) for w, d, m ,y in zip(wod, day, month, year)]

                elif re.search("(tuần)|(tuan)", i):
                    today = datetime.date.today()
                    weekday = today.weekday()
                    result = []
                    for i in range(7-int(weekday)):
                        get_date = self._get_day(timedelta=i, mode="add")
                        day = [get_date[2]]
                        month = [get_date[1]]
                        year = [get_date[0]]
                        wod = [self.week_days[datetime.date(int(year[i]), int(month[i]), int(day[i])).weekday()] for i in range(len(day))]
                        result.extend([(w, d, m, y) for w, d, m ,y in zip(wod, day, month, year)])

                elif re.search("(tháng)|(thang)", i):
                    get_date = self._get_month("current")
                    day = get_date[2]
                    month = get_date[1]
                    year = get_date[0]
                    wod = [self.week_days[datetime.date(int(year[i]), int(month[i]), int(day[i])).weekday()] for i in range(len(day))]
                    result = [(w, d, m, y) for w, d, m ,y in zip(wod, day, month, year)]
            
            elif re.search("mai", i) or re.search("tới", i) or re.search("sau", i):
                
                if re.search("(ngày)|(ngay)|(ngayf)", i) or re.search("(hôm)|(hom)", i) or re.search("(sáng)|(sang)", i) or re.search("(trưa)|(trua)", i) or re.search("(chiều)|(chieu)", i) or re.search("(tối)|(toi)", i):
                    get_date = self._get_day(timedelta=1, mode="add")
                    day = [get_date[2]]
                    month = [get_date[1]]
                    year = [get_date[0]]
                    wod = [self.week_days[datetime.date(int(year[i]), int(month[i]), int(day[i])).weekday()] for i in range(len(day))]
                    result = [(w, d, m, y) for w, d, m ,y in zip(wod, day, month, year)]

                elif re.search("(tuần)|(tuan)", i):
                    result = self._get_week(mode="add")

                elif re.search("(tháng)|(thang)", i):
                    get_date = self._get_month("add")
                    day = get_date[2]
                    month = get_date[1]
                    year = get_date[0]
                    wod = [self.week_days[datetime.date(int(year[i]), int(month[i]), int(day[i])).weekday()] for i in range(len(day))]
                    result = [(w, d, m, y) for w, d, m ,y in zip(wod, day, month, year)]

            elif re.search("mốt", i):
                get_date = self._get_day(timedelta=2, mode="add")
                day = [get_date[2]]
                month = [get_date[1]]
                year = [get_date[0]]
                wod = [self.week_days[datetime.date(int(year[i]), int(month[i]), int(day[i])).weekday()] for i in range(len(day))]
                result = [(w, d, m, y) for w, d, m ,y in zip(wod, day, month, year)]

            elif re.search("kia", i):
                get_date = self._get_day(timedelta=3, mode="add")
                day = [get_date[2]]
                month = [get_date[1]]
                year = [get_date[0]]
                wod = [self.week_days[datetime.date(int(year[i]), int(month[i]), int(day[i])).weekday()] for i in range(len(day))]
                result = [(w, d, m, y) for w, d, m ,y in zip(wod, day, month, year)]

            results.extend(result)
        return results


    def _get_month(self, mode):
        today = datetime.date.today()
        month = int(str(today).split("-")[1])
        year = int(str(today).split("-")[0])
        curr_day = int(str(today).split("-")[2])
        if mode == "add":
            month += 1
            if month in [1, 3, 5, 7, 8, 10, 12]:
                day = list(range(1, 32))
            elif month in [4, 6, 9, 11]:
                day = list(range(1,31))
            else: day = list(range(1, 29))
            month = [month]*len(day)
            year = [year]*len(day)
            return [year, month, day]
        elif mode == "sub":
            month -= 1
            if month in [1, 3, 5, 7, 8, 10, 12]:
                day = list(range(1, 32))
            elif month in [4, 6, 9, 11]:
                day = list(range(1,31))
            else: day = list(range(1, 29))
            month = [month]*len(day)
            year = [year]*len(day)
            return [year, month, day]
        elif mode == "current":
            if month in [1, 3, 5, 7, 8, 10, 12]:
                day = list(range(curr_day, 32))
            elif month in [4, 6, 9, 11]:
                day = list(range(curr_day, 31))
            else: day = list(range(curr_day, 29))
            month = [month]*len(day)
            year = [year]*len(day)
            return [year, month, day]

    def _get_day(self, today=datetime.date.today(), timedelta=1, mode = "sub"):
        if mode == "add":
            return str(today + datetime.timedelta(days=timedelta)).split("-")
        elif mode == "sub":
            return str(today - datetime.timedelta(days=timedelta)).split("-")
    
    def _get_week(self, mode):
        today = datetime.date.today()
        start_delta = datetime.timedelta(today.weekday())
        start_of_week = today - start_delta
        results = []
        for i in range(7,14):
            if mode == "add":
                get_date = self._get_day(start_of_week, timedelta=i, mode=mode)
                day = [get_date[2]]
                month = [get_date[1]]
                year = [get_date[0]]
                wod = [self.week_days[datetime.date(int(year[i]), int(month[i]), int(day[i])).weekday()] for i in range(len(day))]
                result = [(w, d, m, y) for w, d, m ,y in zip(wod, day, month, year)]
                results.extend(result)
            elif mode == "sub":
                get_date = self._get_day(start_of_week, 14-i, mode=mode)
                day = [get_date[2]]
                month = [get_date[1]]
                year = [get_date[0]]
                wod = [self.week_days[datetime.date(int(year[i]), int(month[i]), int(day[i])).weekday()] for i in range(len(day))]
                result = [(w, d, m, y) for w, d, m ,y in zip(wod, day, month, year)]
                results.extend(result)
        return results # [("thứ 2", 1,1,111), ("thứ 3", 2, 1, 1111) ... ("chủ nhật", 7, 1, 1111)]

    # def _fill_none(result):
    #     for i in result:
    #         if i[1] != 'None' and i[2] != 'None':
                