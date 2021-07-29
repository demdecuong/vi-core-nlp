import datetime
import itertools
import pandas as pd

from termcolor import colored
from nltk import text
from tqdm import tqdm
from vi_nlp_core.ner.extractor import Extractor
from vi_nlp_core.testcase.tc_time import get_time_tc
from vi_nlp_core.testcase.tc_pername import get_person_name_tc
from vi_nlp_core.testcase.tc_date import get_date_test_case
from vi_nlp_core.utils.util import read
from vi_nlp_core.utils.preproces import Preprocess

VLSP_PATH = './vi_nlp_core/testcase/vlsp2016'
class Tester:
    def __init__(self):
        self.extractor = Extractor(load_dict=False)
        self.per_tc, self.per_expected_result = get_person_name_tc()
        self.time_tc, self.time_expected_result, self.time_spec_tc, self.time_spec_expected_result = get_time_tc()
        self.date_tc, self.date_expected_result = get_date_test_case()
        self.preprocessor = Preprocess()
        self.error_factor = 2

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

    def test_template(self,tem_dir = './vi_nlp_core/testcase/template'):
        # Set up data
        template = read(tem_dir+'/template.txt')
        data_template = pd.read_csv(tem_dir + '/data_template.csv')
        person_data = [self.preprocessor.preprocess((str(x).lower())) for x in data_template['person'].tolist() if str(x) != 'nan']
        date_time_data = [self.preprocessor.preprocess(str(x)) for x in data_template['date/time'].tolist() if str(x)!='nan']
        date_data = [self.preprocessor.preprocess(str(x)) for x in data_template['date'].tolist() if str(x)!='nan']
        time_data = [self.preprocessor.preprocess(str(x)) for x in data_template['time'].tolist() if str(x) != 'nan']
            
        date_time_data.extend(date_data)
        date_time_data.extend(time_data)

        # list of generated data
        data = self.generate_data_from_template(template,data_template)
        # Testing 
        time_res = []
        pername_res = []
        date_res = []

        per_cnt = 0
        date_cnt = 0
        time_cnt = 0
        for i in tqdm(range(len(data))):
            pername = self.extractor.extract_person_name(data[i], mode='pattern', rt='relative')['entities'][0]['value']
            pername = self.preprocessor.preprocess(pername.lower())
            if pername in person_data:
                per_cnt += 1
            time = self.extractor.extract_time(data[i])['entities']
            if time != []:
                time = data[i][max(time[0]['start'] - self.error_factor,0):min(time[0]['end'] + self.error_factor,len(data[i]))]
                time = self.preprocessor.preprocess(str(time))
                for label in date_time_data:
                    if label in time or time in label:
                        time_cnt += 1
                        break
            try:
                date = self.extractor.extract_date(data[i])['entities']
                if date != []:
                    date = data[i][max(date[0]['start'] - self.error_factor,0):min(date[0]['end'] + self.error_factor,len(data[i]))]
                    date = self.preprocessor.preprocess(str(date))
                    for label in date_time_data:
                        if label in date or date in label:
                            date_cnt += 1
                            break
            except:
                date = []
                print(data[i])
            time_res.append(time)
            pername_res.append(pername)
            date_res.append(date)

        self.write_result('Person name Accuracy',per_cnt,len(data))
        self.write_result('Date Accuracy',date_cnt,len(data))
        self.write_result('Time Accuracy',time_cnt,len(data))
        df = pd.DataFrame({
            'utterance' : data,
            'pername' : pername_res,
            'time' : time_res,
            'date' : date_res,
        })
        df.to_csv('template_result.csv',index=False)
        
    def generate_data_from_template(self,template,data_template):

        data_pattern = {
            '[want]' : ['tôi muốn','muốn','tôi','cho tôi'],
            '[want_cancel]' : ['giúp','cho tôi','giúp cho tôi','giúp tôi'],
            '[pronoun]' : ['bs','bác sĩ','dr','bacsi'],
            '[date/time]' : [str(x) for x in data_template['date/time'].tolist() if str(x)!='nan'],
            '[date]' : [str(x) for x in data_template['date'].tolist() if str(x)!='nan'],
            '[time]' : [str(x) for x in data_template['time'].tolist() if str(x) != 'nan'],
            '[person]' :[str(x) for x in data_template['person'].tolist() if str(x) != 'nan'],
            '[khoa]' :  [str(x) for x in data_template['khoa'].tolist() if str(x) != 'nan']
        }

        global_verification = ['[want]','[pronoun]','[person]','[date/time]', '[khoa]', '[want_cancel]', '[time]','[date]']
        final_data = []
        final_intent = []

        final_pername = []
        final_date = []
        final_time = []
        for sentence in template:
            pattern = []
            generated_data = []
            expected_intent = []

            pername_label = []
            date_label = []
            time_label = []
            
            for token in sentence.split(' '):
                if token in global_verification:
                    pattern.append(data_pattern[token])
                else:
                    pattern.append([token])

            for r in itertools.product(*pattern):
                text = ' '.join(list(r))
                generated_data.append(text)
                if sentence.find('hủy') != -1:
                    expected_intent.append('cancel')
                else:
                    expected_intent.append('book')
            final_data.extend(generated_data)
            final_intent.extend(expected_intent)

        df = pd.DataFrame({
            'utterance' : final_data,
            'intent' : ['default'] * len(final_data),
            'expected_intent' : final_intent
        })
        df.to_csv('template_data.csv', index=False)

        return final_data

    def read_test_cases(self, path):
        pass

    def write_result(self, tc, correct, total):
        print(f"------------Test case {tc}------------")
        print(f"{colored('Pass','green')} {correct}")
        print(f"{colored('Fail','red')} {total-correct}")
        print(f"{colored('Total','green')} {correct}/{total}")
