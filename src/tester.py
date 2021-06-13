
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
            # len_test += len(inputs)
            for input, target in zip(inputs, targets):
                # print(input)
                # print(target)
                pred = self.extractor.extract_date(input)['entities']
                # print(pred)
                len_test += len(pred)
                for i in pred:
                    value = i['value']
                    for j in value:
                        if j not in target:
                            not_exact += 1
                            break
                
        acc = 1 - float(not_exact)/len_test
        return acc
                

