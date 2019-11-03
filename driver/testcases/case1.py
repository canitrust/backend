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

class Case1(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 1

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """
        webDriver.get("https://ssl.test-canitrust.com")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        webDriver.get("http://sub.ssl.test-canitrust.com")
        WebDriverWait(webDriver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        first_HSTS = webDriver.current_url
        webDriver.get("http://plain.test-canitrust.com")
        WebDriverWait(webDriver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        second_HSTS = webDriver.current_url
        if "https" in second_HSTS:
            webDriver.close()
            new_browser = TestCase.testSpawnBS(self.platform, self.os_version, self.browser, self.version, self.key, self.user)
            new_browser.get("https://ssl.test-canitrust.com")
            WebDriverWait(new_browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            new_browser.get("http://test-canitrust.com")
            WebDriverWait(new_browser, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            third_HSTS = new_browser.current_url
            new_browser.close()
        else:
            webDriver.get("http://test-canitrust.com")
            WebDriverWait(webDriver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            third_HSTS = webDriver.current_url
            webDriver.close()
        self.data = {'first_HSTS': first_HSTS, 'second_HSTS': second_HSTS, 'third_HSTS': third_HSTS}
        return 1

    def evaluate(self):
        """ Evaluate the raw data collected from browserstack to one of the expected results
            Evaluated result (int) must be compliant with the testcase definition
        """
        result = 0 # Default value - meaning no https for other domains (includeSubdomain or HSTS is not supported)
        if "https" in self.data['first_HSTS']:
            result = 2 # https for only sub.ssl.test-canitrust.com
            if "https" in self.data['second_HSTS']:
                if "https" in self.data['third_HSTS']:
                    result = 5 # https for every others
                else:
                    result = 3 # https for sub.ssl.test-canitrust.com & plain.test-canitrust.com
            elif "https" in self.data['third_HSTS']:
                result = 4 # http for plain.test-canitrust.com but https for test.canitrust.com
        self.result = result
