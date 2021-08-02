def get_gender_dict():
    d = {}

    d['male'] = [
        'trai',
        'nam',
        'anh',
        'chú',
        'dượng',
        'cậu',
        'ông',
        'phụ thân',
        'sư thúc',
        'sư phụ',
        'rể'
    ]

    d['female'] = [
        'gái',
        'nữ',
        'chị',  
        'cô',
        'dì',
        'thím',
        'bà',
        'mợ',
        'o',
        'phụ mẫu',
        'sư mẫu',
        'dâu'
    ]
    return d


def get_gender_keys():
    keys = {
        'male': 'GEN01',
        'female': 'GEN02'
    }
    return keys
