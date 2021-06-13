
def get_date_absolute():
    format_date = ['(\d+(,|\s|\.|-|\/|_)+\d+(,|\s|\.|-|\/|_)+\d+)', # 21/03/1997  21-03-1997  21.03.1997
                    '((monday|tuesday|wednesday|thursday|friday|saturday|sunday)(,|\s|\.|-|\/|_)\d+(,|\s|\.|-|\/|_)*\d*(,|\s|\.|-|\/|_)*\d*)', # Monday 21 3 
                    ] 
    wod = ['(monday|tuesday|wednesday|friday|saturday|sunday)']
    wod_vn = ['(thứ(\s+|\.+)*[2-8])|(thuws(\s+|\.+)*[2-8])|(thu(\s+|\.+)*[2-8])|(thứ(\s+|\.+)*(hai|ba|tư|tu|bốn|bon|năm|nam|lăm|lam|sáu|say|bảy|bay|chủ nhật|chu nhat|cn))']

    day_vn = ['(ngày(\s+|\.+)*(\d\d|\d)($|\s))|(ngay(\s+|\.+)*(\d\d|\d)($|\s))|(ngafy(\s+|\.+)*(\d\d|\d)($|\s))|(ngày\s+(không|khong|một|mốt|mot|hai|ba|bốn|bon|tư|tu|năm|lăm|nam|lam|sáu|sau|bảy|bay|tám|tam|chín|chin|mười|mươi|muoi)(\s(không|khong|một|mốt|mot|hai|ba|bốn|bon|tư|tu|năm|lăm|nam|lam|sáu|sau|bảy|bay|tám|tam|chín|chin|mười|mươi|muoi))*)']

    month = ['(january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|october|oct|november|nov|december|dec)']
    month_vn = ['(tháng(\s+|\.+)*(\d\d|\d)($|\s))|(thang(\s+|\.+)*(\d\d|\d)($|\s))|(thasng(\s+|\.+)*(\d\d|\d)($|\s))|(((tháng)|(thang))(\s+|\.+)*(một|mot|hai|ba|bốn|bon|tư|tu|năm|nam|lăm|lam|sáu|bảy|bay|tám|tam|chín|chin|mười|muoi|mười một|muoi mot|mười hai|muoi hai|giêng|gieng|chạp|chap))']

    year = ['('+'|'.join([str(i) for i in list(range(1900, 2050))])+')']

    only_number = ['^\d+$']

    return format_date, wod, wod_vn, day_vn, month, month_vn, year

def get_date_relative():
    short_time = ['(hôm\s*qua)|(hôm\s*nay)|(hôm\s*kia)|(ngày\s(hôm\s)*qua)|(sáng\s(hôm\s)*qua)|(trưa\s(hôm\s)*qua)|(chiều\s(hôm\s)*qua)|(tối\s(hôm\s)*qua)|(ngày\s(hôm\s)*nay)|(sáng\s(hôm\s)*nay)|(trưa\s(hôm\s)*nay)|(chiều\s(hôm\s)*nay)|(tối\s(hôm\s)*nay)|(ngày\s(hôm\s)*mai)|(sáng\s(hôm\s)*mai)|(trưa\s(hôm\s)*mai)|(chiều\s(hôm\s)*mai)|(tối\s(hôm\s)*mai)|(ngày\s(hôm\s)*mốt)|(sáng\s(hôm\s)*mốt)|(trưa\s(hôm\s)*mốt)|(chiều\s(hôm\s)*mốt)|(tối\s(hôm\s)*mốt)|(ngày\s(hôm\s)*kia)|(sáng\s(hôm\s)*kia)|(trưa\s(hôm\s)*kia)|(chiều\s(hôm\s)*kia)|(tối\s(hôm\s)*kia)|(buổi\ssáng)|(buổi\strưa)|(buổi\schiều)|(buổi\stối)']

    long_time = ['(((tuần)|(tuan))\s((này)|(nay)))|(((tuần)|(tuan))\ssau)|(((tuần)|(tuan))\squa)|(((tuần)|(tuan))\s((tới)|(toi)))|(((tháng)|(thang))\s((này)|(nay)))|(((tháng)|(thang))\ssau)|(((tháng)|(thang))\squa)|(((tháng)|(thang))\s((tới)|(toi)))']
    
    semi_format = ['([0-3][0-9](,|\s|\.|-|\/|_)[0-1][0-9])|((^|\s)\d(,|\s|\.|-|\/|_)\d(\s|$))|([0-3][0-9](,|\s|\.|-|\/|_)[0-9](\s|$))|((^|\s)\d(,|\s|\.|-|\/|_)(1[0-2]))'] # 21 / 03
    
    

    return short_time, long_time, semi_format

def get_person_pattern():
    # 1 person name
    format_explicit = [r"[^()0-9-]+",r"[A-Z][a-z]+,?\s+(?:[A-Z][a-z]*\.?\s*)?[A-Z][a-z]+"] 

    # (tao/tôi/tui/chúbác/cô/dì/ông/bà/em/cậu/dượng/bác sĩ) la [Name]

    format_pronoun1 = [
        ' tao là \.?([^()0-9-]+)',
        ' tao tên \.?([^()0-9-]+)',
        ' tao tên là \.?([^()0-9-]+)',
        ' tao \.?([^()0-9-]+)',
        ' tao : \.?([^()0-9-]+)',
        ' tao: \.?([^()0-9-]+)',
        ' tao là \.?([^()0-9-.*]+)',
        ' tao tên \.?([^()0-9-.*]+)',
        ' tao tên là \.?([^()0-9-.*]+)',
        ' tao \.?([^()0-9-.*]+)',
        ' tao : \.?([^()0-9-.*]+)',
        ' tao: \.?([^()0-9-.*]+)'
        ]

    format_pronoun2 = [
        ' tôi tên là \.?([^()0-9-]+)',
        ' tôi tên là \.?([^()0-9-.*]+)',
        ' tôi tên \.?([^()0-9-]+)',
        ' tôi tên \.?([^()0-9-.*]+)',
        ' tôi là \.?([^()0-9-]+)',
        ' tôi là \.?([^()0-9-.*]+)',
        ' tôi : \.?([^()0-9-.*]+)',
        ' tôi : \.?([^()0-9-]+)',
        ' tôi: \.?([^()0-9-.*]+)',
        ' tôi: \.?([^()0-9-]+)',
        ' tôi \.?([^()0-9-.*]+)',
        ' tôi \.?([^()0-9-]+)', 
    ]
    format_pronoun3 = [
        ' tui tên là \.?([^()0-9-]+)',
        ' tui là \.?([^()0-9-]+)',
        ' tui tên \.?([^()0-9-]+)',
        ' tui \.?([^()0-9-]+)',
        ' tui : \.?([^()0-9-]+)',
        ' tui: \.?([^()0-9-]+)',
        ' tui là \.?([^()0-9-.*]+)',
        ' tui tên \.?([^()0-9-.*]+)',
        ' tui tên là \.?([^()0-9-.*]+)',
        ' tui \.?([^()0-9-.*]+)',
        ' tui : \.?([^()0-9-.*]+)',
        ' tui: \.?([^()0-9-.*]+)'
    ]
    format_pronoun4 = [
        ' chú là \.?([^()0-9-]+)',
        ' chú tên \.?([^()0-9-]+)',
        ' chú tên là \.?([^()0-9-]+)',
        ' chú \.?([^()0-9-]+)',
        ' chú : \.?([^()0-9-]+)',
        ' chú: \.?([^()0-9-]+)',       
        ' chú là \.?([^()0-9-.*]+)',
        ' chú tên \.?([^()0-9-.*]+)',
        ' chú tên là \.?([^()0-9-.*]+)',
        ' chú \.?([^()0-9-.*]+)',
        ' chú : \.?([^()0-9-.*]+)',
        ' chú: \.?([^()0-9-.*]+)',
    ]
    format_pronoun5 = [
        'bác là \.?([^()0-9-]+)',
        'bác tên \.?([^()0-9-]+)',
        'bác tên là \.?([^()0-9-]+)',
        'bác \.?([^()0-9-]+)',
        'bác : \.?([^()0-9-]+)',
        'bác: \.?([^()0-9-]+)',   
        'bác là \.?([^()0-9-.*]+)',
        'bác tên \.?([^()0-9-.*]+)',
        'bác tên là \.?([^()0-9-.*]+)',
        'bác \.?([^()0-9-.*]+)',
        'bác : \.?([^()0-9-.*]+)',
        'bác: \.?([^()0-9-.*]+)'
    ]
    format_pronoun6 = [
        ' dì là \.?([^()0-9-]+)',
        ' dì tên \.?([^()0-9-]+)',
        ' dì tên là \.?([^()0-9-]+)',
        ' dì \.?([^()0-9-]+)',
        ' dì : \.?([^()0-9-]+)',
        ' dì: \.?([^()0-9-]+)',   
        ' dì là \.?([^()0-9-.*]+)',
        ' dì tên \.?([^()0-9-.*]+)',
        ' dì tên là \.?([^()0-9-.*]+)',
        ' dì \.?([^()0-9-.*]+)',
        ' dì : \.?([^()0-9-.*]+)',
        ' dì: \.?([^()0-9-.*]+)'
    ]
    format_pronoun7 = [
        ' ông là \.?([^()0-9-]+)',
        ' ông tên \.?([^()0-9-]+)',
        ' ông tên là \.?([^()0-9-]+)',
        ' ông \.?([^()0-9-]+)',
        ' ông : \.?([^()0-9-]+)',
        ' ông: \.?([^()0-9-]+)', 
        ' ông là \.?([^()0-9-.*]+)',
        ' ông tên \.?([^()0-9-.*]+)',
        ' ông tên là \.?([^()0-9-.*]+)',
        ' ông \.?([^()0-9-.*]+)',
        ' ông : \.?([^()0-9-.*]+)',
        ' ông: \.?([^()0-9-.*]+)'
    ]
    format_pronoun8 = [
        ' bà là \.?([^()0-9-]+)',
        ' bà tên \.?([^()0-9-]+)',
        ' bà tên là \.?([^()0-9-]+)',
        ' bà \.?([^()0-9-]+)',
        ' bà : \.?([^()0-9-]+)',
        ' bà: \.?([^()0-9-]+)', 
        ' bà là \.?([^()0-9-.*]+)',
        ' bà tên \.?([^()0-9-.*]+)',
        ' bà tên là \.?([^()0-9-.*]+)',
        ' bà \.?([^()0-9-.*]+)',
        ' bà : \.?([^()0-9-.*]+)',
        ' bà: \.?([^()0-9-.*]+)'
    ]
    format_pronoun9 = [
        ' em tên là \.?([^()0-9-.*]+)',
        ' em \.?([^()0-9-]+)',
        ' em là \.?([^()0-9-]+)',
        ' em tên \.?([^()0-9-]+)',
        ' em tên là \.?([^()0-9-]+)',
        ' em : \.?([^()0-9-]+)',
        ' em: \.?([^()0-9-]+)', 
        ' em là \.?([^()0-9-.*]+)',
        ' em tên \.?([^()0-9-.*]+)',
        ' em \.?([^()0-9-.*]+)',
        ' em : \.?([^()0-9-.*]+)',
        ' em: \.?([^()0-9-.*]+)'
    ]
    format_pronoun10 = [
        ' cậu \.?([^()0-9-]+)',
        ' cậu tên \.?([^()0-9-]+)',
        ' cậu là \.?([^()0-9-]+)',
        ' cậu tên là \.?([^()0-9-]+)',
        ' cậu : \.?([^()0-9-]+)',
        ' cậu: \.?([^()0-9-]+)', 
        ' cậu là \.?([^()0-9-.*]+)',
        ' cậu tên \.?([^()0-9-.*]+)',
        ' cậu tên là \.?([^()0-9-.*]+)',
        ' cậu \.?([^()0-9-.*]+)',
        ' cậu : \.?([^()0-9-.*]+)',
        ' cậu: \.?([^()0-9-.*]+)'
    ]
    format_pronoun11 = [
        ' dượng \.?([^()0-9-]+)',
        ' dượng tên \.?([^()0-9-]+)',
        ' dượng là \.?([^()0-9-]+)',
        ' dượng tên là \.?([^()0-9-]+)',
        ' dượng : \.?([^()0-9-]+)',
        ' dượng: \.?([^()0-9-]+)', 
        ' dượng là \.?([^()0-9-.*]+)',
        ' dượng tên \.?([^()0-9-.*]+)',
        ' dượng tên là \.?([^()0-9-.*]+)',
        ' dượng \.?([^()0-9-.*]+)',
        ' dượng : \.?([^()0-9-.*]+)',
        ' dượng: \.?([^()0-9-.*]+)'
    ]
    format_pronoun12 = [
        ' bác sĩ \.?([^()0-9-]+)',
        ' bác sĩ tên \.?([^()0-9-]+)',
        ' bác sĩ là \.?([^()0-9-]+)',
        ' bác sĩ tên là \.?([^()0-9-]+)',
        ' bác sĩ : \.?([^()0-9-]+)',
        ' bác sĩ: \.?([^()0-9-]+)', 
        ' bác sĩ là \.?([^()0-9-.*]+)',
        ' bác sĩ tên \.?([^()0-9-.*]+)',
        ' bác sĩ tên là \.?([^()0-9-.*]+)',
        ' bác sĩ \.?([^()0-9-.*]+)',
        ' bác sĩ : \.?([^()0-9-.*]+)',
        ' bác sĩ: \.?([^()0-9-.*]+)',
    ]
    # (tên/tên là/tên :) la [Name]
    format_semi_pronoun = [
        ' tên là \.?([^()0-9-]+)',
        ' là \.?([^()0-9-]+)',
        ' tên \.?([^()0-9-]+)',
        ' tên : \.?([^()0-9-]+)',
        ' tên là \.?([^()0-9-.*]+)',
        ' là \.?([^()0-9-.*]+)',
        ' tên \.?([^()0-9-.*]+)',
        ' tên : \.?([^()0-9-.*]+)',
    ]

    matches = [
        'tao',
        'tôi',
        'tui',
        'chú',
        'bác',
        'cô',
        'dì',
        'ông',
        'bà',
        'em',
        'cậu',
        'dượng',
        'bác sĩ',
        'tên',
        'là',
    ]

    format_pronoun = [
        format_pronoun12,
        format_pronoun1,
        format_pronoun2,
        format_pronoun3,
        format_pronoun5,
        format_pronoun7,
        format_pronoun9,
        format_pronoun4,
        format_pronoun6,
        format_pronoun8,
        format_pronoun10,
        format_pronoun11,
    ]

    return format_explicit, format_pronoun, format_semi_pronoun, matches

def get_phone_pattern():
    pattern = r"(84|0[3|5|7|8|9])+([0-9]{8})\b"
    return pattern

def get_time_pattern():
    # absolute 1 
    # 5:30 , 6:15 , 8:53 , 3:00 , 3.14.52 , 5.21

    # 11 am, 12pm, 1pm, 2:15pm, 3.30pm ,4.45, 5:30, 06:15, 07:30pm, 8:30 pm, 9.15 pm
    abs_pattern =  [
        "(?=((?: |^)[0-2]?\d[:.hg ]?[0-5]\d?(?:|$)))",
        "(?=((?: |^)[0-2]?\d[:.hg ]?[0-5]\d?(?= giờ|tiếng)\d?(?:|$)))"
    ]

    # contains giờ (logic)
    #   - sáng/chiều/tối (8 giờ chieu)
    #   - tám giờ chiều (số --> chữ)
    #   - 
    #   - 

    # extract AM or PM
    am_pattern = ['am','sáng', 'giờ sáng', 'buổi sáng', 'sunup', 'morning']
    pm_pattern = ['pm','tối','chiều','buổi chiều', 'buổi tối', 'giờ chiều', 'giờ tối' ,'trưa', 'buổi trưa', 'giờ trưa', 'xế chiều', 'chiều tà', 'noon','afternoon','evening']
    
    # relative : 
    # 2 giờ nữa, 15 phút nữa 

    relative_pattern = []
    return abs_pattern, am_pattern, pm_pattern

