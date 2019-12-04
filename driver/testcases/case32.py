from testcases.testCase import TestCase
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from helper import Logger
logger = Logger(__name__).logger

class Case32(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 32

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """
        webDriver.get("http://samesite1.test-canitrust.com/")
        WebDriverWait(webDriver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        webDriver.get("http://samesite2.test-canitrust.com/samesite.php")
        WebDriverWait(webDriver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        cookie_samesite = webDriver.find_element_by_id("cookie_samesite").text
        webDriver.close()

        self.data = { "cookie_samesite" : cookie_samesite }
        return 1

    def evaluate(self):
        result = 0
        if self.data['cookie_samesite'].strip() ==  "NO":
            result = 1
        self.result = result
