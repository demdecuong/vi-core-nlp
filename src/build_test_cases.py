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
# Case 4 : có tân ngữ (tôi/tui/chú/bác/cô/dì/ông/bà/em/)
#   - 
# Case 5 : có nhiều tên trong 1 câu
#   - 


# testcase 1
testcase1 = [
    'Nguyễn Văn Bưởi',
    'Trần Ngọc Văn Sáng'
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

# testcase 2
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

#testcase 3
