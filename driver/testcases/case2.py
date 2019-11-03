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

class Case2(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 2

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """
        webDriver.get("http://ssl2.test-canitrust.com")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        webDriver.get("http://ssl2.test-canitrust.com")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        currentURL = webDriver.current_url
        self.data = {'current_url': currentURL}
        webDriver.close()
        return 1

    def evaluate(self):
        # to check whether current url changed into https. this indicate hsts work or not
        if ('https' in self.data['current_url']):
          self.result = 1
        else:
          self.result = 0