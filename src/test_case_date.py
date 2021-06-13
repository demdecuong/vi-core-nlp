

# Case 1: - Absolute
# Case 1.1: Number
# Case 1.2: Number and string
# Case 2: - Relative
# Case 2.1: Not clearly
# Case 2.2: Clearly

# Case 3: - hybrid 

# Current date - chủ nhật - ngày 13 tháng 6 năm 2021.  

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
        '22/3/1997 và 24/3/1997'
    ]
    
    expected_result_test_case_1_1 = [
        [('thứ 6', 21, 3, 1997)],
        [('thứ 6', 21, 3, 1997)],
        [('thứ 6', 21, 3, 1997)],
        [('thứ 6', 21, 3, 1997)],
        [('thứ 6', 21, 3, 1997)],
        [('thứ 7', 22, 3, 1997), ('thứ 2', 24, 3, 1997)]
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
        [('thứ 6', None, None, None)],
        [(None, 22, 5, None)],
        [('thứ 6', 21, 3, 1997)],
        [(None, None, None, 2021)]
    ]

    final_test.append(test_case_1_2)
    expected_result.append(expected_result_test_case_1_2)
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
        [('thứ 2', 14, 6, 2021),
         ('thứ 3', 15, 6, 2021),
         ('thứ 4', 16, 6, 2021),
         ('thứ 5', 17, 6, 2021),
         ('thứ 6', 18, 6, 2021),
         ('thứ 7', 19, 6, 2021),
         ('chủ nhật', 20, 6, 2021)],
        
        [('thứ 5', 1, 7, 2021),
         ('thứ 6', 2, 7, 2021),
         ('thứ 7', 3, 7, 2021),
         ('chủ nhật', 4, 7, 2021),
         ('thứ 2', 5, 7, 2021),
         ('thứ 3', 6, 7, 2021),
         ('thứ 4', 7, 7, 2021),
         ('thứ 5', 8, 7, 2021),
         ('thứ 6', 9, 7, 2021),
         ('thứ 7', 10, 7, 2021),
         ('chủ nhật', 11, 7, 2021),
         ('thứ 2', 12, 7, 2021),
         ('thứ 3', 13, 7, 2021),
         ('thứ 4', 14, 7, 2021),
         ('thứ 5', 15, 7, 2021),
         ('thứ 6', 16, 7, 2021),
         ('thứ 7', 17, 7, 2021),
         ('chủ nhật', 18, 7, 2021),
         ('thứ 2', 19, 7, 2021),
         ('thứ 3', 20, 7, 2021),
         ('thứ 4', 21, 7, 2021),
         ('thứ 5', 22, 7, 2021),
         ('thứ 6', 23, 7, 2021),
         ('thứ 7', 24, 7, 2021),
         ('chủ nhật', 25, 7, 2021),
         ('thứ 2', 26, 7, 2021),
         ('thứ 3', 27, 7, 2021),
         ('thứ 4', 28, 7, 2021),
         ('thứ 5', 29, 7, 2021),
         ('thứ 6', 30, 7, 2021),
         ('thứ 7', 31, 7, 2021)],

        [('thứ 2', 31, 5, 2021),
         ('thứ 3', 1, 6, 2021),
         ('thứ 4', 2, 6, 2021),
         ('thứ 5', 3, 6, 2021),
         ('thứ 6', 4, 6, 2021),
         ('thứ 7', 5, 6, 2021),
         ('chủ nhật', 6, 6, 2021)],

        [('thứ 2', 31, 5, 2021),
         ('thứ 3', 1, 6, 2021),
         ('thứ 4', 2, 6, 2021),
         ('thứ 5', 3, 6, 2021),
         ('thứ 6', 4, 6, 2021),
         ('thứ 7', 5, 6, 2021),
         ('chủ nhật', 6, 6, 2021)],

        [('thứ 2', 14, 6, 2021),
         ('thứ 3', 15, 6, 2021),
         ('thứ 4', 16, 6, 2021),
         ('thứ 5', 17, 6, 2021),
         ('thứ 6', 18, 6, 2021),
         ('thứ 7', 19, 6, 2021),
         ('chủ nhật', 20, 6, 2021)],

         [('thứ 2', 14, 6, 2021),
         ('thứ 3', 15, 6, 2021),
         ('thứ 4', 16, 6, 2021),
         ('thứ 5', 17, 6, 2021),
         ('thứ 6', 18, 6, 2021),
         ('thứ 7', 19, 6, 2021),
         ('chủ nhật', 20, 6, 2021)]     
    ]
    
    final_test.append(list(test_case_2_1))
    expected_result.append(expected_result_test_case_2_1)


    test_case_2_2 = [
        'hôm qua',
        'hôm nay',
        'ngày mai',
        'ngày kia',
        'thứ 2 tuần sau',
        'thứ 5 tuần vừa rồi',
        'tuần đầu tiên tháng 6',
    ]

    expected_result_test_case_2_2 = [
        [('thứ 7', 12, 6, 2021)],
        [('chủ nhật', 13, 6, 2021)],
        [('thứ 2', 14, 6, 2021)],
        [('thứ 4', 16, 6, 2021)],
        [('thứ 2', 14, 6, 2021)],
        [('thứ 5', 10, 6, 2021)],

        [('thứ 3', 1, 6, 2021),
         ('thứ 4', 2, 6, 2021),
         ('thứ 5', 3, 6, 2021),
         ('thứ 6', 4, 6, 2021),
         ('thứ 7', 5, 6, 2021),
         ('chủ nhật', 6, 6, 2021)]
    ]

    final_test.append(test_case_2_2)
    expected_result.append(expected_result_test_case_2_2)
    print(final_test)
    # print(expected_result)

    return final_test, expected_result

