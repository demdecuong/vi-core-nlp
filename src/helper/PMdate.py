import re
import json

from datetime import date
import datetime


from src.helper.pattern_date import absolute, relative
# from Preprocess import Preprocess


class PatternMatching(object):
    def __init__(self) -> None:
        super().__init__()

        self.format_date, self.wod, self.wod_vn, self.day_vn, self.month, self.month_vn, self.year = absolute()
        self.format_date = "|".join([x for x in self.format_date])

        self.wod = "|".join([self.wod[0], self.wod_vn[0]])
        self.day = self.day_vn[0]
        self.month = "|".join([self.month[0], self.month_vn[0]])
        self.year = self.year[0]

        self.short_time, self.long_time, self.semi_format = relative()
        self.semi_format = self.semi_format[0]
        self.non_format = "|".join([self.short_time[0], self.long_time[0]])

        self.week_days=["Thứ 2","Thứ 3","Thứ 4","Thứ 5","Thứ 6","Thứ 7","Chủ nhật"]

        with open("./src/helper/dictionary_normalize_date.json", "r", encoding="utf-8") as f:
            self.dict_normalize = json.load(f)


    def extract_date(self, text):
        text = text.lower()

        get_pattern_absolute = [(x.group(), x.span()) for x in re.finditer(self.format_date, text)]
        get_pattern_relative = [(x.group(), x.span()) for x in re.finditer(self.non_format, text)]

        value = []
        entities = []

        if not get_pattern_relative and not get_pattern_absolute:
            semi_format = [(x.group(), x.span()) for x in re.finditer(self.semi_format, text)]
            if semi_format:
                for pattern, span in semi_format:
                    tmp = re.split('(,|\s|\.|-|\/|_)', pattern)
                    day = int(tmp[0])
                    month = int(tmp[2])
                    wod = "None"
                    year = "None"
                    entities.append({
                        "start": span[0],
                        "end": span[1]
                    })
                    value.append([(wod, day, month, year)])

            wod = [(x.group(), x.span()) for x in re.finditer(self.wod, text)]
            day = [(x.group(), x.span()) for x in re.finditer(self.day, text)]
            month = [(x.group(), x.span()) for x in re.finditer(self.month, text)]
            year = [(x.group(), x.span()) for x in re.finditer(self.year, text)]

            tmp = max(len(wod), len(day), len(month), len(year))
            if tmp == 0 and entities:
                return entities, value

            for i in range(tmp):
                if not wod:
                    wod = "None"
                else:
                    wod = wod[i][0]
                
                if not day:
                    day = "None"
                else:
                    day = re.search("(\d+)|(((một)|(mot)|(hai)|(ba)|(bốn)|(bon)|(tư)|(tu)|(năm)|(nam)|(lăm)|(lam)|(sáu)|(bảy)|(bay)|(tám)|(tam)|(chín)|(chin)|(mười)|(muoi)|(mười một)|(muoi mot)|(mười hai)|(muoi hai)|(giêng)|(gieng)|(chạp)|(chap)|(mươi))(\s|$)((một)|(mot)|(hai)|(ba)|(bốn)|(bon)|(tư)|(tu)|(năm)|(nam)|(lăm)|(lam)|(sáu)|(bảy)|(bay)|(tám)|(tam)|(chín)|(chin)|(mười)|(muoi)|(mươi)|(mười một)|(muoi mot)|(mười hai)|(muoi hai)|(giêng)|(gieng)|(chạp)|(chap)|(mốt))*(\s|$)*)", day).group()
                    day = self.dict_normalize[day]
                
                if not month:
                    month = "None"
                else:
                    month = re.search("(\d+)|((một)|(mot)|(hai)|(ba)|(bốn)|(bon)|(tư)|(tu)|(năm)|(nam)|(lăm)|(lam)|(sáu)|(bảy)|(bay)|(tám)|(tam)|(chín)|(chin)|(mười)|(muoi)|(mười một)|(muoi mot)|(mười hai)|(muoi hai)|(giêng)|(gieng)|(chạp)|(chap))", month).group()
                    month = self.dict_normalize[day]
                
                if not year:
                    year = "None"
                else:
                    year = int(re.search("\d+", year).group())
                    
            value.append([(w, d, m, y) for w, d, m, y in zip(wod, day, month, year)])
            return entities, value

        else:
            if get_pattern_absolute:
                for pattern, span in get_pattern_absolute:
                    tmp = re.split('(,|\s|\.|-|\/|_)', pattern)
                    day = int(tmp[0])
                    month = int(tmp[2])
                    year = int(tmp[4])
                    wod = self.week_days[datetime.date(year, month, day).weekday()]
                    entities.append({
                        "start": span[0],
                        "end": span[1]
                    })
                    value.append([(wod, day, month, year)])

            if get_pattern_relative: # get_pattern_relative = ['ngày mai', 'tháng này', ... ]
                ent, val = self._map_relative_to_date(get_pattern_relative=get_pattern_relative)

                entities.extend(ent)
                value.extend(val)

            return value, entities

    def _map_relative_to_date(self, get_pattern_relative):

        entities = []
        value = []

        for pattern, span in get_pattern_relative:
            if re.search("qua", pattern):
                
                if re.search("(ngày)|(ngay)|(ngayf)", pattern) or re.search("(hôm)|(hom)", pattern) or re.search("(sáng)|(sang)", pattern) or re.search("(trưa)|(trua)", pattern) or re.search("(chiều)|(chieu)", pattern) or re.search("(tối)|(toi)", pattern):
                    get_date = self._get_day(timedelta=1, mode="sub")
                    day = int(get_date[2])
                    month = int(get_date[1])
                    year = int(get_date[0])
                    wod = self.week_days[datetime.date(year, month, day).weekday()]
                    entities.append({
                        "start": span[0],
                        "end": span[1]
                    })
                    value.append([(wod, day, month, year)])
                    
                
                elif re.search("(tuần)|(tuan)", pattern):
                    entities.append({
                        "start": span[0],
                        "end": span[1]
                    })
                    value.append(self._get_week(mode="sub"))

                elif re.search("(tháng)|(thang)", pattern):
                    get_month = self._get_month("sub")
                    day = get_month[2]
                    month = get_month[1]
                    year = get_month[0]
                    wod = [self.week_days[datetime.date(int(year[i]), int(month[i]), int(day[i])).weekday()] for i in range(len(day))]
                    entities.append({
                        "start": span[0],
                        "end": span[1]
                    })
                    value.append([(w, d, m, y) for w, d, m ,y in zip(wod, day, month, year)])
            
            elif re.search("(này)|(nay)", pattern):

                if re.search("(ngày)|(ngay)|(ngayf)", pattern) or re.search("(hôm)|(hom)", pattern) or re.search("(sáng)|(sang)", pattern) or re.search("(trưa)|(trua)", pattern) or re.search("(chiều)|(chieu)", pattern) or re.search("(tối)|(toi)", pattern):
                    get_date = self._get_day(timedelta=0, mode="add")
                    day = int(get_date[2])
                    month = int(get_date[1])
                    year = int(get_date[0])
                    wod = self.week_days[datetime.date(year, month, day).weekday()]
                    entities.append({
                        "start": span[0],
                        "end": span[1]
                    })
                    value.append([(wod, day, month, year)])

                elif re.search("(tuần)|(tuan)", pattern):
                    today = datetime.date.today()
                    weekday = today.weekday()
                    result = []
                    for i in range(7-int(weekday)):
                        get_date = self._get_day(timedelta=i, mode="add")
                        day = int(get_date[2])
                        month = int(get_date[1])
                        year = int(get_date[0])
                        wod = self.week_days[datetime.date(year, month, day).weekday()]
                        result.append((wod, day, month, year))
                    entities.append({
                        "start": span[0],
                        "end": span[1]
                    })    
                    value.append(result)

                elif re.search("(tháng)|(thang)", pattern):
                    get_month = self._get_month("current")
                    day = get_month[2]
                    month = get_month[1]
                    year = get_month[0]
                    wod = [self.week_days[datetime.date(int(year[i]), int(month[i]), int(day[i])).weekday()] for i in range(len(day))]
                    entities.append({
                        "start": span[0],
                        "end": span[1]
                    })
                    value.append([(w, d, m, y) for w, d, m ,y in zip(wod, day, month, year)])
            
            elif re.search("mai", pattern) or re.search("tới", pattern) or re.search("sau", pattern):
                
                if re.search("(ngày)|(ngay)|(ngayf)", pattern) or re.search("(hôm)|(hom)", pattern) or re.search("(sáng)|(sang)", pattern) or re.search("(trưa)|(trua)", pattern) or re.search("(chiều)|(chieu)", pattern) or re.search("(tối)|(toi)", pattern):
                    get_date = self._get_day(timedelta=1, mode="add")
                    day = int(get_date[2])
                    month = int(get_date[1])
                    year = int(get_date[0])
                    wod = self.week_days[datetime.date(year, month, day).weekday()]
                    entities.append({
                        "start": span[0],
                        "end": span[1]
                    })
                    value.append([(wod, day, month, year)])

                elif re.search("(tuần)|(tuan)", pattern):
                    entities.append({
                        "start": span[0],
                        "end": span[1]
                    })
                    value.append(self._get_week(mode="add"))

                elif re.search("(tháng)|(thang)", pattern):
                    get_date = self._get_month("add")
                    day = get_date[2]
                    month = get_date[1]
                    year = get_date[0]
                    wod = [self.week_days[datetime.date(int(year[i]), int(month[i]), int(day[i])).weekday()] for i in range(len(day))]
                    entities.append({
                        "start": span[0],
                        "end": span[1]
                    })
                    value.append([(w, d, m, y) for w, d, m ,y in zip(wod, day, month, year)])

            elif re.search("mốt", pattern):
                get_date = self._get_day(timedelta=2, mode="add")
                day = int(get_date[2])
                month = int(get_date[1])
                year = int(get_date[0])
                wod = self.week_days[datetime.date(year, month, day).weekday()]
                entities.append({
                    "start": span[0],
                    "end": span[1]
                })
                value.append([(wod, day, month, year)])

            elif re.search("kia", pattern):
                get_date = self._get_day(timedelta=3, mode="add")
                day = int(get_date[2])
                month = int(get_date[1])
                year = int(get_date[0])
                wod = self.week_days[datetime.date(year, month, day).weekday()]
                entities.append({
                    "start": span[0],
                    "end": span[1]
                })
                value.append([(wod, day, month, year)])
            
        return entities, value


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
        value = []
        for i in range(7,14):
            if mode == "add":
                get_date = self._get_day(start_of_week, timedelta=i, mode=mode)
                day = int(get_date[2])
                month = int(get_date[1])
                year = int(get_date[0])
                wod = self.week_days[datetime.date(year, month, day).weekday()]
                value.append((wod, day, month, year))
            elif mode == "sub":
                get_date = self._get_day(start_of_week, 14-i, mode=mode)
                day = int(get_date[2])
                month = int(get_date[1])
                year = int(get_date[0])
                wod = self.week_days[datetime.date(year, month, day).weekday()]
                value.append((wod, day, month, year))
        return value # [("thứ 2", 1,1,111), ("thứ 3", 2, 1, 1111) ... ("chủ nhật", 7, 1, 1111)]

    # def _fill_none(result):
    #     for i in result:
    #         if i[1] != 'None' and i[2] != 'None':
                