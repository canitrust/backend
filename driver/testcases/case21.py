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

class Case21(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 21

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """
        webDriver.get("https://cache4.test-canitrust.com")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'span')))
        html1 = webDriver.find_element_by_tag_name('span')
        randomString1 = html1.text
        webDriver.get("https://cache4.test-canitrust.com")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'span')))
        html2 = webDriver.find_element_by_tag_name('span')
        randomString2 = html2.text
        self.data = {'randomString1': randomString1, 'randomString2': randomString2}
        webDriver.close()
        return 1

    def evaluate(self):
        # when randomString1 is not equal to randomString2, it means the browser sent a 2nd request to the server
        # => cache not stored => answer a) + c)
        # in this case, we actually need to check whether there is a header "If-None-Match"/"If-Modified-Since" in the 2nd request or not.
        # However, we haven't figured out how to check request headers without proxy so we combine answer a) and c) in one.
        # This needs to be fixed later.
        if (self.data['randomString1'] != self.data['randomString2']):
            self.result = 2
        # when randomString1 is equal to randomString2, it means the browser did not send a 2nd request to the server
        # => cache stored => answer b)
        elif (self.data['randomString1'] == self.data['randomString2']):
            self.result = 3
        # classifying answers hasn't been completed yet, need to be fixed later.
