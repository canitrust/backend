# ------------------------------------------------------------------------------------------------
#  Copyright (c) mgm security partners GmbH. All rights reserved.
#  Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
#-------------------------------------------------------------------------------------------------

from testcases.testCase import TestCase
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

class Case37(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 37

    def executeTest(self, webDriver):
        webDriver.get("http://csp5.test-canitrust.com/contradict-csp-header-and-meta1.html")
        WebDriverWait(webDriver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'script')))
        content1 = webDriver.find_element_by_id('content1').text
        webDriver.get("http://csp6.test-canitrust.com/contradict-csp-header-and-meta2.html")
        WebDriverWait(webDriver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'script')))
        content2 = webDriver.find_element_by_id('content2').text
        webDriver.close()

        self.data = { 'content1': content1, 'content2': content2 }
        return 1

    def evaluate(self):
        if self.data['content1'] == 'Content1':
          if self.data['content2'] == 'Content2':
            result = 2
        else:
          result = 0

        self.result = result
