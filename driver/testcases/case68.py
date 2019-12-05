from testcases.testCase import TestCase
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from helper import Logger
logger = Logger(__name__).logger

class Case68(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 68

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """
        webDriver.get("https://ssl.test-canitrust.com/svg-embed.html")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        try:
          WebDriverWait(webDriver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'p')))
          p_content = webDriver.find_element_by_tag_name('p').text
          self.data = {'content': p_content}
        except:
          self.data = {'content': 'no change'}
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
