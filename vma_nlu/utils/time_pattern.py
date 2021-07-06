def get_time_pattern():
    # absolute 1 
    # 5:30 , 6:15 , 8:53 , 3:00 , 3.14.52 , 5.21

    # 11 am, 12pm, 1pm, 2:15pm, 3.30pm ,4.45, 5:30, 06:15, 07:30pm, 8:30 pm, 9.15 pm
    # abs_pattern =  [
    #     "(?=((?: |^|\s*)[0-2]?\d[:.hg]))",
    #     "(?=((?: |^|\s*)[0-2]?\d[:.hg ]?[0-5]\d?(?:|$)))",
    #     "(?=((?: |^|\s*)[0-2]?\d[:.hg ]?[0-5]\d?(?= giờ|tiếng)\d?(?:|$)))"
    # ]
    abs_pattern = [
        '((\d?\d[:.hg]\s*\d\d?)(?=\s|$|p|a))|((\d?\d[:.hg])(?=\s|$|p|a))'
    ]

    # contains giờ (logic)
    #   - sáng/chiều/tối (8 giờ chieu)
    #   - tám giờ chiều (số --> chữ)
    #   - 
    #   - 

    # extract AM or PM
    am_pattern = ['am','sáng', 'giờ sáng', 'buổi sáng', 'sunup', 'morning']
    pm_pattern = ['pm','tối','chiều','buổi chiều', 'buổi tối', 'giờ chiều', 'giờ tối' ,'trưa', 'buổi trưa', 'giờ trưa', 'xế chiều', 'chiều tà', 'noon','afternoon','evening']
    

    # special : cuoi buoi sang cuoi buoi chieu
    first_spec_pattern = {
        'đầu giờ sáng'      : '7h00',
        'đầu buổi sáng'     : '7h00',
        'đầu giờ chiều'     : '13h30', 
        'đầu buổi chiều'    : '13h30', 
        
    }
    mid_spec_pattern = {
        'giữa giờ sáng'     : '9h',
        'giữa buổi sáng'    : '9h',
        'giữa buổi chiều'   : '9h',
        'giữa giờ chiều'    : '9h',
    }

    last_spec_pattern = {
        'cuối giờ sáng'     : '11h00',
        'cuối buổi sáng'    : '11h00',
        'cuối giờ chiều'    : '17h00', 
        'cuối buổi chiều'   : '17h00',
    } 
    spec_pattern = [
        first_spec_pattern,
        mid_spec_pattern,
        last_spec_pattern
    ] 
    
    relative_pattern = []
    return abs_pattern, am_pattern, pm_pattern

