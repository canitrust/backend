# ------------------------------------------------------------------------------------------------
#  Copyright (c) mgm security partners GmbH. All rights reserved.
#  Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
#-------------------------------------------------------------------------------------------------

import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import json
from testcases.testCase import TestCase
from helper import Logger

logger = Logger(__name__).logger

class Case8(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 8
    
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
    
    def evaluate(self):
        result = 1 # setting cookie to a foreign domain is ignored - expected cookie was not found
        cookies = self.data['cookies_in_noexamplemgm']

        # Test whether cookies object is iterable to prevent bug in Edge
        try:
            iterator = iter(cookies)
        except TypeError:
            # not iterable
            result = 1
        else:
            # iterable
            for cookie in cookies:
                if cookie['name'] == 'cookie2' and cookie['value'] == 'value1':
                    # expected cookie was found
                    result = 0
                    break
        
        self.result = result
