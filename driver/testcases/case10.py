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

class Case10(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 10

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """
        webDriver.get("http://plain.test-canitrust.com")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        webDriver.get("https://ssl.test-canitrust.com")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        cookies = webDriver.get_cookies()
        self.data = {'set_cookies' : cookies}
        webDriver.close()
        return 1

    def evaluate(self):
        #if cookie is in cookies which is set by other domain
        result = 0
        cookie_set = 0
        cookie_flag = 0

        for cookie in self.data['set_cookies']:
            try:
                if 'cookie4 ' in cookie['name']:
                  cookie_set = 1
                  if cookie['secure'] == True:
                    cookie_flag = 1 
            except TypeError:
                cookie_set = 0

        if cookie_set == 1:
          if cookie_flag == 1:
            result = 0
          else:
            result = 10
        else:
          result = 1
        self.result = result
