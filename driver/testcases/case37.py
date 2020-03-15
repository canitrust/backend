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
        webDriver.get("http://csp7.test-canitrust.com/contradict-csp-header-and-meta3.html")
        WebDriverWait(webDriver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'script')))
        content3 = webDriver.find_element_by_id('content3').text
        webDriver.get("http://csp8.test-canitrust.com/contradict-csp-header-and-meta4.html")
        WebDriverWait(webDriver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'script')))
        content4 = webDriver.find_element_by_id('content4').text
        webDriver.get("http://csp9.test-canitrust.com/contradict-csp-header-and-meta5.html")
        WebDriverWait(webDriver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'script')))
        content5 = webDriver.find_element_by_id('content5').text
        webDriver.get("http://csp10.test-canitrust.com/contradict-csp-header-and-meta6.html")
        WebDriverWait(webDriver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'script')))
        content6 = webDriver.find_element_by_id('content6').text
        webDriver.close()

        self.data = { 'Header page 1': content1,
                      'Meta page 1': content2,
                      'Header page 2': content3,
                      'Meta page 2': content4,
                      'Is Looser page 1': content5,
                      'Is Looser page 2': content6 }
        return 1

    def evaluate(self):
        if self.data:
            result = 2
        else:
          result = 0

        self.result = result
