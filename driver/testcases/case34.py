# ------------------------------------------------------------------------------------------------
#  Copyright (c) mgm security partners GmbH. All rights reserved.
#  Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
#-------------------------------------------------------------------------------------------------

from testcases.testCase import TestCase
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from helper import Logger
logger = Logger(__name__).logger

class Case34(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 34

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """

        webDriver.get("http://case34.test-canitrust.com/?id=1;_")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        time.sleep(1)
        content = webDriver.find_element_by_tag_name("p").text
        self.data = {'content': content.strip()}
        webDriver.close()
        return 1

    def evaluate(self):
        if 'exploited' in self.data['content']:
            self.result = 0
        elif 'safe' in self.data['content']:
            self.result = 1
        else:
            self.result = 9
