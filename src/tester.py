
from src.extractor import Extractor
from src.test_case_date import get_date_test_case

class Tester(object):
    def __init__(self) -> None:
        super().__init__()

        self.extractor = Extractor()
        self.input, self.target = get_date_test_case()

    def test_date(self):

        not_exact = 0
        len_test = 0

        for inputs, targets in zip(self.input, self.target):
            # print(len(inputs))
            for input, target in zip(inputs, targets):
                # print(input)
                # print(target)
                pred = self.extractor.extract_date(input)['entities']
                print(pred)
                # print(pred)
                for i in pred:
                    value = i['value']
                    for j in value:
                        if j not in target:
                            not_exact += 1
                            break
                        break
                    break
                break
        print(not_exact)
        print(len_test)
                
        # acc = 1 - float(not_exact)/len_test
        return 1
                

