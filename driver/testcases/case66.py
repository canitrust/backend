from testcases.testCase import TestCase
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from helper import Logger
import time
logger = Logger(__name__).logger

class Case66(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 66

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """
        webDriver.get("https://ssl.test-canitrust.com/svg-img.html")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.ID, 'changeme')))
        # Wait for svg run script
        time.sleep(2)
        p_content = webDriver.find_element_by_id('changeme').text
        self.data = {'content': p_content}
        webDriver.close()

        return 1

    def evaluate(self):
        if self.data['content'] == 'no change':
          result = 1
        elif self.data['content'] == 'SVG':
          result = 0
        else:
          result = 9

        self.result = result
