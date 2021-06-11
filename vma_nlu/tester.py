from vma_nlu.ner.extractor import Extractor
from vma_nlu.testcase.test_cases import get_person_name_tc
from termcolor import colored

class Tester:
    def __init__(self):
        self.extractor = Extractor(load_dict=False)    
        self.per_tc, self.per_expected_result = get_person_name_tc()

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
        pass

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