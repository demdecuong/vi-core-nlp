import pandas as pd

# Case 1 : tên đứng 1 mình
#   - viết Hoa
#   - viết hoa hết
#   - viết thường
#   - viết hoa ngẫu nhiên
#   - viết sai chính tả
#   - viết thiếu dấu
# Case 2 : tên đứng 1 mình thiếu họ
# Case 3 : tên đứng 1 mình thiếu tên
# Case 4 : có tân ngữ (tôi/tui/chú/bác/cô/dì/ông/bà/em/bác sĩ)
# Case 5 : có nhiều tên trong 1 câu/ phức tạp/ tự nhiên
# Case 6 : Không có tên trong câu

def get_person_name_tc():
    final_testcase = []
    final_expected_result = [] 

    testcase1 = [
        'Nguyễn Văn Bưởi',
        'Trần Ngọc Văn Sáng',
        'TẠ ĐÌNH TRUNG',
        'LÊ YÊN THANH',
        'hoàng nguyễn',
        'nguyễn dương phước phúc',
        'nGuyễn tHị khÁnh Vy',
        'nGuyễn tHị khÁnh VÂN',
        'Ngyễn Mậu Sn',
        'Lê Văn Ponn',
        'Nguyen Thi Ta',
        'Quach Ngoc Hoanh'
    ]
    expected_result1 = [
        'Nguyễn Văn Bưởi',
        'Trần Ngọc Văn Sáng',
        'Tạ Đình Trung',
        'Lê Yên Thanh',
        'Hoàng Nguyễn',
        'Nguyễn Dương Phước Phúc',
        'Nguyễn Thị Khánh Vy',
        'Nguyễn Thị Khánh Vân',
        'Ngyễn Mậu Sn',
        'Lê Văn Ponn',
        'Nguyen Thi Ta',
        'Quach Ngoc Hoanh'
    ]
    final_testcase.append(testcase1)
    final_expected_result.append(expected_result1)

    testcase2 = [
        'Văn Trần Chuyên',
        'Ngọc Đại Nghĩa',
        'ĐÌNH CHUNG',
        'YẾN TRANG',
        'nguyễn',
        'dương phước phúc',
        'tHị khÁnh Vy',
        'tHị khÁnh VÂN',
        'Mậu Sn',
        'Văn Ponn',
        'Thi Ta',
        'Ngoc Hoanh'
    ]
    expected_result2 = [
        'Văn Trần Chuyên',
        'Ngọc Đại Nghĩa',
        'Đình Chung',
        'Yến Trang',
        'Nguyễn',
        'Dương Phước Phúc',
        'Thị Khánh Vy',
        'Thị Khánh Vân',
        'Mậu Sn',
        'Văn Ponn',
        'Thi Ta',
        'Ngoc Hoanh'
    ]
    final_testcase.append(testcase2)
    final_expected_result.append(expected_result2)

    testcase3 = [
        'Võ Hoàng',
        'tran minh',
        'nguyễn công',
        'Alexander Alnord',
        'Mohammet Sala'
    ]

    expected_result3 = [
        'Võ Hoàng',
        'Tran Minh',
        'Nguyễn Công',
        'Alexander Alnord',
        'Mohammet Sala'
    ]

    final_testcase.append(testcase3)
    final_expected_result.append(expected_result3)

    testcase4 = [
        'tôi là Nguyễn Văn Đậu',
        'ông trần văn cường',
        'tôi muốn đặt bác sĩ Phạm Văn Hải',
        'tôi tên Tạ Deep Huy',
        'em là Nguyễn Dương Phúc Tài',
        'bác là Trần Hoàng Phúc',
        'dì tên là Thích Ăn Gà',
        'cậu là Trần Khắc Việt',
        'tôi ký ngực fan 2k3',
        'trong giấy khai sinh tên tôi là ông Nam Hên'
    ]
    expected_result4 = [
        'Nguyễn Văn Đậu',
        'Trần Văn Cường',
        'Phạm Văn Hải',
        'Tạ Deep Huy',
        'Nguyễn Dương Phúc Tài',
        'Trần Hoàng Phúc',
        'Thích Ăn Gà',
        'Trần Khắc Việt',
        'Ký Ngực Fan 2k3',
        'Ông Nam Hên'
    ]
    final_testcase.append(testcase4)
    final_expected_result.append(expected_result4)
    
    testcase5 = [
        'tôi là Nguyễn Phúc Minh, học trò của Trần Nam Dũng',
        'tôi tên Trần Hoàng Vũ, tôi hẹn bác sĩ Nguyễn Anh Tú',
        'tôi tên là Microsoft, tôi nghe nói bác sĩ Phạm Hải Nam chuyên khoa chấn thương chỉnh hình. Nên tôi muốn đặt bác sĩ.',
        'tôi trần nam dũng, em của trần đại quang, cháu của nguyễn tấn dũng',
        'bác sĩ Khắc Việt ngày 20/03 có rãnh không ạ ? Tôi muốn đặt lịch hẹn ạ. Tôi tên Nguyễn Sang Em',
        'tôi muốn đặt lịch hẹn bác Hoan là bác sĩ chuyên khoa 2',
        'bác sĩ Cường tên thật là Trần Cường Cương',
        'ở xóm mọi người gọi tôi là Tèo nhưng tên cúng cơm là Trần Nguyễn Hoàng Trương',
        'Đồng nghiệp cũ tôi là Lê Văn Pon, anh đã giúp đỡ tôi rất nhiều. Cảm ơn anh',
        'Sếp Cũ tôi tên là Phạm Văn Hùng, chúc anh thật nhiều sức khỏe',
    ]
    expected_result5 = [
        'Nguyễn Phúc Minh,Trần Nam Dũng',
        'Trần Hoàng Vũ,Nguyễn Anh Tú',
        'Microsoft, Phạm Hải Nam',
        'Trần Nam Dũng, Trần đại quang, Nguyễn tấn dũng',
        'Khắc Việt, Nguyễn Sang Em',
        'Hoan',
        'Cường,Trần Cường Cương',
        'Tèo,Trần Nguyễn Hoàng Trương',
        'Lê Văn Pon',
        'Phạm Văn Hùng',
    ]
    final_testcase.append(testcase5)
    final_expected_result.append(expected_result5)
    
    return final_testcase, final_expected_result

def get_time_tc():
    final_tc = []
    final_expected_result = []

    # 7:30  [VALUE] tiếng [VALUE]    
    tc1 = [
        'tôi đặt bác sĩ Hoàn vào lúc 8:30 phút ngày 1/2/2021',
        '7:15 sáng thứ hai tuần sau',
        '5.45 chiều ngày 1/6 tuần này',
        'trưa 1.30.00 thứ ba hàng tuần',
        '9h sáng hôm sau',
        '15h30 ngày 2/4/2021',
        'tôi hẹn bác sĩ Toàn lúc 17h05 được không ạ',
        'tôi muốn đặt lịch lúc 7:00 với bác sĩ Minh',
        'tôi muốn đặt lịch lúc 7h00 với bác sĩ Minh',
        'đồng hồ chỉ 10:30:30 là tôi đến',
    ]
    exp_res1 = [
        (8,30),
        (7,15),
        (17,45),
        (13,30),
        (9,0),
        (15,30),
        (17,5),
        (7,0),
        (7,0),
        (10,30),
    ]

    final_tc.append(tc1)
    final_expected_result.append(exp_res1)

    # 7 giờ 20 phút    
    tc2 = [
        'tôi đặt bác sĩ Hoàn vào lúc 8 giờ 30 phút ngày 1/2/2021',
        'tuần sau lúc 7 giờ 15',
        'sáng ngày 3/7 lúc 15 giờ',
        '7 giờ 00 sáng thứ ba đầu tiên của tháng sau',
        'ngày 10/3, 9h giờ rưỡi',
        'thứ 2 ngày 15/06, 9 giờ 45',
        'tuần tới tôi mới rãnh, nhưng khoảng 4 giờ rưỡi tôi rãnh',
        '4 giờ rưỡi chiều mai tại vinmec',
        '4 giờ sáng thứ sáu ngày mai nhé',
        'hẹn bác sĩ lúc 5 rưỡi chiều thứ 2 ngày 15/06',
    ]

    exp_res2 = [
        (8,30),
        (7,15),
        (15,0),
        (7,0),
        (9,30),
        (9,45),
        (4,30),
        (16,30),
        (4,0),
        (17,30),
    ]

    final_tc.append(tc2)
    final_expected_result.append(exp_res2)

    # bảy giờ hay mươi phút 
    tc3 = [
        'tôi đặt bác sĩ Hoàn vào lúc tám giờ ba mươi phút ngày 1/2/2021',
        'tuần sau lúc bảy giờ mười lăm',
        'sáng ngày 3/7 lúc mười năm giờ',
        'bảy giờ sáng thứ ba đầu tiên của tháng sau',
        'ngày 10/3, chín giờ rưỡi',
        'thứ 2 ngày 15/06, chín giờ bốn mươi lăm',
        'tuần tới tôi mới rãnh, nhưng khoảng bốn giờ rưỡi tôi rãnh',
        'bốn giờ ba mươi phút chiều mai tại vinmec',
        'bốn giờ sáng thứ sáu ngày mai nhé',
        'hẹn bác sĩ lúc năm rưỡi chiều thứ 2 ngày 15/06',
    ]

    exp_res3 = [
        (8,30),
        (7,15),
        (15,0),
        (7,0),
        (9,30),
        (9,45),
        (4,30),
        (16,30),
        (4,0),
        (17,30),
    ]

    final_tc.append(tc3)
    final_expected_result.append(exp_res3)

    # bảy giờ kém/hơn mươi phút    
    tc4 = [
        'tôi đặt bác sĩ Hoàn vào lúc 8 giờ kém 20 phút ngày 1/2/2021',
        'tuần sau lúc 7 giờ hơn 15',
        'sáng ngày 3/7 lúc 15 giờ kém 5 phút',
        '7 giờ 20 kém 5 phút sáng thứ ba đầu tiên của tháng sau',
        'ngày 10/3, chín giờ kém 15 phút',
        'thứ 2 ngày 15/06, 10 giờ kém mười lăm',
        'tuần tới tôi mới rãnh, nhưng khoảng bốn giờ rưỡi hơn tôi rãnh',
        '4 giờ thiếu 5 chiều mai tại vinmec',
        '9 giờ kém 10 sáng thứ sáu ngày mai nhé',
        'hẹn bác sĩ lúc 5 rưỡi hơn chiều thứ 2 ngày 15/06',
    ]

    exp_res4 = [
        (7,40),
        (7,15),
        (14,55),
        (7,15),
        (8,45),
        (9,45),
        (4,30),
        (15,55),
        (8,50),
        (17,30),
    ]
    final_tc.append(tc4)
    final_expected_result.append(exp_res4)

    # 7 tieng nua    
    special_tc = []
    final_spec_expected_result = []
    tc5 = [
        '2 tiếng nữa tại vinmec',
        '3 giờ tiếp theo nhưng vào ngày mai',
        'tôi có hẹn với bác sĩ Toàn vào 2 tiếng tiếp theo',
        '4 tiếng sau họp tại trụ sở CA',
        'tôi cần book lịch gấp vào 30 phút sau',
        'tôi cần book lịch gấp vào 1 tiếng rưỡi sau',
        'lát nữa sau 1 tiếng , tôi cần gặp bác sĩ gấp',
        'lát nữa sau 1 tiếng 20 phút, tôi cần gặp bác sĩ gấp',
    ]
    exp_res5 = [
        (2,0),
        (3,0),
        (2,0),
        (4,0),
        (0,30),
        (1,30),
        (1,0),
        (1,20),
    ]
    special_tc.append(tc5)
    final_spec_expected_result.append(exp_res5)

    return final_tc, final_expected_result, special_tc, final_spec_expected_result