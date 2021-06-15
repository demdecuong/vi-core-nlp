# Case 1: - Absolute
# Case 1.1: Number
# Case 1.2: Number and string
# Case 2: - Relative
# Case 2.1: Not clearly
# Case 2.2: Clearly

# Case 3: - hybrid 

# Current date - thứ 2 - ngày 14 tháng 6 năm 2021.  

def get_date_test_case():

    final_test = []
    expected_result = []

    # TEST CASE 
    test_case_1_1 = [
        '21/03/1997',
        '21/3/1997',
        '21/3/97',
        '21-3-1997',
        '21 3 1997',
        '22/3/1997 và 24/3/1997',
        '21-3'
    ]
    
    expected_result_test_case_1_1 = [
        [('Thứ 6', 21, 3, 1997)],
        [('Thứ 6', 21, 3, 1997)],
        [('Thứ 6', 21, 3, 1997)],
        [('Thứ 6', 21, 3, 1997)],
        [('Thứ 6', 21, 3, 1997)],
        [('Thứ 7', 22, 3, 1997), ('Thứ 2', 24, 3, 1997)],
        [('None', 21, 3, 'None')]
    ]

    final_test.append(test_case_1_1)
    expected_result.append(expected_result_test_case_1_1)

    test_case_1_2 = [
        'thứ 6',
        'ngày 22 tháng 5',
        'thứ 6 ngày 21 tháng 3 năm 1997',
        'năm 2021'
    ]


    expected_result_test_case_1_2 = [
        [('thứ 6', 'None', 'None', 'None')],
        [('None', 22, 5, 'None')],
        [('thứ 6', 21, 3, 1997)],
        [('None', 'None', 'None', 2021)]
    ]

    final_test.append(test_case_1_2)
    expected_result.append(expected_result_test_case_1_2)

    test_case_1_3 = [
        'ngày hai mot tháng ba',
        'ngày hai hai',
        'ngay hai muoi hai',
        'thứ sáu ngày hai mươi lăm',
        'tháng giêng'
    ]
    expected_result_test_case_1_3 = [
        [('None', 21, 3, 'None')],
        [('None', 22, 'None', 'None')],
        [('None', 22, 'None', 'None')],
        [('thứ 6', 25, 'None', 'None')],
        [('None', 'None', 1, 'None')]

    ]

    final_test.append(test_case_1_3)
    expected_result.append(expected_result_test_case_1_3)

    # TEST CASE 2
    test_case_2_1 = [
        'tuần sau',
        'tháng sau',
        'tuần vừa rồi',
        'tuần qua',
        'đầu tuần sau',
        'cuối tuần'
    ]

    expected_result_test_case_2_1 = [
        [('Thứ 2', 21, 6, 2021),
         ('Thứ 3', 22, 6, 2021),
         ('Thứ 4', 23, 6, 2021),
         ('Thứ 5', 24, 6, 2021),
         ('Thứ 6', 25, 6, 2021),
         ('Thứ 7', 26, 6, 2021),
         ('Chủ nhật', 27, 6, 2021)],
        
        [('Thứ 5', 1, 7, 2021),
         ('Thứ 6', 2, 7, 2021),
         ('Thứ 7', 3, 7, 2021),
         ('Chủ nhật', 4, 7, 2021),
         ('Thứ 2', 5, 7, 2021),
         ('Thứ 3', 6, 7, 2021),
         ('Thứ 4', 7, 7, 2021)],

        [('Thứ 2', 7, 6, 2021),
         ('Thứ 3', 8, 6, 2021),
         ('Thứ 4', 9, 6, 2021),
         ('Thứ 5', 10, 6, 2021),
         ('Thứ 6', 11, 6, 2021),
         ('Thứ 7', 12, 6, 2021),
         ('Chủ nhật', 13, 6, 2021)],

        [('Thứ 2', 7, 6, 2021),
         ('Thứ 3', 8, 6, 2021),
         ('Thứ 4', 9, 6, 2021),
         ('Thứ 5', 10, 6, 2021),
         ('Thứ 6', 11, 6, 2021),
         ('Thứ 7', 12, 6, 2021),
         ('Chủ nhật', 13, 6, 2021)],

        [('Thứ 2', 21, 6, 2021),
         ('Thứ 3', 22, 6, 2021),
         ('Thứ 4', 23, 6, 2021),
         ('Thứ 5', 24, 6, 2021),
         ('Thứ 6', 25, 6, 2021),
         ('Thứ 7', 26, 6, 2021),
         ('Chủ nhật', 27, 6, 2021)],

        [('Thứ 7', 26, 6, 2021),
         ('Chủ nhật', 27, 6, 2021)]     
    ]
    
    final_test.append(list(test_case_2_1))
    expected_result.append(expected_result_test_case_2_1)
    
    
    test_case_2_2 = [
        'hôm qua',
        'hôm nay',
        'ngày mai',
        'ngày kia',
        'thứ 2 tuần sau',
        'thứ 5 tuần vừa qua',
        'tuần đầu tiên tháng 6',
    ]

    expected_result_test_case_2_2 = [
        [('Thứ 2', 14, 6, 2021)],
        [('Thứ 3', 15, 6, 2021)],
        [('Thứ 4', 16, 6, 2021)],
        [('Thứ 6', 18, 6, 2021)],
        [('Thứ 2', 21, 6, 2021)],
        [('Thứ 5', 10, 6, 2021)],

        [('Thứ 3', 1, 6, 2021),
         ('Thứ 4', 2, 6, 2021),
         ('Thứ 5', 3, 6, 2021),
         ('Thứ 6', 4, 6, 2021),
         ('Thứ 7', 5, 6, 2021),
         ('Chủ nhật', 6, 6, 2021)]
    ]

    final_test.append(test_case_2_2)
    expected_result.append(expected_result_test_case_2_2)
    # print(final_test)
    # print(expected_result)

    return final_test, expected_result