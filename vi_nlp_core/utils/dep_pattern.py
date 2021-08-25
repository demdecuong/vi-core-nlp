import os


def get_dep_dict():
    d = {}

    d['SP001'] = [
        'bác sĩ gia đình',
        'bs gia đình',
        'bs gđ',
        'gia đình',
        'y học gia đình',
        'bsgd',
        'family medical'
    ]
    d['SP002'] = [
        'da liễu',
        'da',
        'thẩm mĩ',
        'thẩm mý',
    ]
    d['SP003'] = [
        'dinh dưỡng',
        'dinh dưỡng học đường',
        'ăn uông',
        'suất ăn',
        'chế biến',
        'an toàn vệ sinh thực phẩm',
        'thực phẩm'
    ]
    d['SP004'] = [
        'hô hấp',
        'phổi'
    ]
    d['SP005'] = [
        'nội thận',
        'thận'
    ]
    d['SP006'] = [
        'nhi',
        'em bé',
        'nhi đồng',
    ]
    d['SP007'] = [
        'nội tiết'
    ]
    d['SP008'] = [
        'nội tiêu hóa',
        'tiêu hóa'
    ]
    d['SP009'] = [
        'nội tổng quát'
    ]
    d['SP010'] = [
        'tim mạch',
        'tim'
    ]
    d['SP011'] = [
        'tâm thần'
    ]
    d['SP012'] = [
        'thần kinh'
    ]
    d['SP013'] = [
        'tuyến vú',
        'vú'
    ]
    d['SP014'] = [
        'chẩn đoán hình ảnh',
        'chuẩn đoán hình ảnh',
        'hình ảnh',
        'xquang'
    ]
    d['SP015'] = [
        'chấn thương chỉnh hình',
        'xương khớp',
        'xương',
        'khớp',
        'ngoại'
    ]
    d['SP016'] = [
        'nhiễm',
        'dịch tể',
        'virus'
    ]
    d['SP017'] = [
        'sản phụ khoa',
        'sản phụ',
        'sản',
        'sinh đẻ'
    ]
    d['SP018'] = [
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

    d['SP001'] = [
        'đau bụng', 'sốt', 'ho', 'ói', 'nôn', 'chóng mặt', 'đau ngực', 'đau khớp', 'mất'
        'ngủ', 'lo âu', 'khó thở', 'tăng huyết áp', 'giảm huyết áp', 'cao huyết áp',
        'đau họng,' 'đau khớp', 'mỏi vai gáy', 'mỏi vai', 'tiểu đường', 'mệt',
    ]
    d['SP002'] = [
        'ngứa', 'nổi sẩn', 'da dày sừng', 'bong vảy', 'mụn nước', 'bóng nước', 'chảy dịch',
        'mụn mủ', 'loét', 'mụn trứng cá', 'ngứa da', 'ngứa âm đạo', 'vảy nến',
        'dị ứng', 'phát ban', 'nổi bóng nước', 'phù mặt', 'khó thở', 'mụn', 'nám',
        'mụn cóc', 'đỏ da', 'phát ban', 'dị ứng', 'loét', 'áp-xe', 'hoại tử ', 'nổi nốt', ]
    d['SP003'] = ['béo', 'gầy', 'mập', 'nhẹ cân',
                  'thiếu cân', 'ốm', 'tăng cân', 'suy dinh dưỡng']
    d['SP004'] = ['khó thở', 'đau ngực', 'sốt', 'nôn', 'ho']
    d['SP005'] = ['mệt', 'tiểu đêm', 'đái đêm', 'tăng huyết áp',
                  'đái tháo đường', 'tiểu đường', 'phù, ói', 'nôn', 'khó thở', 'mệt', 'lơ mơ', ]
    d['SP006'] = ['sốt', 'ho', 'ói', 'nôn', 'táo bón', 'sổ mũi', 'tiêu chảy', 'đau bụng', 'nôn ói'
                  'dị ứng', 'nhiễm trùng da', 'tai nạn', 'co giật', 'thở mệt', 'ọc sữa', 'ho',
                  'đau đầu', 'dị ứng', 'viêm da', 'thở khò khè', ]
    d['SP007'] = ['sốt', 'đường huyết cao', 'nhiễm trùng', 'tuyến giáp', 'bệnh tuyến giáp',
                  'sốt', 'đau ngực', 'khó thở', ]
    d['SP008'] = ['đau bụng', 'tiêu chảy', 'nôn', 'táo bón', 'đi ngoài có máu', 'đi ngoài ra máu', 'vàng da',
                  'ói', 'sốt cao', 'lơ mơ', 'ợ chua',
                  'đầy bụng', 'đầy hơi', 'viêm dạ dày', 'loét dạ dày', 'viêm gan', 'viêm gan',
                  'siêu vi', 'viêm gan siêu vi B', 'viêm gan siêu vi C', ]
    d['SP009'] = ['đau ngực', 'ho', 'khó thở', 'đau bụng', 'nôn', 'ói', 'đau đầu', 'sốt', 'huyết áp',
                  'tăng', 'chóng mặt', 'huyết áp cao', 'sốt cao', 'khó thở', 'rối loạn tri',
                          'giác', 'tăng huyết áp', 'rối loạn tiêu hoá', 'đau khớp', 'rối loạn tiền',
                          'đình', 'đái tháo đường', 'bệnh tuyến giáp', 'viêm phế quản', ]
    d['SP010'] = ['đau ngực', 'khó thở', 'hồi hộp', 'chóng mặt', 'phù', 'sốt', 'huyết áp cao',
                  'ho khan', 'phù chân', 'đau ngực', ]
    d['SP011'] = ['mất ngủ', 'tự sát', 'trầm cảm', 'lo âu', 'bồn chồn', 'kích động', 'tự vẫn',
                  'nóng tính', 'nóng tánh', 'tự tử ']
    d['SP012'] = ['đau đầu', 'chóng mặt', 'mất ngủ', 'nói khó', 'khó nói', 'yếu tay',
                  'yếu chân', 'yếu chân tay', 'yếu tay chân', 'hồi hộp', 'tai biến', 
                  'chóng mặt', 'rối loạn ý thức', 'co giật', 'rối loạn ngôn ngữ', 'căng thẳng', 'nhức đầu', 'chóng mặt']
    d['SP013'] = ['u vú', 'đau vú', 'chảy dịch núm vú', ]
    d['SP014'] = ['ho', 'sốt', 'khó thở', 'ho ra máu', 'đau bụng', 'ói', 'nôn', 'tiêu chảy', 'đi ngoài',
                               'táo bón', 'rối loạn tri giác', 'liệt nửa người', 'suy hô hấp', 'x-quang', ]
    d['SP015'] = ['đau lưng', 'đau vai gáy', 'đau gối háng', 'gãy xương', 'trật khớp', 'đau lưng',
                  'thoái hóa khớp', ]
    d['SP016'] = ['sốt', 'đau đầu', 'ói', 'phát ban', 'co giật', 'rối loạn tri giác', 'suy hô hấp',
                  'tiêu chảy', 'đi ngoài', 'thủy đậu', 'quai bị', 'covid-19', ]
    d['SP017'] = ['ngứa âm đạo', 'huyết trắng', 'ngứa âm hộ', ]
    d['SP018'] = ['ho', 'sổ mũi', 'đau họng', 'đau đầu', 'nghẹt mũi', 'mất mùi', 'chảy máu mũi',
                  'khàn tiếng', 'viêm họng', 'viêm xoang', ]

    return d


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SYMPTOMS_PATH = os.path.join(ROOT_DIR, "data/symptoms.txt")


def get_list_of_symps():
    data = []
    with open(SYMPTOMS_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(line.replace('\n', ''))
    return data
