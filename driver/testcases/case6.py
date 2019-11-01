# ------------------------------------------------------------------------------------------------
#  Copyright (c) mgm security partners GmbH. All rights reserved.
#  Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
#-------------------------------------------------------------------------------------------------

from testcases.testCase import TestCase
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from helper import Logger
logger = Logger(__name__).logger

class Case6(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 6

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """
        webDriver.get("https://ssl.test-canitrust.com")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        cookies = webDriver.get_cookies()
        webDriver.close()
        self.data = { 'data_cookies': cookies }
        return 1

    def evaluate(self):
        result = 0
        for cookie in self.data['data_cookies']:
            if cookie['name'] == 'cookie0':
                if cookie['value'] == 'value1':
                    result = 2
                else:
                    result = 3
        self.result = result
