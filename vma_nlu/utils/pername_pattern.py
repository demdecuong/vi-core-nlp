
def get_person_pattern():
    # 1 person name
    format_explicit = [r"[^()0-9-]+",r"[A-Z][a-z]+,?\s+(?:[A-Z][a-z]*\.?\s*)?[A-Z][a-z]+"] 

    # (tao/tôi/tui/chúbác/cô/dì/ông/bà/em/cậu/dượng/bác sĩ) la [Name]

    format_pronoun1 = [
        ' tao là \.?([^()0-9-.,!*]+)',
        ' tao tên \.?([^()0-9-.,!*]+)',
        ' tao tên là \.?([^()0-9-.,!*]+)',
        ' tao \.?([^()0-9-.,!*]+)',
        ' tao : \.?([^()0-9-.,!*]+)',
        ' tao: \.?([^()0-9-.,!*]+)',
        'tao là \.?([^()0-9-.,!*]+)',
        'tao tên \.?([^()0-9-.,!*]+)',
        'tao tên là \.?([^()0-9-.,!*]+)',
        'tao \.?([^()0-9-.,!*]+)',
        'tao : \.?([^()0-9-.,!*]+)',
        'tao: \.?([^()0-9-.,!*]+)',
        ]

    format_pronoun2 = [
        ' tôi tên là \.?([^()0-9-.,!*]+)',
        ' tôi tên \.?([^()0-9-.,!*]+)',
        ' tôi là \.?([^()0-9-.,!*]+)',
        ' tôi : \.?([^()0-9-.,!*]+)',
        ' tôi: \.?([^()0-9-.,!*]+)',
        ' tôi \.?([^()0-9-.,!*]+)',
        'tôi tên là \.?([^()0-9-.,!*]+)',
        'tôi tên \.?([^()0-9-.,!*]+)',
        'tôi là \.?([^()0-9-.,!*]+)',
        'tôi : \.?([^()0-9-.,!*]+)',
        'tôi: \.?([^()0-9-.,!*]+)',
        'tôi \.?([^()0-9-.,!*]+)',
    ]
    format_pronoun3 = [
        ' tui tên là \.?([^()0-9-.,!*]+)',
        ' tui là \.?([^()0-9-.,!*]+)',
        ' tui tên \.?([^()0-9-.,!*]+)',
        ' tui \.?([^()0-9-.,!*]+)',
        ' tui : \.?([^()0-9-.,!*]+)',
        ' tui: \.?([^()0-9-.,!*]+)',
        'tui tên là \.?([^()0-9-.,!*]+)',
        'tui là \.?([^()0-9-.,!*]+)',
        'tui tên \.?([^()0-9-.,!*]+)',
        'tui \.?([^()0-9-.,!*]+)',
        'tui : \.?([^()0-9-.,!*]+)',
        'tui: \.?([^()0-9-.,!*]+)',
    ]
    format_pronoun4 = [
        ' chú là \.?([^()0-9-.,!*]+)',
        ' chú tên \.?([^()0-9-.,!*]+)',
        ' chú tên là \.?([^()0-9-.,!*]+)',
        ' chú \.?([^()0-9-.,!*]+)',
        ' chú : \.?([^()0-9-.,!*]+)',
        ' chú: \.?([^()0-9-.,!*]+)', 
        'chú là \.?([^()0-9-.,!*]+)',
        'chú tên \.?([^()0-9-.,!*]+)',
        'chú tên là \.?([^()0-9-.,!*]+)',
        'chú \.?([^()0-9-.,!*]+)',
        'chú : \.?([^()0-9-.,!*]+)',
        'chú: \.?([^()0-9-.,!*]+)',
    ]
    format_pronoun5 = [
        ' bác là \.?([^()0-9-.,!*]+)',
        ' bác tên \.?([^()0-9-.,!*]+)',
        ' bác tên là \.?([^()0-9-.,!*]+)',
        ' bác \.?([^()0-9-.,!*]+)',
        ' bác : \.?([^()0-9-.,!*]+)',
        ' bác: \.?([^()0-9-.,!*]+)',
        'bác là \.?([^()0-9-.,!*]+)',
        'bác tên \.?([^()0-9-.,!*]+)',
        'bác tên là \.?([^()0-9-.,!*]+)',
        'bác \.?([^()0-9-.,!*]+)',
        'bác : \.?([^()0-9-.,!*]+)',
        'bác: \.?([^()0-9-.,!*]+)',
    ]
    format_pronoun6 = [
        ' dì là \.?([^()0-9-.,!*]+)',
        ' dì tên \.?([^()0-9-.,!*]+)',
        ' dì tên là \.?([^()0-9-.,!*]+)',
        ' dì \.?([^()0-9-.,!*]+)',
        ' dì : \.?([^()0-9-.,!*]+)',
        ' dì: \.?([^()0-9-.,!*]+)',
        'dì là \.?([^()0-9-.,!*]+)',
        'dì tên \.?([^()0-9-.,!*]+)',
        'dì tên là \.?([^()0-9-.,!*]+)',
        'dì \.?([^()0-9-.,!*]+)',
        'dì : \.?([^()0-9-.,!*]+)',
        'dì: \.?([^()0-9-.,!*]+)',
    ]
    format_pronoun7 = [
        ' ông là \.?([^()0-9-.,!*]+)',
        ' ông tên \.?([^()0-9-.,!*]+)',
        ' ông tên là \.?([^()0-9-.,!*]+)',
        ' ông \.?([^()0-9-.,!*]+)',
        ' ông : \.?([^()0-9-.,!*]+)',
        ' ông: \.?([^()0-9-.,!*]+)', 
        'ông là \.?([^()0-9-.,!*]+)',
        'ông tên \.?([^()0-9-.,!*]+)',
        'ông tên là \.?([^()0-9-.,!*]+)',
        'ông \.?([^()0-9-.,!*]+)',
        'ông : \.?([^()0-9-.,!*]+)',
        'ông: \.?([^()0-9-.,!*]+)', 
    ]
    format_pronoun8 = [
        ' bà là \.?([^()0-9-.,!*]+)',
        ' bà tên \.?([^()0-9-.,!*]+)',
        ' bà tên là \.?([^()0-9-.,!*]+)',
        ' bà \.?([^()0-9-.,!*]+)',
        ' bà : \.?([^()0-9-.,!*]+)',
        ' bà: \.?([^()0-9-.,!*]+)',
        'bà là \.?([^()0-9-.,!*]+)',
        'bà tên \.?([^()0-9-.,!*]+)',
        'bà tên là \.?([^()0-9-.,!*]+)',
        'bà \.?([^()0-9-.,!*]+)',
        'bà : \.?([^()0-9-.,!*]+)',
        'bà: \.?([^()0-9-.,!*]+)',
    ]
    format_pronoun9 = [
        ' em tên là \.?([^()0-9-.,!*]+)',
        ' em \.?([^()0-9-.,!*]+)',
        ' em là \.?([^()0-9-.,!*]+)',
        ' em tên \.?([^()0-9-.,!*]+)',
        ' em tên là \.?([^()0-9-.,!*]+)',
        ' em : \.?([^()0-9-.,!*]+)',
        ' em: \.?([^()0-9-.,!*]+)', 
        'em tên là \.?([^()0-9-.,!*]+)',
        'em \.?([^()0-9-.,!*]+)',
        'em là \.?([^()0-9-.,!*]+)',
        'em tên \.?([^()0-9-.,!*]+)',
        'em tên là \.?([^()0-9-.,!*]+)',
        'em : \.?([^()0-9-.,!*]+)',
        'em: \.?([^()0-9-.,!*]+)', 
    ]
    format_pronoun10 = [
        ' cậu \.?([^()0-9-]+)',
        ' cậu tên \.?([^()0-9-]+)',
        ' cậu là \.?([^()0-9-]+)',
        ' cậu tên là \.?([^()0-9-]+)',
        ' cậu : \.?([^()0-9-.,!*]+)',
        ' cậu: \.?([^()0-9-.,!*]+)', 
        'cậu \.?([^()0-9-]+)',
        'cậu tên \.?([^()0-9-]+)',
        'cậu là \.?([^()0-9-]+)',
        'cậu tên là \.?([^()0-9-]+)',
        'cậu : \.?([^()0-9-.,!*]+)',
        'cậu: \.?([^()0-9-.,!*]+)', 
    ]
    format_pronoun11 = [
        ' dượng \.?([^()0-9-.,!*]+)',
        ' dượng tên \.?([^()0-9-.,!*]+)',
        ' dượng là \.?([^()0-9-.,!*]+)',
        ' dượng tên là \.?([^()0-9-.,!*]+)',
        ' dượng : \.?([^()0-9-.,!*]+)',
        ' dượng: \.?([^()0-9-.,!*]+)', 
        'dượng \.?([^()0-9-.,!*]+)',
        'dượng tên \.?([^()0-9-.,!*]+)',
        'dượng là \.?([^()0-9-.,!*]+)',
        'dượng tên là \.?([^()0-9-.,!*]+)',
        'dượng : \.?([^()0-9-.,!*]+)',
        'dượng: \.?([^()0-9-.,!*]+)', 
    ]
    format_pronoun12 = [
        ' bác sĩ \.?([^()0-9-.,!*]+)',
        ' bác sĩ tên \.?([^()0-9-.,!*]+)',
        ' bác sĩ là \.?([^()0-9-.,!*]+)',
        ' bác sĩ tên là \.?([^()0-9-.,!*]+)',
        ' bác sĩ : \.?([^()0-9-.,!*]+)',
        ' bác sĩ: \.?([^()0-9-.,!*]+)', 
        'bác sĩ \.?([^()0-9-.,!*]+)',
        'bác sĩ tên \.?([^()0-9-.,!*]+)',
        'bác sĩ là \.?([^()0-9-.,!*]+)',
        'bác sĩ tên là \.?([^()0-9-.,!*]+)',
        'bác sĩ : \.?([^()0-9-.,!*]+)',
        'bác sĩ: \.?([^()0-9-.,!*]+)', 
    ]
    
    format_pronoun13 = [
        ' bs \.?([^()0-9-.,!*]+)',
        ' bs tên \.?([^()0-9-.,!*]+)',
        ' bs là \.?([^()0-9-.,!*]+)',
        ' bs tên là \.?([^()0-9-.,!*]+)',
        ' bs: \.?([^()0-9-.,!*]+)', 
        ' bs : \.?([^()0-9-.,!*]+)',
        'bs \.?([^()0-9-.,!*]+)',
        'bs tên \.?([^()0-9-.,!*]+)',
        'bs là \.?([^()0-9-.,!*]+)',
        'bs tên là \.?([^()0-9-.,!*]+)',
        'bs: \.?([^()0-9-.,!*]+)', 
        'bs : \.?([^()0-9-.,!*]+)',
    ]

    format_pronoun14 = [
        ' bsi \.?([^()0-9-.,!*]+)',
        ' bsi tên \.?([^()0-9-.,!*]+)',
        ' bsi là \.?([^()0-9-.,!*]+)',
        ' bsi tên là \.?([^()0-9-.,!*]+)',
        ' bsi : \.?([^()0-9-.,!*]+)',
        ' bsi: \.?([^()0-9-.,!*]+)', 
        'bsi \.?([^()0-9-.,!*]+)',
        'bsi tên \.?([^()0-9-.,!*]+)',
        'bsi là \.?([^()0-9-.,!*]+)',
        'bsi tên là \.?([^()0-9-.,!*]+)',
        'bsi : \.?([^()0-9-.,!*]+)',
        'bsi: \.?([^()0-9-.,!*]+)', 
    ]

    format_pronoun15 = [
        ' bacsi \.?([^()0-9-.,!*]+)',
        ' bacsi tên \.?([^()0-9-.,!*]+)',
        ' bacsi là \.?([^()0-9-.,!*]+)',
        ' bacsi tên là \.?([^()0-9-.,!*]+)',
        ' bacsi : \.?([^()0-9-.,!*]+)',
        ' bacsi: \.?([^()0-9-.,!*]+)', 
        'bacsi \.?([^()0-9-.,!*]+)',
        'bacsi tên \.?([^()0-9-.,!*]+)',
        'bacsi là \.?([^()0-9-.,!*]+)',
        'bacsi tên là \.?([^()0-9-.,!*]+)',
        'bacsi : \.?([^()0-9-.,!*]+)',
        'bacsi: \.?([^()0-9-.,!*]+)', 
    ]

    format_pronoun16 = [
        ' dr \.?([^()0-9-.,!*]+)',
        ' dr tên \.?([^()0-9-.,!*]+)',
        ' dr là \.?([^()0-9-.,!*]+)',
        ' dr tên là \.?([^()0-9-.,!*]+)',
        ' dr : \.?([^()0-9-.,!*]+)',
        ' dr: \.?([^()0-9-.,!*]+)', 
        'dr \.?([^()0-9-.,!*]+)',
        'dr tên \.?([^()0-9-.,!*]+)',
        'dr là \.?([^()0-9-.,!*]+)',
        'dr tên là \.?([^()0-9-.,!*]+)',
        'dr : \.?([^()0-9-.,!*]+)',
        'dr: \.?([^()0-9-.,!*]+)', 
    ]
    format_pronoun17 = [
        ' mr \.?([^()0-9-.,!*]+)',
        ' mr tên \.?([^()0-9-.,!*]+)',
        ' mr là \.?([^()0-9-.,!*]+)',
        ' mr tên là \.?([^()0-9-.,!*]+)',
        ' mr : \.?([^()0-9-.,!*]+)',
        ' mr: \.?([^()0-9-.,!*]+)', 
        'mr \.?([^()0-9-.,!*]+)',
        'mr tên \.?([^()0-9-.,!*]+)',
        'mr là \.?([^()0-9-.,!*]+)',
        'mr tên là \.?([^()0-9-.,!*]+)',
        'mr : \.?([^()0-9-.,!*]+)',
        'mr: \.?([^()0-9-.,!*]+)', 
    ]
    format_pronoun18 = [
        ' mrs \.?([^()0-9-.,!*]+)',
        ' mrs tên \.?([^()0-9-.,!*]+)',
        ' mrs là \.?([^()0-9-.,!*]+)',
        ' mrs tên là \.?([^()0-9-.,!*]+)',
        ' mrs : \.?([^()0-9-.,!*]+)',
        ' mrs: \.?([^()0-9-.,!*]+)', 
        'mrs \.?([^()0-9-.,!*]+)',
        'mrs tên \.?([^()0-9-.,!*]+)',
        'mrs là \.?([^()0-9-.,!*]+)',
        'mrs tên là \.?([^()0-9-.,!*]+)',
        'mrs : \.?([^()0-9-.,!*]+)',
        'mrs: \.?([^()0-9-.,!*]+)', 
    ]
    format_pronoun19 = [
        ' ms \.?([^()0-9-.,!*]+)',
        ' ms tên \.?([^()0-9-.,!*]+)',
        ' ms là \.?([^()0-9-.,!*]+)',
        ' ms tên là \.?([^()0-9-.,!*]+)',
        ' ms : \.?([^()0-9-.,!*]+)',
        ' ms: \.?([^()0-9-.,!*]+)', 
        'ms \.?([^()0-9-.,!*]+)',
        'ms tên \.?([^()0-9-.,!*]+)',
        'ms là \.?([^()0-9-.,!*]+)',
        'ms tên là \.?([^()0-9-.,!*]+)',
        'ms : \.?([^()0-9-.,!*]+)',
        'ms: \.?([^()0-9-.,!*]+)', 
    ]

    format_pronoun20 = [
        ' ngài \.?([^()0-9-.,!*]+)',
        ' ngài tên \.?([^()0-9-.,!*]+)',
        ' ngài là \.?([^()0-9-.,!*]+)',
        ' ngài tên là \.?([^()0-9-.,!*]+)',
        ' ngài : \.?([^()0-9-.,!*]+)',
        ' ngài: \.?([^()0-9-.,!*]+)', 
        'ngài \.?([^()0-9-.,!*]+)',
        'ngài tên \.?([^()0-9-.,!*]+)',
        'ngài là \.?([^()0-9-.,!*]+)',
        'ngài tên là \.?([^()0-9-.,!*]+)',
        'ngài : \.?([^()0-9-.,!*]+)',
        'ngài: \.?([^()0-9-.,!*]+)', 
    ]

    # (tên/tên là/tên :) la [Name]
    format_semi_pronoun = [
        ' tên là \.?([^()0-9-.,!*]+)',
        ' là \.?([^()0-9-.,!*]+)',
        ' tên \.?([^()0-9-.,!*]+)',
        ' tên : \.?([^()0-9-.,!*]+)',
        'tên là \.?([^()0-9-.,!*]+)',
        'là \.?([^()0-9-.,!*]+)',
        'tên \.?([^()0-9-.,!*]+)',
        'tên : \.?([^()0-9-.,!*]+)',
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
        format_pronoun13,
        format_pronoun14,
        format_pronoun15,
        format_pronoun16,
        format_pronoun17,
        format_pronoun18,
        format_pronoun19,
        format_pronoun20,
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