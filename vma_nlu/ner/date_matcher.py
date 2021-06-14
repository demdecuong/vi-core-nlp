import re
import json

from datetime import date
import datetime

from vma_nlu.utils.pattern import absolute, relative
class DateMatcher(object):
    def __init__(self, dict_path = "./vma_nlu/data/dictionary_normalize_date.json") -> None:
        super().__init__()

        self.abs_pattern, self.wod, self.wod_vn, self.day_vn, self.month, self.month_vn, self.year, self.only_number, self.short_abs = absolute()
        
        self.abs_pattern = "|".join([x for x in self.abs_pattern])

        self.wod = "|".join([self.wod[0], self.wod_vn[0]])
        self.day = self.day_vn[0]
        self.month = "|".join([self.month[0], self.month_vn[0]])
        self.year = self.year[0]

        self.short_abs = self.short_abs[0]
        self.only_number = self.only_number[0]
        ####################################################
        self.short_time, self.long_time = relative()
        self.rel_pattern = "|".join([self.short_time[0], self.long_time[0]])

        self.week_days=["Thứ 2","Thứ 3","Thứ 4","Thứ 5","Thứ 6","Thứ 7","Chủ nhật"]
        with open(dict_path, "r", encoding="utf-8") as f:
            self.dict_normalize = json.load(f)


    def extract_date(self, text):

        text = text.lower()

        value = []
        entities = []

        get_pattern_absolute = [(x.group(), x.span()) for x in re.finditer(self.abs_pattern, text)]
        get_pattern_relative = [(x.group(), x.span()) for x in re.finditer(self.rel_pattern, text)]

        wod = [(x.group(), x.span()) for x in re.finditer(self.wod, text)] # TODO normalize
        day = [(x.group(), x.span()) for x in re.finditer(self.day, text)] # TODO normalize
        # print(day)
        month = [(x.group(), x.span()) for x in re.finditer(self.month, text)] # TODO normalize
        year = [(x.group(), x.span()) for x in re.finditer(self.year, text)] # TODO normalize

        short_abs = [(x.group(), x.span()) for x in re.finditer(self.short_abs, text)]

        # Process
        
        # Absolute - Number
        if get_pattern_absolute:
            del short_abs
            short_abs = None
            val, ent = self.extract_date_abs_number(get_pattern_absolute, "long")
            value.extend(val)
            entities.extend(ent)
            return self.output_format(value=value, entities=entities, extractor="date_matcher")
        elif short_abs:
            val, ent = self.extract_date_abs_number(short_abs, "short")
            value.extend(val)
            entities.extend(ent)
            return self.output_format(value=value, entities=entities, extractor="date_matcher")
            

        if get_pattern_relative: # Relative
            val, ent  = self._map_relative_to_date(get_pattern_relative)
            # Relative clear
            # val, ent = self.extract_date_rel_clearly(val, ent, wod, day, month, year)
            value.extend(val)
            entities.extend(ent)
            return self.output_format(value=value, entities=entities, extractor="date_matcher")

        # Return None if not extract
        tmp = max(len(wod), len(day), len(month), len(year))
        if tmp == 0:
            return self.output_format(value=value, entities=entities, extractor="date_matcher")
        
        # Absolute - String and Number
        val, ent  = self.extract_date_abs_string_number(wod, day, month, year)
        value.extend(val)
        entities.extend(ent)

        return self.output_format(value=value, entities=entities, extractor="date_matcher")

    def _map_relative_to_date(self, get_pattern_relative):

        value = []
        entities = []
        
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
                    day = get_month[2][-7:]
                    month = get_month[1][-7:]
                    year = get_month[0][-7:]
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
                    tmp = []
                    for i in range(7-int(weekday)):
                        get_date = self._get_day(timedelta=i, mode="add")
                        day = int(get_date[2])
                        month = int(get_date[1])
                        year = int(get_date[0])
                        wod = self.week_days[datetime.date(year, month, day).weekday()]
                        tmp.append((wod, day, month, year))
                    entities.append({
                        "start": span[0],
                        "end": span[1]
                    })
                    value.append(tmp)

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
                    day = get_date[2][:7]
                    month = get_date[1][:7]
                    year = get_date[0][:7]
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
            
        return value, entities


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

    def output_format(self, value, entities, extractor):
        if not value:
            return {
                "entities": []
            }
        else:
            result = {
                "entities": []
            }
            for i in range(len(value)):
                result["entities"].append(
                    {
                        "start": entities[i]["start"],
                        "end": entities[i]["end"],
                        "entity": "date_time",
                        "value": value[i],
                        "confidence": 1.0,
                        "extractor": extractor
                    }
                )
            return result

    def extract_date_abs_number(self, patterns, cat="long"): # [21/03/1997 21-03-1997 21_03-1997, ... ]
        value = []
        entities = []
        for pattern, span in patterns:
            tmp = re.split('(,|\s|\.|-|\/|_)', pattern)
            day = int(tmp[0])
            month = int(tmp[2])
            if cat == "long":
                year = int(tmp[4])
                wod = self.week_days[datetime.date(year, month, day).weekday()]
            else:
                year = "None"
                wod = "None"
            entities.append({
                "start": span[0],
                "end": span[1]
            })
            value.append([self.normalize_date((wod, day, month, year))])
        return value, entities

    def normalize_date(self, input_date): # (WOD, DD, MM, YYYY)
        WOD = str(input_date[0]) #TODO normalize
        DD = int(input_date[1])
        MM = int(input_date[2])
        YYYY = input_date[3]
        return (WOD, DD, MM, YYYY)

    def extract_date_rel_clearly(self, val, ent, wod, day, month, year): # Ex: thứ 5 tuần sau, thứ 2 tuần tới
        for v, e in zip(val, ent): # [[("thứ 2", 22, 2, 2222)], [("thứ 2", 22, 2, 2222), ("thứ 3", 22, 3, 2232)]] # [{"start": 10, "end": 20 },  {"start": 20, "end":25}]
            if wod: # assume wod = [("thứ 2", (10, 20))]
                for i in v:
                    if wod[0][0] in i:
                        pass
            pass

    def extract_date_abs_string_number(self, wod, day, month, year):
        tmp = max(len(wod), len(day), len(month), len(year))
        # print(tmp)
        start_span = 100
        end_span = 0
        wod_tmp = ["None"] * tmp
        day_tmp = ["None"] * tmp
        month_tmp = ["None"] * tmp
        year_tmp = ["None"] * tmp
        if wod:
            wod = wod * tmp
            wod = wod[:tmp]
            wod_tmp = [i[0] for i in wod]
            start_span = min([j[1][0] if j[1][0] < start_span else start_span for j in wod])
            end_span = max([j[1][1] if j[1][1] > end_span else end_span for j in wod])
        if day:
            day = day * tmp
            day = day[:tmp]
            day_tmp = [i[0] for i in day]
            start_span = min([j[1][0] if j[1][0] < start_span else start_span for j in day])
            end_span = max([j[1][1] if j[1][1] > end_span else end_span for j in day])
        if month:
            month = month * tmp
            month = month[:tmp]
            month_tmp = [i[0] for i in month]
            start_span = min([j[1][0] if j[1][0] < start_span else start_span for j in month])
            end_span = max([j[1][1] if j[1][1] > end_span else end_span for j in month])
        if year:
            year = year * tmp
            year = year[:tmp]
            year_tmp = [i[0] for i in year]
            start_span = min([j[1][0] if j[1][0] < start_span else start_span for j in year])
            end_span = max([j[1][1] if j[1][1] > end_span else end_span for j in year])
        value = []
        entities = [{
            "start": start_span,
            "end": end_span
        }]
        value.append([(w, d, m, y) for w, d, m, y in zip(wod_tmp, day_tmp, month_tmp, year_tmp)])
        return value, entities