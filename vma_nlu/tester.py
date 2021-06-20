import datetime
import pandas as pd

from nltk import text
from vma_nlu.ner.extractor import Extractor
from vma_nlu.testcase.tc_time import get_time_tc
from vma_nlu.testcase.tc_pername import get_person_name_tc
from termcolor import colored
from vma_nlu.testcase.tc_date import get_date_test_case

VLSP_PATH = './vma_nlu/testcase/vlsp2016'
class Tester:
    def __init__(self):
        self.extractor = Extractor(load_dict=False)
        self.per_tc, self.per_expected_result = get_person_name_tc()
        self.time_tc, self.time_expected_result, self.time_spec_tc, self.time_spec_expected_result = get_time_tc()
        self.date_tc, self.date_expected_result = get_date_test_case()

    def test_person_name(self):
        tc_num = 1
        total_acc = 0
        total_len = 0
        for tc, ex_result in zip(self.per_tc, self.per_expected_result):
            acc = 0
            for test, label in zip(tc, ex_result):
                pred = self.extractor.extract_person_name(
                    test, mode='pattern', rt='relative')['entities']
                if pred[0]['value'] in label:
                    acc += 1
                # print(pred[0]['value'], label , acc)
            self.write_result(tc_num, acc, len(tc))
            tc_num += 1
            total_len += len(tc)
            total_acc += (acc)
        self.write_result('Total', total_acc, total_len)

    def test_person_name_vlsp(self,mode='train'):
        vlsp = pd.read_csv(f"{VLSP_PATH}/{mode}_processed.csv")
        per_tc = vlsp['src']
        per_expected_result = vlsp['trg']

        correct = 0

        for test, label in zip(per_tc, per_expected_result):
            pred = self.extractor.extract_person_name(
                test, mode='pattern', rt='relative')['entities']
            if pred[0]['value'] in label:
                correct += 1
 
        self.write_result('Total', correct, len(vlsp))
 
    def test_time(self):
        tc_num = 1
        total_acc = 0
        total_len = 0
        for tc, ex_result in zip(self.time_tc, self.time_expected_result):
            acc = 0
            for test, label in zip(tc, ex_result):
                pred = self.extractor.extract_time(test)['entities']
                if pred[0]['value'] == label:
                    acc += 1
                # print(pred[0]['value'], label , acc,pred[0]['extractor'])
            self.write_result(tc_num, acc, len(tc))
            tc_num += 1
            total_len += len(tc)
            total_acc += (acc)
        for tc, ex_result in zip(self.time_spec_tc, self.time_spec_expected_result):
            acc = 0
            for test, label in zip(tc, ex_result):
                pred = self.extractor.extract_time(test)['entities']
                pred = pred[0]['value']
                now = datetime.datetime.now()
                hour = now.hour + int(label[0])
                minute = now.minute + int(label[1])
                if minute >= 60:
                    minute -= 60
                    hour += 1
                if hour - pred[0] == 0 and minute - pred[1] <= 1:
                    acc += 1
                print(pred, hour ,minute, acc)
            self.write_result(tc_num, acc, len(tc))
            tc_num += 1
            total_len += len(tc)
            total_acc += (acc)
        self.write_result('Total', total_acc, total_len)

    def test_date(self):
        correct = 0
        len_total_test = 0
        tc_num = 1
        for tc, ex_result in zip(self.date_tc, self.date_expected_result):
            len_total_test += len(tc)
            correct_tc = 0
            for test, target in zip(tc, ex_result):
                # print(test)
                pred = self.extractor.extract_date(test)
                # print(pred)
                entitites = pred['entities']
                result = []
                for i in entitites:
                    value = i['value']
                    result.extend(value)

                if result == target:
                    correct += 1
                    correct_tc += 1
            len_tc = len(tc)
            self.write_result(tc=tc_num, correct=correct_tc, total=len_tc)
            tc_num += 1

        acc = correct/len_total_test
        self.write_result(tc='Total', correct=correct, total=len_total_test)
        return acc

    def test_intent(self):
        pass

    def unit_test(self,features='pername'):
        assert features in ['pername','time','date']
        while True:
            utterance = str(input("Enter a sentence:"))
            if features == 'pername':
                result = self.extractor.extract_person_name(utterance)
            elif features == 'time':
                result = self.extractor.extract_time(utterance)
            elif features == 'date':
                result = self.extractor.extract_datetime(utterance)
            print(result)

    def read_test_cases(self, path):
        pass

    def write_result(self, tc, correct, total):
        print(f"------------Test case {tc}------------")
        print(f"{colored('Pass','green')} {correct}")
        print(f"{colored('Fail','red')} {total-correct}")
        print(f"{colored('Total','green')} {correct}/{total}")
