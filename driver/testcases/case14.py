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

class Case14(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 14

    def executeTest(self, webDriver):
        webDriver.get("https://csp2.test-canitrust.com/scriptsrc.html")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'script')))
        textGetFromBrowser = webDriver.find_element_by_id('test')
        dataText = textGetFromBrowser.text
        webDriver.close()

        self.data = dataText
        return 1
        
    def evaluate(self):
        # if the script was not loaded, the second CSP took precedance
        if 'not loaded' in self.data:
            result = 2
        else:
            result = 3
        self.result = result
