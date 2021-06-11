import pandas as pd

# Case 1 : tên đứng 1 mình
#   - viết Hoa
#   - viết hoa hết
#   - viết thường
#   - viết hoa ngẫu nhiên
#   - viết sai chính tả
#   - viết thiếu dấu
# Case 2 : tên đứng 1 mình thiếu họ
#   - viết Hoa
#   - viết hoa hết
#   - viết thường
#   - viết hoa ngẫu nhiên
#   - viết sai chính tả
#   - viết thiếu dấu
# Case 3 : tên đứng 1 mình thiếu tên
#   - viết Hoa
#   - viết hoa hết
#   - viết thường
#   - viết hoa ngẫu nhiên
#   - viết sai chính tả
#   - viết thiếu dấu
# Case 4 : có tân ngữ (tôi/tui/chú/bác/cô/dì/ông/bà/em/bác sĩ)
#   - 
# Case 5 : có nhiều tên trong 1 câu/ phức tạp/ tự nhiên
#   - 
# Case 6 : Không có tên trong câu

# testcase 1
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
        'Nguyễn Thị khánh Vân',
        'Ngyễn Mậu Sn',
        'Lê Văn Ponn',
        'Nguyen Thi Ta',
        'Quach Ngoc Hoanh'
    ]
    final_testcase.append(testcase1)
    final_expected_result.append(expected_result1)

    testcase2 = [
        'Văn Trần Chuyên',
        'Ngọc Đại Nghĩa'
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
        'Ngọc Đại Nghĩa'
        'Đình Chung',
        'Yến Trang',
        'Nguyễn',
        'Dương Phước Phúc',
        'Thị Khánh Vy',
        'Thị khánh Vân',
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