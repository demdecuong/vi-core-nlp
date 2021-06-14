import datetime
from vma_nlu.ner.extractor import Extractor
from vma_nlu.testcase.test_cases import get_person_name_tc, get_time_tc
from termcolor import colored

class Tester:
    def __init__(self):
        self.extractor = Extractor(load_dict=False)    
        self.per_tc, self.per_expected_result = get_person_name_tc()
        self.time_tc, self.time_expected_result, self.time_spec_tc, self.time_spec_expected_result = get_time_tc()
    def test_person_name(self):
        tc_num = 1
        total_acc = 0 
        total_len = 0
        for tc, ex_result in zip(self.per_tc,self.per_expected_result):
            acc = 0
            for test, label in zip(tc,ex_result):
                pred = self.extractor.extract_person_name(test,mode='pattern', rt='relative')['entities']
                if pred[0]['value'] in label:
                    acc += 1
                # print(pred[0]['value'], label , acc)
            self.write_result(tc_num,acc,len(tc))
            tc_num += 1
            total_len += len(tc)
            total_acc += (acc)
        self.write_result('Total',total_acc,total_len)

    def test_time(self):
        tc_num = 1
        total_acc = 0 
        total_len = 0
        for tc, ex_result in zip(self.time_tc,self.time_expected_result):
            acc = 0
            for test, label in zip(tc,ex_result):
                pred = self.extractor.extract_time(test)['entities']    
                if pred[0]['value'] == label:
                    acc += 1
                # print(pred[0]['value'], label , acc,pred[0]['extractor'])
            self.write_result(tc_num,acc,len(tc))
            tc_num += 1
            total_len += len(tc)
            total_acc += (acc)
        for tc, ex_result in zip(self.time_spec_tc,self.time_spec_expected_result):
            acc = 0
            for test, label in zip(tc,ex_result):
                pred = self.extractor.extract_time(test)['entities']
                pred = pred[0]['value']
                now = datetime.datetime.now()
                hour = now.hour + int(label[0])
                minute = now.minute + int(label[1])
                if hour - pred[0] == 0 and minute - pred[1] <= 1:
                    acc += 1
                # print(pred, hour ,minute, acc)
            self.write_result(tc_num,acc,len(tc))
            tc_num += 1
            total_len += len(tc)
            total_acc += (acc)
        self.write_result('Total',total_acc,total_len)

    def test_date(self):
        pass

    def test_intent(self):
        pass
    
    def read_test_cases(self,path): 
        pass

    def write_result(self,tc,correct,total):
        print(f"------------Test case {tc}------------")
        print(f"{colored('Pass','green')} {correct}")
        print(f"{colored('Fail','red')} {total-correct}")
        print(f"{colored('Total','green')} {correct}/{total}")