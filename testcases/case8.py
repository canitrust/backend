# ------------------------------------------------------------------------------------------------
#  Copyright (c) mgm security partners GmbH. All rights reserved.
#  Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
#-------------------------------------------------------------------------------------------------

from testCase import TestCase
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import json

class Case8(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 8
    # Todo
    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """
        webDriver.get('https://ssl.test-canitrust.com')
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        webDriver.get('http://noexample.mgm') 
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        cookies = webDriver.get_cookies()
        webDriver.close()
        self.data = {'cookies_in_noexamplemgm': cookies}
        return 1
    # Todo
    def evaluate(self):
        result = 1 # setting cookie to a foreign domain is ignored - expected cookie was not found
        for cookie in self.data['cookies_in_noexamplemgm']:
            if cookie['name'] == 'cookie2' and cookie['value'] == 'value1':
                # expected cookie was found
                result = 0
                break
        self.result = result
