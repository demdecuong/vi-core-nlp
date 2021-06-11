import re
import json

from datetime import date
import datetime

from vma_nlu.utils.pattern import get_date_absolute, get_date_relative

class PatternMatching(object):
    def __init__(self, dict_path = "./vma_nlu/data/dictionary_normalize_date.json") -> None:
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

        with open(dict_path, "r", encoding="utf-8") as f:
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
            if tmp == 0:
                return entities, value

            if wod:
                wod_tmp = [x[0] for x in wod]
                day_tmp = ["None"] * len(wod)
                month_tmp = ["None"] * len(wod)
                year_tmp = ["None"] * len(wod)
                for i in range(len(wod)):
                    value.append([(wod_tmp[i], day_tmp[i], month_tmp[i], year_tmp[i])])
                    entities.append({
                        "start": wod[i][1][0],
                        "end": wod[i][1][1]
                    })
            if day:
                wod_tmp = ["None"] * len(day)
                day_tmp = [self.dict_normalize[re.search("(\d+)|(((một)|(mot)|(hai)|(ba)|(bốn)|(bon)|(tư)|(tu)|(năm)|(nam)|(lăm)|(lam)|(sáu)|(bảy)|(bay)|(tám)|(tam)|(chín)|(chin)|(mười)|(muoi)|(mười một)|(muoi mot)|(mười hai)|(muoi hai)|(giêng)|(gieng)|(chạp)|(chap)|(mươi))(\s|$)((một)|(mot)|(hai)|(ba)|(bốn)|(bon)|(tư)|(tu)|(năm)|(nam)|(lăm)|(lam)|(sáu)|(bảy)|(bay)|(tám)|(tam)|(chín)|(chin)|(mười)|(muoi)|(mươi)|(mười một)|(muoi mot)|(mười hai)|(muoi hai)|(giêng)|(gieng)|(chạp)|(chap)|(mốt))*(\s|$)*)", x[0]).group()] for x in day]
                month_tmp = ["None"] * len(day)
                year_tmp = ["None"] * len(day)
                for i in range(len(day)):
                    value.append([(wod_tmp[i], day_tmp[i], month_tmp[i], year_tmp[i])])
                    entities.append({
                        "start": day[i][1][0],
                        "end": day[i][1][1]
                    })

            if month:
                wod_tmp = ["None"] * len(month)
                day_tmp = ["None"] * len(month)
                month_tmp = [self.dict_normalize[re.search("(\d+)|(((một)|(mot)|(hai)|(ba)|(bốn)|(bon)|(tư)|(tu)|(năm)|(nam)|(lăm)|(lam)|(sáu)|(bảy)|(bay)|(tám)|(tam)|(chín)|(chin)|(mười)|(muoi)|(mười một)|(muoi mot)|(mười hai)|(muoi hai)|(giêng)|(gieng)|(chạp)|(chap)|(mươi))(\s|$)((một)|(mot)|(hai)|(ba)|(bốn)|(bon)|(tư)|(tu)|(năm)|(nam)|(lăm)|(lam)|(sáu)|(bảy)|(bay)|(tám)|(tam)|(chín)|(chin)|(mười)|(muoi)|(mươi)|(mười một)|(muoi mot)|(mười hai)|(muoi hai)|(giêng)|(gieng)|(chạp)|(chap)|(mốt))*(\s|$)*)", x[0]).group()] for x in month]
                year_tmp = ["None"] * len(month)
                for i in range(len(month)):
                    value.append([(wod_tmp[i], day_tmp[i], month_tmp[i], year_tmp[i])])
                    entities.append({
                        "start": month[i][1][0],
                        "end": month[i][1][1]
                    })
            if year:
                wod_tmp = ["None"] * len(year)
                day_tmp = ["None"] * len(year)
                month_tmp = ["None"] * len(year)
                year_tmp = [int(re.search("\d+", x[0]).group()) for x in year]
                for i in range(len(year)):
                    value.append([(wod_tmp[i], day_tmp[i], month_tmp[i], year_tmp[i])])
                    entities.append({
                        "start": year[i][1][0],
                        "end": year[i][1][1]
                    })

            # wod_pattern = []
            # wod_span = []
            # day_pattern = []
            # day_span = []
            # month_pattern = []
            # month_span = []
            # year_pattern = []
            # year_span = []
            # for x in re.finditer(self.wod, text):
            #     wod_pattern.append(x.group())
            #     wod_span.append(x.span())
            # for x in re.finditer(self.day, text):
            #     day_pattern.append(x.group())
            #     day_span.append(x.span())
            # for x in re.finditer(self.month, text):
            #     month_pattern.append(x.group())
            #     month_span.append(x.span())
            # for x in re.finditer(self.year, text):
            #     year_pattern.append(x.group())
            #     year_span.append(x.span())
            
            # tmp = max(len(wod_pattern), len(day_pattern), len(month_pattern), len(year_pattern)) 
            # if tmp == 0:
            #     return entities, value
            
            # all_span = wod_span + day_span + month_span + year_span
            # start_span = min(all_span, key= lambda x: x[0])
            # end_span = max(all_span, key= lambda x: x[1])

            # wod = ["None"] * tmp
            # day = ["None"] * tmp
            # month = ["None"] * tmp
            # year = ["None"] * tmp

            # if wod_pattern:
            #     wod = wod_pattern * tmp
            #     wod = wod[:tmp]
                
            # if day_pattern:
            #     day_pattern = [self.dict_normalize[re.search("(\d+)|(((một)|(mot)|(hai)|(ba)|(bốn)|(bon)|(tư)|(tu)|(năm)|(nam)|(lăm)|(lam)|(sáu)|(bảy)|(bay)|(tám)|(tam)|(chín)|(chin)|(mười)|(muoi)|(mười một)|(muoi mot)|(mười hai)|(muoi hai)|(giêng)|(gieng)|(chạp)|(chap)|(mươi))(\s|$)((một)|(mot)|(hai)|(ba)|(bốn)|(bon)|(tư)|(tu)|(năm)|(nam)|(lăm)|(lam)|(sáu)|(bảy)|(bay)|(tám)|(tam)|(chín)|(chin)|(mười)|(muoi)|(mươi)|(mười một)|(muoi mot)|(mười hai)|(muoi hai)|(giêng)|(gieng)|(chạp)|(chap)|(mốt))*(\s|$)*)", x).group()] for x in day_pattern]
            #     day = day_pattern * tmp
            #     day = day[:tmp]
            
            # if month_pattern:
            #     month_pattern = [self.dict_normalize[re.search("(\d+)|(((một)|(mot)|(hai)|(ba)|(bốn)|(bon)|(tư)|(tu)|(năm)|(nam)|(lăm)|(lam)|(sáu)|(bảy)|(bay)|(tám)|(tam)|(chín)|(chin)|(mười)|(muoi)|(mười một)|(muoi mot)|(mười hai)|(muoi hai)|(giêng)|(gieng)|(chạp)|(chap)|(mươi))(\s|$)((một)|(mot)|(hai)|(ba)|(bốn)|(bon)|(tư)|(tu)|(năm)|(nam)|(lăm)|(lam)|(sáu)|(bảy)|(bay)|(tám)|(tam)|(chín)|(chin)|(mười)|(muoi)|(mươi)|(mười một)|(muoi mot)|(mười hai)|(muoi hai)|(giêng)|(gieng)|(chạp)|(chap)|(mốt))*(\s|$)*)", x).group()] for x in month_pattern]
            #     month = month_pattern * tmp
            #     month = month[:tmp]
            
            # if year_pattern:
            #     year_pattern = [int(re.search("\d+", x).group()) for x in year_pattern]
            #     year = year_pattern * tmp
            #     year = year[:tmp]

            # entities.append({
            #     "start": start_span[0],
            #     "end": end_span[1]
            # })

            # value.append([(w, d, m, y) for w, d, m, y in zip(wod, day, month, year)])

            return value, entities 

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