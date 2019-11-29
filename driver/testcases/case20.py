# ------------------------------------------------------------------------------------------------
#  Copyright (c) mgm security partners GmbH. All rights reserved.
#  Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
#-------------------------------------------------------------------------------------------------

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from testcases.testCase import TestCase
from helper import Logger
logger = Logger(__name__).logger

class Case20(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 20

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """
        webDriver.get("https://cache3.test-canitrust.com/cache3.cgi")
        WebDriverWait(webDriver, 15).until(EC.presence_of_element_located((By.TAG_NAME, 'span')))
        html1 = webDriver.find_element_by_tag_name('span')
        randomString1 = html1.text
        webDriver.get("https://cache3.test-canitrust.com/cache3.cgi")
        WebDriverWait(webDriver, 15).until(EC.presence_of_element_located((By.TAG_NAME, 'span')))
        html2 = webDriver.find_element_by_tag_name('span')
        randomString2 = html2.text     
        self.data = {'randomString1': randomString1, 'randomString2': randomString2}
        webDriver.close()
        return 1

    def evaluate(self):
        # when randomString1 is not equal to randomString2, it means the browser sent a 2nd request to the server
        # => cache not stored 
        if (self.data['randomString1'] != self.data['randomString2']):
            self.result = 2
        # when randomString1 is equal to randomString2, it means the browser did not send a 2nd request to the server
        # => cache stored
        elif (self.data['randomString1'] == self.data['randomString2']):
            self.result = 3
