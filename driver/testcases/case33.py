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

        webDriver.get("http://case33.test-canitrust.com/?payload=%3Cobject%20data=%22javascript:(function(){p=document.createElement(%27p%27);p.id=p.innerHTML=%27exploited%27;document.body.appendChild(p)}())%22%3E%3C/object%3E")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        try:
            WebDriverWait(webDriver, 2).until(EC.presence_of_element_located((By.ID, 'exploited')))
            self.data = {'CSPblocked': 0}
        except TimeoutException:
            self.data = {'CSPblocked': 1}
        webDriver.close()
        return 1

    def evaluate(self):
        self.result = self.data['CSPblocked']
