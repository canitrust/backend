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
        content1 = webDriver.find_element_by_id('text').text
        webDriver.get("http://csp6.test-canitrust.com/contradict-csp-header-and-meta2.html")
        WebDriverWait(webDriver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'script')))
        content2 = webDriver.find_element_by_id('text').text
        webDriver.close()

        if content1 == 'No' and content2 == 'No':
            self.data = {'Stricter page 1 win, is script run?': content1,
                        'Stricter page 2 win, is script run?': content2,}
        elif content1 == 'Yes' and content2 == 'No':
            self.data = {'Meta page 1 win, is script run?': content1,
                        'Meta page 2 win, is script run?': content2,}
        elif content1 == 'No' and content2 == 'Yes':
            self.data = {'Header page 1 win, is script run?': content1,
                        'Header page 2 win, is script run?': content2,}
        elif content1 == 'Yes' and content2 == 'Yes':
            self.data = {'Looser page 1 win, is script run?': content1,
                        'Looser page 2 win, is script run?': content2}
        return 1

    def evaluate(self):
        if self.data:
            result = 2
        else:
            result = 0

        self.result = result
