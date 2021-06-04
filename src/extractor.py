import re

class Extractor:
    def __init__(self):

        self.phone_regex = r"(84|0[3|5|7|8|9])+([0-9]{8})\b"


    def extract_time(self,input):
        '''
        Input:
            given string
        '''

    def extract_date(self,input):
        '''
        Input:
            input string
        Output:
            return tuple of (dd,mm,yyyy)
        '''

    def extract_date_time(self,input):
        pass
    
    def extract_person_name(self,input):
        pass

    def extract_phone_num(self,text):
        result = re.findall(self.phone_regex, text)
        if result == []:
            return 'Invalid'
        else:
            nha_mang = result[0][0]
            remain = result[0][1]
            return nha_mang + remain

    # số thứ tự, có thể dùng trong trường hợp user thay đổi/hủy lịch trong danh sách lịch hẹn)
    def extract_ordinal_number(self,input):
        pass

    # chuyên khoa của bác sỹ
    def extract_specialization(self,input):
        pass