def get_time_pattern():
    # absolute 1 
    # 5:30 , 6:15 , 8:53 , 3:00 , 3.14.52 , 5.21

    # 11 am, 12pm, 1pm, 2:15pm, 3.30pm ,4.45, 5:30, 06:15, 07:30pm, 8:30 pm, 9.15 pm
    abs_pattern =  [
        "(?=((?: |^)[0-2]?\d[:.hg ]?[0-5]\d?(?:|$)))",
        "(?=((?: |^)[0-2]?\d[:.hg]))",
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

