from vma_nlu.tester import Tester

tester = Tester()

print('----------------- Test person name -----------------')
tester.test_person_name()

print('----------------- Test time -----------------')
tester.test_time()

print('----------------- Test date -----------------')
tester.test_date()

# tester.unit_test('time')


# VLSP-2016 TESTSET
# tester.test_person_name_vlsp('train')
# tester.test_person_name_vlsp('dev')
# tester.test_person_name_vlsp('test')
