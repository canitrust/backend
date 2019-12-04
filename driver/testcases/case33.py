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
logger = Logger(__name__).logger

class Case33(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 33

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """

        # Check the virtualhost works or not
        webDriver.get("http://case33.test-canitrust.com/?payload=<object%20data=\"javascript:alert(1)\"></object>")
        try:
            WebDriverWait(webDriver, 2).until(EC.alert_is_present())
            self.data = {'bypassed': 1}
        except TimeoutException:
            self.data = {'bypassed': 0}
        webDriver.close()
        return 1  

    def evaluate(self):
        self.result = self.data['bypassed']
