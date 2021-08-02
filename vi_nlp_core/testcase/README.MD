# Test Cases Document

### Usage
- Test template : 
```
from vi_nlp_core.tester import Tester

tester = Tester()
tester.test_template()

# Test NER
tester.test_person_name()
tester.test_time()
tester.test_date()

# Test VLSP2016
tester.test_person_name_vlsp('train')
tester.test_person_name_vlsp('dev')
tester.test_person_name_vlsp('test')
```
## Person Name
Mỗi testcase đảm bảo các data
- viết Hoa chữ cái đầu
- viết Hoa hết
- viết thường hết
- viết Hoa ngẫu nhiên
- viết sai chính tả
- viết thiếu dấu

### testcase 1 : Tên đứng 1 mình 
-   số lương : 12 
### testcase 2 : Tên đứng 1 mình thiếu họ
-   số lương : 12 
### testcase 3 : tên đứng 1 mình thiếu tên
-   số lương : 5 
### testcase 4 : có tân ngữ (tôi/tui/chú/bác/cô/dì/ông/bà/em/bác sĩ)
-   số lương : 10 
### testcase 5 : có nhiều tên trong 1 câu/ phức tạp/ tự nhiên
-   số lương : 10 

### Result
- Public Testset   

| Testcase | Accuracy |
| --- | --- |
| 1 | 12/12 |
| 2 | 12/12 |
| 3 | 5/5 |
| 4 | 10/10 |
| 5 | 3/10 |
| Total | 42/49 |

- Template Testset

Precision = 1742224/2206632 = 78.95 %

- VLSP 2016 (Data contains Person Name only)

| Data | Accuracy |
| --- | --- |
| train | 15/4924 |
| dev | 2/571 |
| test | 7/861 |

## Time
### testcase 1 : 7:30 (straight forward)  
-   số lương : 10
### testcase 2 : 7 giờ 20 phút  (giờ và phút ghi số)
-   số lương : 10 
### testcase 3 : bảy giờ hay mươi phút (giờ và phút ghi chữ)
-   số lương : 10
### testcase 4 :bảy giờ kém/hơn mươi phút (giờ và phút ghi chữ + hơn/kém)
-   số lương : 10 
### testcase 5 : 2 tiếng nữa tại vinmec (giờ phút hiện tại)
-   số lương : 8

### Result
- Public Testset 

| Testcase | Accuracy |
| --- | --- |
| 1 | 10/10 |
| 2 | 9/10 |
| 3 | 9/10 |
| 4 | 8/10 |
| 5 | 9/9 |
| Total | 46/49 |

- Template Testset

Precision =  662352/2206632 = 62.45 %

## Date
### testcase 1: Absolute - Number (21/3/1997, 21/3, 21-3, ... )
 - số lượng: 7

### testcase 2: Absolute - Number and String (vd: ngày 21 tháng 3 năm 1997, ngày 21, ngày 21 tháng 3, ... )

- số lượng: 4

### testcase 3: Absolute - String (vd: ngày hai mốt tháng ba, ... )

- số lượng: 5

### testcase 4: Relative - Unclear (vd: tuần sau, tuần qua, tháng tới, đầu tháng tới... )

- số lượng: 6

### testcase: Relative - Clear (vd: ngay mai, ngày kia, thứ 3 tuần sau, ngày đầu tiên tuần sau)

- số lượng: 7

### Result:

- Public Testset

| Testcase | Accuracy |
| --- | --- |
| 1 | 6/7 |
| 2 | 4/4 |
| 3 | 4/5 |
| 4 | 5/6 |
| 5 | 4/7 |
| Total | 23/29 |

- Template Testset

Precision = 1997632/2206632 = 90.53 %

## Intent
TBD

