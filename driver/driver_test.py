import unittest
import os
import json
import importlib

class DriverTest(unittest.TestCase):
 
    def test_completeness_testcases(self):
        keys = []

        with open(os.path.abspath(os.path.dirname(__file__)) + '/config/map.json', "r") as read_it:
            dataJson = json.load(read_it)
        for key, value in dataJson.items():
            if dataJson[key]['isLive']: keys.append(key)

        with open(os.path.abspath(os.path.dirname(__file__)) + '/config/testcases.json', "r") as read_it:
            testcases = json.load(read_it)
            
        with open(os.path.abspath(os.path.dirname(__file__)) + '/config/tags.json', "r") as read_it:
            tags = json.load(read_it)
        
        for key in keys:
            with self.subTest(key=key):
                self.assertEqual(testcases[key]["testNumber"], int(key))
                self.assertIsInstance(testcases[key]["title"], str)
                self.assertIsInstance(testcases[key]["description"], str)
                self.assertIsInstance(testcases[key]["date_created"], str)
                self.assertIsInstance(testcases[key]["path"], str)
                self.assertIsInstance(testcases[key]["question"], str)
                self.assertIsInstance(testcases[key]["tagNums"], list)
                for tag_num in testcases[key]["tagNums"]:
                    self.assertEqual(tags[str(tag_num)]["tagNumber"], tag_num)
                    self.assertIsInstance(tags[str(tag_num)]["tagText"], str)
                self.assertIsInstance(testcases[key]["possibleAnswers"], list)
                for ans in testcases[key]["possibleAnswers"]:
                    self.assertIsInstance(ans["ans_id"], int)
                    self.assertIsInstance(ans["ans_desc"], str)
    
if __name__ == '__main__':
    unittest.main()