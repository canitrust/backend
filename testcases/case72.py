from testCase import TestCase
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

class Case72(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 72

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """
        # Part 1
        webDriver.get("https://hsts1.test-canitrust.com")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        time.sleep(10)
        webDriver.get("http://hsts1.test-canitrust.com")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        first_URL = webDriver.current_url

        # Part 2
        webDriver.get("https://hsts2.test-canitrust.com")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        time.sleep(10)
        webDriver.get("http://hsts2.test-canitrust.com")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        second_URL = webDriver.current_url

        webDriver.close()

        self.data = {'first_url': first_URL, 'second_url': second_URL}

        return 1

    def evaluate(self):
        first_part_ssl = "https" in self.data['first_url']
        second_part_ssl = "https" in self.data['second_url']

        if (first_part_ssl and second_part_ssl):
          # always the longest max-age
          result = 2
        elif (first_part_ssl and not second_part_ssl):
          # always the second header
          result = 3
        elif (not first_part_ssl and second_part_ssl):
          # always the first header
          result = 4
        else:
          # always the shorstest max-age
          result = 5

        self.result = result
