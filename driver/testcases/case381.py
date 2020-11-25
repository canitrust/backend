# ------------------------------------------------------------------------------------------------
#  Copyright (c) mgm security partners GmbH. All rights reserved.
#  Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
#-------------------------------------------------------------------------------------------------

from testcases.testCase import TestCase
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from helper import Logger
import time
logger = Logger(__name__).logger

class Case381(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 381

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """

        self.data = {}
        # load initial URL which is vulnerable to reverse tabnabbing
        webDriver.get("http://plain.test-canitrust.com/startTab.html")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # click on link to open new tab
        webDriver.find_element_by_id("link").click()
        time.sleep(3)
        
        webDriver.close()
        return 1

    def evaluate(self):
        result = 1
        # to be done
        self.result = result