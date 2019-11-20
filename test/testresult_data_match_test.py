import unittest
import os
import json


class DriverTest(unittest.TestCase):

    def test_testresult_possible_answer(self):
        sync_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../sync')
        with open(sync_path + '/translated.json', "r") as read_it:
            testresults = json.load(read_it)

        with open(sync_path + '/testcases.db.json', "r") as read_it:
            testcases = json.load(read_it)
            # Extract a dict of possible answer ids per testcase for easier comparison
            possible_answers = {testcase['testNumber']: [answer['ans_id'] for answer in testcase['possibleAnswers']] for testcase in testcases}

        with open(sync_path + '/tags.db.json', "r") as read_it:
            tags = json.load(read_it)

        for result in testresults:
            curr_test_num = result['testNumber']
            curr_result_num = result['result']
            # test whether each answer id in the new test results exists in the test case descriptions
            self.assertIn(curr_result_num, possible_answers[curr_test_num], 'Error in test result: ' + str(result))


if __name__ == '__main__':
    unittest.main()
