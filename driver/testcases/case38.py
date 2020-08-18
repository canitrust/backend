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

class Case38(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 38

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """

        def checkTab1URL(urlName):
            webDriver.switch_to_window(tab1)
            self.data[urlName] = webDriver.current_url
            webDriver.switch_to_window(tab2)

        def check4opener(resultName):
            try:
                WebDriverWait(webDriver, 2).until(EC.presence_of_element_located((By.ID, 'result')))
                print(webDriver.find_element_by_id("result").get_attribute("innerHTML"))
                status = webDriver.find_element_by_id("result").get_attribute("innerHTML")
                if (status == "opener existing"):
                    self.data[resultName] = 1
                else:
                    self.data[resultName] = 0
            except TimeoutException:
                self.data[resultName] = 9

        self.data = {}
        # load initial URL which is vulnerable to reverse tabnabbing
        webDriver.get("http://plain.test-canitrust.com/reverseTabnabbing_startTab.html")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        self.data['initialUrlTab1'] = webDriver.current_url
        tab1 = webDriver.window_handles[0]
        # click on link to open new tab
        webDriver.find_element_by_id("link").click()
        time.sleep(3)
        tab2 = webDriver.window_handles[1]
        webDriver.switch_to_window(tab2)
        checkTab1URL('step1')
        check4opener('opener')
        # click on link in target tab (will be opened in the same tab)
        webDriver.find_element_by_id("link").click()
        time.sleep(3)
        checkTab1URL('step2')
        check4opener('opener_after_link')
        # enter new URL and check opener
        webDriver.get("http://www.alternative-canitrust.com/reverseTabnabbing_manualTarget.html")
        time.sleep(3)
        checkTab1URL('step3')
        check4opener('opener_entered_url')
        webDriver.close()
        return 1

    def evaluate(self):
        result = 1
        if (self.data['opener'] == 1):
            result = 3
        if (self.data['opener_after_link'] == 1):
            result = 4
        if (self.data['opener_entered_url'] == 1):
            result = 5
        self.result = result