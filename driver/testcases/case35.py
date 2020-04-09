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

#import time

class Case35(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 35

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """

        # Check the virtualhost works or not
        logger.debug("Before")
        webDriver.get("https://nosniff.test-canitrust.com/sniff.uct")
        logger.debug("After")
        # server returns file without content-type and with X-Content-Type-Options: nosniff
        self.data = {}
        try:
            WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            oHeadline = webDriver.find_element_by_id('headline')
            textHeadline = str(oHeadline.get_attribute('innerHTML'))
            if (textHeadline == "XSS exploited"):
                self.data = {'XSS': "exploited"}
            else:
                self.data = {'XSS': "safe"}
        except:
            self.data = {'XSS': "safe"}
        webDriver.close()
        return 1

    def evaluate(self):
        if ('exploited' in self.data['XSS']):
            # response sniffed, rendered and XSS exploited
            result = 7 # orange
        if ('safe' in self.data['XSS']):
            # response not sniffed or rendered, safe option
            result = 1 # green
        self.result = result
