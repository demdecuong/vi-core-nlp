import re
import json

from datetime import date
import datetime

from vi_nlp_core.utils.date_pattern import absolute, relative
from vi_nlp_core.utils.util import convert_date_to_timestamp


class DateMatcher(object):
    def __init__(self, dict_path="./vi_nlp_core/data/dictionary_normalize_date.json") -> None:
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
        self.short_time, self.long_time, self.adj_pattern_top, self.adj_pattern_middle, self.adj_pattern_bot = relative()
        self.rel_pattern = "|".join([self.short_time[0], self.long_time[0]])

        self.adj_pattern_top = self.adj_pattern_top[0]
        self.adj_pattern_middle = self.adj_pattern_middle[0]
        self.adj_pattern_bot = self.adj_pattern_bot[0]

        self.week_days = ["thứ 2", "thứ 3", "thứ 4",
                          "thứ 5", "thứ 6", "thứ 7", "chủ nhật"]
        with open(dict_path, "r", encoding="utf-8") as f:
            self.dict_normalize = json.load(f)

    def extract_date(self, text):

        text = text.lower()

        value = []
        entities = []

        get_pattern_absolute = [(x.group(), x.span())
                                for x in re.finditer(self.abs_pattern, text)]
        get_pattern_relative = [(x.group(), x.span())
                                for x in re.finditer(self.rel_pattern, text)]

        wod = [(x.group(), x.span()) for x in re.finditer(self.wod, text)]
        day = [(x.group(), x.span()) for x in re.finditer(self.day, text)]
        # print(day)
        month = [(x.group(), x.span()) for x in re.finditer(self.month, text)]
        year = [(x.group(), x.span()) for x in re.finditer(self.year, text)]

        wod, day, month, year = self.normalize_date_2(wod, day, month, year)

        short_abs = [(x.group(), x.span())
                     for x in re.finditer(self.short_abs, text)]

        # Process

        # Absolute - Number
        if get_pattern_absolute:
            del short_abs
            short_abs = None
            val, ent = self.extract_date_abs_number(
                get_pattern_absolute, "long")
            value.extend(val)
            entities.extend(ent)
            return self.output_format_timestamp(value=value, entities=entities, extractor="date_matcher")
        elif short_abs:
            val, ent = self.extract_date_abs_number(short_abs, "short")
            value.extend(val)
            entities.extend(ent)
            return self.output_format_timestamp(value=value, entities=entities, extractor="date_matcher")

        if get_pattern_relative:  # Relative
            val, ent = self._map_relative_to_date(get_pattern_relative)
            # print(val)
            # print(ent)
            # Relative clear
            val, ent, flag = self.extract_date_rel_with_adj(
                val, ent, self.adj_pattern_top, self.adj_pattern_middle, self.adj_pattern_bot, text)
            # print(val)
            # print(ent)
            val, ent = self.extract_date_rel_clearly(val, ent, wod, day, flag)
            # print(val)
            # print(ent)
            value.extend(val)
            entities.extend(ent)
            return self.output_format_timestamp(value=value, entities=entities, extractor="date_matcher")

        # Return None if not extract
        tmp = max(len(wod), len(day), len(month), len(year))
        if tmp == 0:
            return self.output_format_timestamp(value=value, entities=entities, extractor="date_matcher")

        # Absolute - String and Number
        val, ent = self.extract_date_abs_string_number(wod, day, month, year)
        value.extend(val)
        entities.extend(ent)

        return self.output_format_timestamp(value=value, entities=entities, extractor="date_matcher")

    def _map_relative_to_date(self, get_pattern_relative):

        value = []
        entities = []

        for pattern, span in get_pattern_relative:
            if re.search("((qua)|(rồi))", pattern):

                if re.search("(ngày)|(ngay)|(ngayf)", pattern) or re.search("(hôm)|(hom)", pattern) or re.search("(sáng)|(sang)", pattern) or re.search("(trưa)|(trua)", pattern) or re.search("(chiều)|(chieu)", pattern) or re.search("(tối)|(toi)", pattern):
                    get_date = self._get_day(timedelta=1, mode="sub")
                    day = int(get_date[2])
                    month = int(get_date[1])
                    year = int(get_date[0])
                    wod = self.week_days[datetime.date(
                        year, month, day).weekday()]
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
                    wod = [self.week_days[datetime.date(int(year[i]), int(
                        month[i]), int(day[i])).weekday()] for i in range(len(day))]
                    entities.append({
                        "start": span[0],
                        "end": span[1]
                    })
                    value.append([(w, d, m, y)
                                  for w, d, m, y in zip(wod, day, month, year)])

            elif re.search("(này)|(nay)", pattern):

                if re.search("(ngày)|(ngay)|(ngayf)", pattern) or re.search("(hôm)|(hom)", pattern) or re.search("(sáng)|(sang)", pattern) or re.search("(trưa)|(trua)", pattern) or re.search("(chiều)|(chieu)", pattern) or re.search("(tối)|(toi)", pattern):
                    get_date = self._get_day(timedelta=0, mode="add")
                    day = int(get_date[2])
                    month = int(get_date[1])
                    year = int(get_date[0])
                    wod = self.week_days[datetime.date(
                        year, month, day).weekday()]
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
                        wod = self.week_days[datetime.date(
                            year, month, day).weekday()]
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
                    wod = [self.week_days[datetime.date(int(year[i]), int(
                        month[i]), int(day[i])).weekday()] for i in range(len(day))]
                    entities.append({
                        "start": span[0],
                        "end": span[1]
                    })
                    value.append([(w, d, m, y)
                                  for w, d, m, y in zip(wod, day, month, year)])

            elif re.search("mai", pattern) or re.search("tới", pattern) or re.search("sau", pattern):

                if re.search("(ngày)|(ngay)|(ngayf)", pattern) or re.search("(hôm)|(hom)", pattern) or re.search("(sáng)|(sang)", pattern) or re.search("(trưa)|(trua)", pattern) or re.search("(chiều)|(chieu)", pattern) or re.search("(tối)|(toi)", pattern):
                    get_date = self._get_day(timedelta=1, mode="add")
                    day = int(get_date[2])
                    month = int(get_date[1])
                    year = int(get_date[0])
                    wod = self.week_days[datetime.date(
                        year, month, day).weekday()]
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
                    wod = [self.week_days[datetime.date(int(year[i]), int(
                        month[i]), int(day[i])).weekday()] for i in range(len(day))]
                    entities.append({
                        "start": span[0],
                        "end": span[1]
                    })
                    value.append([(w, d, m, y)
                                  for w, d, m, y in zip(wod, day, month, year)])

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
                day = list(range(1, 31))
            else:
                day = list(range(1, 29))
            month = [month]*len(day)
            year = [year]*len(day)
            return [year, month, day]
        elif mode == "sub":
            month -= 1
            if month in [1, 3, 5, 7, 8, 10, 12]:
                day = list(range(1, 32))
            elif month in [4, 6, 9, 11]:
                day = list(range(1, 31))
            else:
                day = list(range(1, 29))
            month = [month]*len(day)
            year = [year]*len(day)
            return [year, month, day]
        elif mode == "current":
            if month in [1, 3, 5, 7, 8, 10, 12]:
                day = list(range(curr_day, 32))
            elif month in [4, 6, 9, 11]:
                day = list(range(curr_day, 31))
            else:
                day = list(range(curr_day, 29))
            month = [month]*len(day)
            year = [year]*len(day)
            return [year, month, day]

    def _get_day(self, today=datetime.date.today(), timedelta=1, mode="sub"):
        if mode == "add":
            return str(today + datetime.timedelta(days=timedelta)).split("-")
        elif mode == "sub":
            return str(today - datetime.timedelta(days=timedelta)).split("-")

    def _get_week(self, mode):
        today = datetime.date.today()
        start_delta = datetime.timedelta(today.weekday())
        start_of_week = today - start_delta
        value = []
        for i in range(7, 14):
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
        # [("thứ 2", 1,1,111), ("thứ 3", 2, 1, 1111) ... ("chủ nhật", 7, 1, 1111)]
        return value

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

    def output_format_timestamp(self, value, entities, extractor):
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
                        "value": convert_date_to_timestamp(value[i]),
                        "confidence": 1.0,
                        "extractor": extractor
                    }
                )
            return result
    # [21/03/1997 21-03-1997 21_03-1997, ... ]
    def extract_date_abs_number(self, patterns, cat="long"):
        value=[]
        entities=[]
        for pattern, span in patterns:
            tmp=re.split('(,|\s|\.|-|\/|_)', pattern.strip())
            day=int(tmp[0])
            month=int(tmp[2])
            flag=self.check_valid_date(day, month)
            if not flag:
                value.append([])
            else:
                if cat == "long":
                    year=str(tmp[4])
                    if len(year) == 4:
                        year=int(year)
                    elif len(year) == 2:
                        if int(year) > 50:
                            year="19"+year
                        else:
                            year="20"+year
                        year=int(year)
                    elif len(year) == 1:
                        year=int(datetime.datetime.now().year)
                    wod=self.week_days[datetime.date(
                        year, month, day).weekday()]
                    value.append(
                        [self.normalize_date((wod, day, month, year))])
                else:
                    year=None
                    wod=None
                    value.append(
                        [self.normalize_date((wod, day, month, year))])
            entities.append({
                "start": span[0],
                "end": span[1]
            })

        return value, entities

    def normalize_date(self, input_date):  # (WOD, DD, MM, YYYY)
        WOD=input_date[0]
        DD=int(input_date[1])
        MM=int(input_date[2])
        YYYY=input_date[3]
        return (WOD, DD, MM, YYYY)

    # Ex: thứ 5 tuần sau, thứ 2 tuần tới
    def extract_date_rel_clearly(self, val, ent, wod, day, flag):
        if not wod and not day:
            if flag:
                return val, ent
            else:
                values=[]
                entities=[]
                for vs, es in zip(val, ent):
                    v=vs[int(len(vs)/2)]
                    values.append([v])
                    entities.append(es)
                return values, entities
        entities=[]
        values=[]

        # [[("thứ 2", 22, 2, 2222)], [("thứ 2", 22, 2, 2222), ("thứ 3", 22, 3, 2232)]] # [{"start": 10, "end": 20 },  {"start": 20, "end":25}]
        for v, e in zip(val, ent):
            if len(v) == 1:
                entities.append(v)
                values.append(e)
                continue
            if wod:
                start_span=100
                end_span=0
                start_span=min([i[1][0] for i in wod])
                start_span=min(start_span, e['start'])
                end_span=max([i[1][1] for i in wod])
                end_span=max(end_span, e['end'])
                value=[]
                tmp=[i[0] for i in v]
                tmp_1=[i[0] for i in wod]
                for index, i in enumerate(tmp):
                    if i in tmp_1:
                        value.extend([v[index]])
                if not value:
                    value=v
                    entities.append(e)
                else:
                    entities.append({
                        "start": start_span,
                        "end": end_span
                    })
                    values.append(value)

            if day:
                value=[]
                start_span=100
                end_span=0
                start_span=min([i[1][0] for i in day])
                start_span=min(start_span, e['start'])
                end_span=max([i[1][1] for i in day])
                end_span=max(end_span, e['end'])
                tmp=[i[1] for i in v]
                tmp_1=[i[0] for i in day]
                for index, i in enumerate(tmp):
                    if i in tmp_1:
                        value.extend([v[index]])
                if not value:
                    value=v
                    entities.append(e)
                else:
                    entities.append({
                        "start": start_span,
                        "end": end_span
                    })
                    values.append(value)
        return values, entities

    def extract_date_abs_string_number(self, wod, day, month, year):
        tmp=max(len(wod), len(day), len(month), len(year))
        # print(tmp)
        start_span=100
        end_span=0
        wod_tmp=[None] * tmp
        day_tmp=[None] * tmp
        month_tmp=[None] * tmp
        year_tmp=[None] * tmp
        if wod:
            wod=wod * tmp
            wod=wod[:tmp]
            wod_tmp=[i[0] for i in wod]
            start_span=min(
                [j[1][0] if j[1][0] < start_span else start_span for j in wod])
            end_span=max(
                [j[1][1] if j[1][1] > end_span else end_span for j in wod])
        if day:
            day=day * tmp
            day=day[:tmp]
            day_tmp=[i[0] for i in day]
            start_span=min(
                [j[1][0] if j[1][0] < start_span else start_span for j in day])
            end_span=max(
                [j[1][1] if j[1][1] > end_span else end_span for j in day])
        if month:
            month=month * tmp
            month=month[:tmp]
            month_tmp=[i[0] for i in month]
            start_span=min(
                [j[1][0] if j[1][0] < start_span else start_span for j in month])
            end_span=max(
                [j[1][1] if j[1][1] > end_span else end_span for j in month])
        if year:
            year=year * tmp
            year=year[:tmp]
            year_tmp=[i[0] for i in year]
            start_span=min(
                [j[1][0] if j[1][0] < start_span else start_span for j in year])
            end_span=max(
                [j[1][1] if j[1][1] > end_span else end_span for j in year])
        value=[]
        entities=[{
            "start": start_span,
            "end": end_span
        }]
        value.append([(w, d, m, y) for w, d, m, y in zip(
            wod_tmp, day_tmp, month_tmp, year_tmp)])
        return value, entities

    def normalize_date_2(self, wod, day, month, year):
        if wod:
            wod_tmp=[]
            for i in wod:
                value=re.sub('(thứ)|(thu)|(thuws)|(Thứ)', '', i[0])
                value=value.strip()
                value=self.dict_normalize.get(value, value)
                if value != "chủ nhật":
                    value='thứ ' + str(value)
                wod_tmp.append((value, i[1]))
            wod=wod_tmp
        if day:
            day_tmp=[]
            for i in day:
                value=re.sub('(ngày)|(ngay)|(ngafy)', '', i[0])
                value=re.sub('(tháng)|(thang)', '', value)
                value=value.strip()
                value=self.dict_normalize.get(value, value)
                day_tmp.append((value, i[1]))
            day=day_tmp
        if month:
            month_tmp=[]
            for i in month:
                value=re.sub('(tháng)|(thang)|(thasng)', '', i[0])
                value=value.strip()
                value=self.dict_normalize.get(value, value)
                month_tmp.append((value, i[1]))
            month=month_tmp
        if year:
            year_tmp=[]
            for i in year:
                value=re.sub('(năm)|(nam)', '', i[0])
                value=value.strip()
                value=int(value)
                year_tmp.append((value, i[1]))
            year=year_tmp
        return wod, day, month, year

    def extract_date_rel_with_adj(self, val, ent, top, middle, bot, text):
        flag=False
        top=[(x.group(), x.span()) for x in re.finditer(top, text)]
        middle=[(x.group(), x.span()) for x in re.finditer(middle, text)]
        bot=[(x.group(), x.span()) for x in re.finditer(bot, text)]
        if not top and not middle and not bot:
            return val, ent, flag
        else:
            flag=True
            values=[]
            entities=[]
            for vs, es in zip(val, ent):
                if top:
                    for i in top:
                        v=vs[:round(len(vs)*0.25)]
                        # print(v)
                        values.append(v)
                        start_span=min(i[1][0], es["start"])
                        end_span=max(i[1][1], es["end"])
                        entities.append({
                            "start": start_span,
                            "end": end_span
                        })
                if middle:
                    for i in middle:
                        v=vs[round(len(vs)*0.25):round(len(vs)*0.75)]
                        values.append(v)
                        start_span=min(i[1][0], es["start"])
                        end_span=max(i[1][1], es["end"])
                        entities.append({
                            "start": start_span,
                            "end": end_span
                        })
                if bot:
                    for i in bot:
                        v=vs[round(len(vs)*0.75):]
                        values.append(v)
                        start_span=min(i[1][0], es["start"])
                        end_span=max(i[1][1], es["end"])
                        entities.append({
                            "start": start_span,
                            "end": end_span
                        })
            return values, entities, flag

    def check_valid_date(self, day, month):
        flag=False
        day_count_for_month=[0, 31, 28, 31,
                               30, 31, 30, 31, 31, 30, 31, 30, 31]
        if month > 12 or month <= 0 or int(day) > day_count_for_month[(month)]:
            return flag
        else:
            return True
