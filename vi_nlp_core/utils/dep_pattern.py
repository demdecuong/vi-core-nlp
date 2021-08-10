def get_dep_dict():
    d = {}

    d['bác sĩ gia đình'] = [
        'bác sĩ gia đình',
        'bs gia đình',
        'bs gđ',
        'gia đình',
        'y học gia đình',
        'bsgd',
        'family medical'
    ]
    d['da liễu'] = [
        'da liễu',
        'da',
        'thẩm mĩ',
        'thẩm mý',
    ]
    d['dinh dưỡng'] = [
        'dinh dưỡng',
        'dinh dưỡng học đường',
        'ăn uông',
        'suất ăn',
        'chế biến',
        'an toàn vệ sinh thực phẩm',
        'thực phẩm'
    ]
    d['hô hấp'] = [
        'hô hấp',
        'phổi'
    ]
    d['nội thận'] = [
        'nội thận',
        'thận'
    ]
    d['nhi'] = [
        'nhi',
        'em bé',
        'nhi đồng',
    ]
    d['nội tiết'] = [
        'nội tiết'
    ]
    d['nội tiêu hóa'] = [
        'nội tiêu hóa',
        'tiêu hóa'
    ]
    d['nội tổng quát'] = [
        'nội tổng quát'
    ]
    d['tim mạch'] = [
        'tim mạch',
        'tim'
    ]
    d['tâm thần'] = [
        'tâm thần'
    ]
    d['thần kinh'] = [
        'thần kinh'
    ]
    d['tuyến vú'] = [
        'tuyến vú',
        'vú'
    ]
    d['chẩn đoán hình ảnh'] = [
        'chẩn đoán hình ảnh',
        'chuẩn đoán hình ảnh',
        'hình ảnh',
        'xquang'
    ]
    d['chấn thương chỉnh hình'] = [
        'chấn thương chỉnh hình',
        'xương khớp',
        'xương',
        'khớp',
        'ngoại'
    ]
    d['nhiễm'] = [
        'nhiễm',
        'dịch tể',
        'virus'
    ]
    d['sản phụ khoa'] = [
        'sản phụ khoa',
        'sản phụ',
        'sản',
        'sinh đẻ'
    ]
    d['tai mũi họng'] = [
        'tai mũi họng',
        'mũi',
        'họng',
    ]

    return d


def get_dep_keys():
    keys = {
        'bác sĩ gia đình': 'SP001',
        'da liễu': 'SP002',
        'dinh dưỡng': 'SP003',
        'hô hấp': 'SP004',
        'nội thận': 'SP005',
        'nhi': 'SP006',
        'nội tiết': 'SP007',
        'nội tiêu hóa': 'SP008',
        'nội tổng quát': 'SP009',
        'tim mạch': 'SP010',
        'tâm thần': 'SP011',
        'thần kinh': 'SP012',
        'tuyến vú': 'SP013',
        'chẩn đoán hình ảnh': 'SP014',
        'chấn thương chỉnh hình': 'SP015',
        'nhiễm': 'SP016',
        'sản phụ khoa': 'SP017',
        'tai mũi họng': 'SP018',
    }
    return keys


def get_dep_symptoms_dict():
    d = {}

    d['bác sĩ gia đình'] = [
        'đau bụng', 'sốt', 'ho', 'ói', 'nôn', 'chóng mặt', 'đau ngực', 'đau khớp', 'mất'
        'ngủ', 'lo âu', 'khó thở', 'tăng huyết áp', 'giảm huyết áp', 'cao huyết áp',
        'đau họng,' 'đau khớp', 'mỏi vai gáy', 'mỏi vai', 'tiểu đường', 'mệt',
    ]
    d['da liễu'] = [
        'ngứa', 'nổi sẩn', 'da dày sừng', 'bong vảy', 'mụn nước', 'bóng nước', 'chảy dịch',
        'mụn mủ', 'loét', 'mụn trứng cá', 'ngứa da', 'ngứa âm đạo', 'vảy nến',
        'dị ứng', 'phát ban', 'nổi bóng nước', 'phù mặt', 'khó thở', 'mụn', 'nám',
        'mụn cóc', 'đỏ da', 'phát ban', 'dị ứng', 'loét', 'áp-xe', 'hoại tử ', 'nổi nốt', ]
    d['dinh dưỡng'] = ['béo', 'gầy', 'mập', 'nhẹ cân',
                       'thiếu cân', 'ốm', 'tăng cân', 'suy dinh dưỡng']
    d['hô hấp'] = ['khó thở', 'đau ngực', 'sốt', 'nôn', 'ho']
    d['nội thận'] = ['mệt', 'tiểu đêm', 'đái đêm', 'tăng huyết áp',
                     'đái tháo đường', 'tiểu đường', 'phù, ói', 'nôn', 'khó thở', 'mệt', 'lơ mơ', ]
    d['nhi'] = ['sốt', 'ho', 'ói', 'nôn', 'táo bón', 'sổ mũi', 'tiêu chảy', 'đau bụng', 'nôn ói'
                'dị ứng', 'nhiễm trùng da', 'tai nạn', 'co giật', 'thở mệt', 'ọc sữa', 'ho',
                'đau đầu', 'dị ứng', 'viêm da', 'thở khò khè', ]
    d['nội tiết'] = ['sốt', 'đường huyết cao', 'nhiễm trùng', 'tuyến giáp', 'bệnh tuyến giáp',
                     'sốt', 'đau ngực', 'khó thở', ]
    d['nội tiêu hóa'] = ['đau bụng', 'tiêu chảy', 'nôn', 'táo bón', 'đi ngoài có máu', 'đi ngoài ra máu', 'vàng da',
                         'nhức đầu', 'chóng mặt', 'ói', 'sốt cao', 'lơ mơ', 'ợ chua',
                         'đầy bụng', 'đầy hơi', 'viêm dạ dày', 'loét dạ dày', 'viêm gan', 'viêm gan',
                         'siêu vi', 'viêm gan siêu vi B', 'viêm gan siêu vi C', ]
    d['nội tổng quát'] = ['đau ngực', 'ho', 'khó thở', 'đau bụng', 'nôn', 'ói', 'đau đầu', 'sốt', 'huyết áp',
                          'tăng', 'chóng mặt', 'huyết áp cao', 'sốt cao', 'khó thở', 'rối loạn tri',
                          'giác', 'tăng huyết áp', 'rối loạn tiêu hoá', 'đau khớp', 'rối loạn tiền',
                          'đình', 'đái tháo đường', 'bệnh tuyến giáp', 'viêm phế quản', ]
    d['tim mạch'] = ['đau ngực', 'khó thở', 'hồi hộp', 'chóng mặt', 'phù', 'sốt', 'huyết áp cao',
                     'ho khan', 'phù chân', 'đau ngực', ]
    d['tâm thần'] = ['mất ngủ', 'tự sát', 'trầm cảm', 'lo âu', 'bồn chồn', 'kích động', 'tự vẫn',
                     'nóng tính', 'nóng tánh', 'tự tử ']
    d['thần kinh'] = ['đau đầu', 'chóng mặt', 'mất ngủ', 'nói khó', 'khó nói', 'yếu tay',
                      'yếu chân', 'yếu chân tay', 'yếu tay chân', 'hồi hộp', 'tai biến',  'đau đầu',
                      'chóng mặt', 'rối loạn ý thức', 'co giật', 'rối loạn ngôn ngữ','căng thẳng' ]
    d['tuyến vú'] = ['u vú', 'đau vú', 'chảy dịch núm vú', ]
    d['chẩn đoán hình ảnh'] = ['ho', 'sốt', 'khó thở', 'ho ra máu', 'đau bụng', 'ói', 'nôn', 'tiêu chảy', 'đi ngoài',
                               'táo bón', 'rối loạn tri giác', 'liệt nửa người', 'suy hô hấp', 'x-quang', ]
    d['chấn thương chỉnh hình'] = ['đau lưng', 'đau vai gáy', 'đau gối háng', 'gãy xương', 'trật khớp', 'đau lưng',
                                   'thoái hóa khớp', ]
    d['nhiễm'] = ['sốt', 'đau đầu', 'ói', 'phát ban', 'co giật', 'rối loạn tri giác', 'suy hô hấp',
                  'tiêu chảy', 'đi ngoài', 'thủy đậu', 'quai bị', 'covid-19', ]
    d['sản phụ khoa'] = ['ngứa âm đạo', 'huyết trắng', 'ngứa âm hộ', ]
    d['tai mũi họng'] = ['ho', 'sổ mũi', 'đau họng', 'đau đầu', 'nghẹt mũi', 'mất mùi', 'chảy máu mũi',
                         'khàn tiếng', 'viêm họng', 'viêm xoang', ]

    return d

def get_list_of_symps(path="vi_nlp_core/utils/symptoms.txt"):
    data = []
    with open(path,'r',encoding='utf-8') as f:
        for line in f:
            data.append(line.replace('\n',''))
    return data 