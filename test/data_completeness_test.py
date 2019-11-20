import unittest
import os
import json

class DriverTest(unittest.TestCase):
 
    def test_completeness_testcases(self):
        cases = []
        config_path = os.path.abspath(os.path.dirname(__file__)) + '/../driver/config/'
        with open(config_path + 'map.json', "r") as read_it:
            dataJson = json.load(read_it)
        for key, value in dataJson.items():
            if dataJson[key]['isLive']: cases.append(key)

        with open(config_path + 'testcases.json', "r") as read_it:
            testcases = json.load(read_it)

        with open(config_path + 'tags.json', "r") as read_it:
            tags = json.load(read_it)
        required_keys = ["testNumber", "title", "description", "detailedDescription", "date_created", "path", "question", "tagNums", "possibleAnswers"]
        for case in cases:
            with self.subTest(case=case):
                for key in required_keys:
                    # all required keys have to exist
                    self.assertIn(key, testcases[case])
                    self.assertEqual(testcases[case]["testNumber"], int(case))
                    if key in ["title", "description", "detailedDescription", "date_created", "path", "question"]:
                        # fields have to be a string and not empty
                        self.assertIsInstance(testcases[case][key], str)
                        self.assertGreater(len(testcases[case][key]), 0)
                    elif key in ["tagNums", "possibleAnswers"]:
                        # fields have to be a list and not None
                        self.assertIsInstance(testcases[case][key], list)
                        self.assertGreater(len(testcases[case][key]), 0)       

                        for tag_num in testcases[case]["tagNums"]:
                            self.assertEqual(tags[str(tag_num)]["tagNumber"], tag_num)
                            self.assertIsInstance(tags[str(tag_num)]["tagText"], str)
                            self.assertGreater(len(tags[str(tag_num)]["tagText"]), 0)

                        for ans in testcases[case]["possibleAnswers"]:
                            self.assertIsInstance(ans["ans_id"], int)
                            # ans_id 0-10(include)
                            self.assertIn(ans["ans_id"], range(0,11))
                            self.assertIsInstance(ans["ans_desc"], str)
                            self.assertGreater(len(ans["ans_desc"]), 0)    
    
if __name__ == '__main__':
    unittest.main()