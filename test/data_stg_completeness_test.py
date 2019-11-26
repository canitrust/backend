import unittest
import os
import json
import sys
import pymongo

class Mongo:
  def __init__(self, credential):
    self.client = pymongo.MongoClient(credential['DB_URL'])
    self.db = self.client[credential['DB_DATABASE']]
    self.testresults = self.db['testresults']
    self.testcases = self.db['testcases']

  def close(self):
    self.client.close()


class DriverTest(unittest.TestCase):
  def test_testresult_possible_answer(self):
    DB = Mongo(credential)
    testresults = DB.testresults.find()
    testcases = DB.testcases.find()
    # Extract a dict of possible answer ids per testcase for easier comparison
    possible_answers = {testcase['testNumber']: [answer['ans_id'] for answer in testcase['possibleAnswers']] for testcase in testcases}

    for result in testresults:
      with self.subTest(case=result):
        curr_test_num = result['testNumber']
        curr_result_num = result['result']
        # test whether each answer id in the new test results exists in the test case descriptions
        self.assertIn(curr_result_num, possible_answers[curr_test_num], 'Error in test result number: ' + str(curr_test_num))

if __name__ == '__main__':
  credential = {}
  credential['DB_DATABASE'] = sys.argv.pop()
  credential['DB_URL'] = sys.argv.pop()
  unittest.main()
