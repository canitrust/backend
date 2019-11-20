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
import time

class Case11(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 11

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """
        webDriver.get("http://plain.test-canitrust.com/setSecureCookie.html")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        time.sleep(1)
        cookies = webDriver.get_cookies()
        self.data = {'Cookies': cookies}
        return 1

    def evaluate(self):
        self.result = 0 
        cookies = self.data['Cookies']
        standardCookieSet = False
        sslCookieSet = False
        for cookie in cookies:
            if ('standardCookie' in cookie['name']):
                standardCookieSet = True
            if ('secureCookie' in cookie['name']):
                sslCookieSet = True
        if (standardCookieSet == False):
            self.result = 0 # red, cookie definition failed
            return 0
        if (sslCookieSet == True):
            self.result = 7 # orange, not expected behavior, secure cookie set from JS loaded via HTTP
        else:
            self.result = 1 # green, expected behavior, secure cookie not set from JS loaded via HTTP
