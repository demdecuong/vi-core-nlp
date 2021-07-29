def absolute():
    absolute = ['(\d+(,|\s|\.|-|\/|_)+\d+(,|\s|\.|-|\/|_)+\d+)', # 21/03/1997  21-03-1997  21.03.1997
                   '((monday|tuesday|wednesday|thursday|friday|saturday|sunday)(,|\s|\.|-|\/|_)\d+(,|\s|\.|-|\/|_)*\d*(,|\s|\.|-|\/|_)*\d*)', # Monday 21 3 
                ] 
    wod = ['(monday|tuesday|wednesday|friday|saturday|sunday)']
    wod_vn = ['(((thứ)|(thu)|(thuws))(\s+|\.+)*[2-8])|(((thứ)|(thu)|(thuws))(\s+|\.+)*((hai)|(bay)|(tư)|(tu)|(bốn)|(bon)|(năm)|(nam)|(lăm)|(lam)|(sáu)|(say)|(bảy)|(ba)))|((chủ nhật)|(chu nhat)|(cn))']

    day_vn = ['(((ngày)|(ngay)|(ngafy))(\s+|\.+)*(\d\d|\d)($|\s))|(((ngày)|(ngay)|(ngafy))\s+((không)|(khong)|(một)|(hai)|(bay)|(bốn)|(bon)|(tư)|(tu)|(năm)|(lăm)|(nam)|(lam)|(sáu)|(sau)|(bảy)|(ba)|(tám)|(tam)|(chín)|(chin)|(mười)|(mươi)|(muoi))(\s*((không)|(khong)|(một)|(mốt)|(mot)|(hai)|(bay)|(bốn)|(bon)|(tư)|(tu)|(năm)|(lăm)|(nam)|(lam)|(sáu)|(sau)|(bảy)|(ba)|(tám)|(tam)|(chín)|(chin)|(mười)|(mươi)|(muoi)))?(\s*((không)|(khong)|(một)|(mốt)|(mot)|(hai)|(bay)|(bốn)|(bon)|(tư)|(tu)|(năm)|(lăm)|(nam)|(lam)|(sáu)|(sau)|(bảy)|(ba)|(tám)|(tam)|(chín)|(chin)|(mười)|(mươi)|(muoi)))?)|((^|\s)\d\d?\s*((tháng)|(thang)))|((^|\s)((không)|(khong)|(một)|(hai)|(bay)|(bốn)|(bon)|(tư)|(tu)|(năm)|(lăm)|(nam)|(lam)|(sáu)|(sau)|(bảy)|(ba)|(tám)|(tam)|(chín)|(chin)|(mười)|(mươi)|(muoi))(\s*((không)|(khong)|(một)|(mốt)|(mot)|(hai)|(bay)|(bốn)|(bon)|(tư)|(tu)|(năm)|(lăm)|(nam)|(lam)|(sáu)|(sau)|(bảy)|(ba)|(tám)|(tam)|(chín)|(chin)|(mười)|(mươi)|(muoi)))?(\s*((không)|(khong)|(một)|(mốt)|(mot)|(hai)|(bay)|(bốn)|(bon)|(tư)|(tu)|(năm)|(lăm)|(nam)|(lam)|(sáu)|(sau)|(bảy)|(ba)|(tám)|(tam)|(chín)|(chin)|(mười)|(mươi)|(muoi)))?\s*((tháng)|(thang)))']

    month = ['((?<=\s)january(?=\s)|(?<=\s)jan(?=\s)|(?<=\s)february(?=\s)|(?<=\s)feb(?=\s)|(?<=\s)march(?=\s)|(?<=\s)mar(?=\s)|(?<=\s)april(?=\s)|(?<=\s)apr(?=\s)|(?<=\s)may(?=\s)|(?<=\s)june(?=\s)|(?<=\s)jun(?=\s)|(?<=\s)july(?=\s)|(?<=\s)jul(?=\s)|(?<=\s)august(?=\s)|(?<=\s)aug(?=\s)|(?<=\s)september(?=\s)|(?<=\s)sep(?=\s)|(?<=\s)october(?=\s)|(?<=\s)oct(?=\s)|(?<=\s)november(?=\s)|(?<=\s)nov(?=\s)|(?<=\s)december(?=\s)|(?<=\s)dec(?=\s))']
    month_vn = ['(((tháng)|(thang)|(thasng))(\s+|\.+)*(\d\d|\d)($|\s))|(((tháng)|(thang))(\s+|\.+)*(một|mot|hai|ba|bốn|bon|tư|tu|năm|nam|lăm|lam|sáu|bảy|bay|tám|tam|chín|chin|muoi|mười một|muoi mot|mười hai|muoi hai|giêng|gieng|chạp|chap|mười))']

    year = ['('+'|'.join([str(i) for i in list(range(1900, 2050))])+')']

    only_number = ['^\d+$']

    short_abs = ['([0-3][0-9](,|\s|\.|-|\/|_)[0-1][0-9])|((^|\s)\d(,|\s|\.|-|\/|_)\d(\s|$))|([0-3][0-9](,|\s|\.|-|\/|_)[0-9](\s|$))|((^|\s)\d(,|\s|\.|-|\/|_)(1[0-2]))'] # 21 / 03

    return absolute, wod, wod_vn, day_vn, month, month_vn, year, only_number, short_abs

def relative():
    short_time = ['(((hôm)|(hom))\s*((qua)|(rồi)|(vừa rồi)|(roi)))|(((hôm)|(hom))\s*nay)|(((hôm)|(hom))\s*kia)|(((ngày)|(ngay))\s(((hôm)|(hom))\s)*((qua)|(rồi)|(vừa rồi)|(roi)))|(sáng\s(((hôm)|(hom))\s)*((qua)|(rồi)|(vừa rồi)|(roi)))|(trưa\s(((hôm)|(hom))\s)*((qua)|(rồi)|(vừa rồi)|(roi)))|(chiều\s(((hôm)|(hom))\s)*((qua)|(rồi)|(vừa rồi)|(roi)))|(tối\s(((hôm)|(hom))\s)*((qua)|(rồi)|(vừa rồi)|(roi)))|(((ngày)|(ngay))\s(((hôm)|(hom))\s)*nay)|(sáng\s(((hôm)|(hom))\s)*nay)|(trưa\s(((hôm)|(hom))\s)*nay)|(chiều\s(((hôm)|(hom))\s)*nay)|(tối\s(((hôm)|(hom))\s)*nay)|(((ngày)|(ngay))\s(((hôm)|(hom))\s)*mai)|(sáng\s(((hôm)|(hom))\s)*mai)|(trưa\s(((hôm)|(hom))\s)*mai)|(chiều\s(((hôm)|(hom))\s)*mai)|(tối\s(((hôm)|(hom))\s)*mai)|(((ngày)|(ngay))\s(((hôm)|(hom))\s)*mốt)|(sáng\s(((hôm)|(hom))\s)*mốt)|(trưa\s(((hôm)|(hom))\s)*mốt)|(chiều\s(((hôm)|(hom))\s)*mốt)|(tối\s(((hôm)|(hom))\s)*mốt)|(((ngày)|(ngay))\s(((hôm)|(hom))\s)*kia)|(sáng\s(((hôm)|(hom))\s)*kia)|(trưa\s(((hôm)|(hom))\s)*kia)|(chiều\s(((hôm)|(hom))\s)*kia)|(tối\s(((hôm)|(hom))\s)*kia)|(buổi\ssáng)|(buổi\strưa)|(buổi\schiều)|(buổi\stối)']

    long_time = ['(((tuần)|(tuan))\s((này)|(nay)))|(((tuần)|(tuan))\ssau)|(((tuần)|(tuan))\s((qua)|(rồi)|(roi)|(vừa rồi)))|(((tuần)|(tuan))\s((tới)|(toi)))|(((tháng)|(thang))\s((này)|(nay)))|(((tháng)|(thang))\ssau)|(((tháng)|(thang))\s((qua)|(rồi)|(roi)|(vừa rồi)))|(((tháng)|(thang))\s((tới)|(toi)))']
    
    adj_pattern_top = ['((đầu)|(dau))\s*((tuần)|(tuan)|(tháng)|(thang))']
    adj_pattern_middle = ['((giữa)|(giua))\s*((tuần)|(tuan)|(tháng)|(thang))']
    adj_pattern_bot = ['((cuối)|(cuoi))\s*((tuần)|(tuan)|(tháng)|(thang))']


    return short_time, long_time, adj_pattern_top, adj_pattern_middle, adj_pattern_bot