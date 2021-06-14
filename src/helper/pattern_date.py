def absolute():
    absolute = ['(\d+(,|\s|\.|-|\/|_)+\d+(,|\s|\.|-|\/|_)+\d+)', # 21/03/1997  21-03-1997  21.03.1997
                   '((monday|tuesday|wednesday|thursday|friday|saturday|sunday)(,|\s|\.|-|\/|_)\d+(,|\s|\.|-|\/|_)*\d*(,|\s|\.|-|\/|_)*\d*)', # Monday 21 3 
                ] 
    wod = ['(monday|tuesday|wednesday|friday|saturday|sunday)']
    wod_vn = ['(((thứ)|(thu)|(thuws))(\s+|\.+)*[2-8])|(((thứ)|(thu)|(thuws))(\s+|\.+)*(hai|ba|tư|tu|bốn|bon|năm|nam|lăm|lam|sáu|say|bảy|bay))|((chủ nhật)|(chu nhat)|(cn))']

    day_vn = ['(((ngày)|(ngay)|(ngafy))(\s+|\.+)*(\d\d|\d)($|\s))|(((ngày)|(ngay)|(ngafy))\s+(không|khong|một|mốt|mot|hai|ba|bốn|bon|tư|tu|năm|lăm|nam|lam|sáu|sau|bảy|bay|tám|tam|chín|chin|mười|mươi|muoi)(\s*(không|khong|một|mốt|mot|hai|ba|bốn|bon|tư|tu|năm|lăm|nam|lam|sáu|sau|bảy|bay|tám|tam|chín|chin|mười|mươi|muoi))?(\s*(không|khong|một|mốt|mot|hai|ba|bốn|bon|tư|tu|năm|lăm|nam|lam|sáu|sau|bảy|bay|tám|tam|chín|chin|mười|mươi|muoi))?)']

    month = ['(january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|october|oct|november|nov|december|dec)']
    month_vn = ['(((tháng)|(thang)|(thasng))(\s+|\.+)*(\d\d|\d)($|\s))|(((tháng)|(thang))(\s+|\.+)*(một|mot|hai|ba|bốn|bon|tư|tu|năm|nam|lăm|lam|sáu|bảy|bay|tám|tam|chín|chin|mười|muoi|mười một|muoi mot|mười hai|muoi hai|giêng|gieng|chạp|chap))']

    year = ['('+'|'.join([str(i) for i in list(range(1900, 2050))])+')']

    only_number = ['^\d+$']

    short_abs = ['([0-3][0-9](,|\s|\.|-|\/|_)[0-1][0-9])|((^|\s)\d(,|\s|\.|-|\/|_)\d(\s|$))|([0-3][0-9](,|\s|\.|-|\/|_)[0-9](\s|$))|((^|\s)\d(,|\s|\.|-|\/|_)(1[0-2]))'] # 21 / 03

    return absolute, wod, wod_vn, day_vn, month, month_vn, year, only_number, short_abs

def relative():
    short_time = ['(hôm\s*qua)|(hôm\s*nay)|(hôm\s*kia)|(ngày\s(hôm\s)*qua)|(sáng\s(hôm\s)*qua)|(trưa\s(hôm\s)*qua)|(chiều\s(hôm\s)*qua)|(tối\s(hôm\s)*qua)|(ngày\s(hôm\s)*nay)|(sáng\s(hôm\s)*nay)|(trưa\s(hôm\s)*nay)|(chiều\s(hôm\s)*nay)|(tối\s(hôm\s)*nay)|(ngày\s(hôm\s)*mai)|(sáng\s(hôm\s)*mai)|(trưa\s(hôm\s)*mai)|(chiều\s(hôm\s)*mai)|(tối\s(hôm\s)*mai)|(ngày\s(hôm\s)*mốt)|(sáng\s(hôm\s)*mốt)|(trưa\s(hôm\s)*mốt)|(chiều\s(hôm\s)*mốt)|(tối\s(hôm\s)*mốt)|(ngày\s(hôm\s)*kia)|(sáng\s(hôm\s)*kia)|(trưa\s(hôm\s)*kia)|(chiều\s(hôm\s)*kia)|(tối\s(hôm\s)*kia)|(buổi\ssáng)|(buổi\strưa)|(buổi\schiều)|(buổi\stối)']

    long_time = ['(((tuần)|(tuan))\s((này)|(nay)))|(((tuần)|(tuan))\ssau)|(((tuần)|(tuan))\squa)|(((tuần)|(tuan))\s((tới)|(toi)))|(((tháng)|(thang))\s((này)|(nay)))|(((tháng)|(thang))\ssau)|(((tháng)|(thang))\squa)|(((tháng)|(thang))\s((tới)|(toi)))']
    
    return short_time, long_time