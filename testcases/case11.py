# ------------------------------------------------------------------------------------------------
#  Copyright (c) mgm security partners GmbH. All rights reserved.
#  Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
#-------------------------------------------------------------------------------------------------

from testCase import TestCase
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
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
        #alert_box = webDriver.switch_to_alert()
        #alert_box.dismiss()
        cookies1 = webDriver.get_cookies()
        
        webDriver.get("https://ssl.test-canitrust.com")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        time.sleep(1)
        cookies2 = webDriver.get_cookies()

        self.data = {'step1Cookies': cookies1,'step2Cookies': cookies2}
        return 1

    def evaluate(self):
        self.result = 0
        #print(type(self.result)) 
        cookies = self.data['step2Cookies']
        standardCookieSet = False
        sslCookieSet = False
        for cookie in cookies:
            print(cookie)
            if ('standardCookie' in cookie['name']):
                standardCookieSet = True
            if ('secureCookie' in cookie['name']):
                sslCookieSet = True
        if (standardCookieSet == True):
            print('standard cookie set')
        else:
            print('standard cookie not set')
        if (sslCookieSet == True):
            print('secure cookie set')
            self.result = 0 # not expected behavior, secure cookie set from JS loaded via HTTP
        else:
            print('secure cookie not set')
            self.result = 1 # expected behavior, secure cookie not set from JS loaded via HTTP
        print(self.result)
        

        