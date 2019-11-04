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

class Case17(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 17

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """
        webDriver.get("https://sslsub1.test-canitrust.com/cookies-max-age-vs-expires.html")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        time.sleep(6)
        try:
            # test2: max-age(2) < expires(5)
            oTest2 = webDriver.find_element_by_id('test2')
            textTest2 = str(oTest2.get_attribute('innerHTML'))
            countsTest2 = textTest2.count('ping: 1')
            if (countsTest2 == 1):
                dataTest2 = 'max-age'
            elif (countsTest2 == 4):
                dataTest2 = 'expires'
            else:
                dataTest2 = 'error'
            # test3: max-age(5) > expires(2)
            oTest3 = webDriver.find_element_by_id('test3')
            textTest3 = str(oTest3.get_attribute('innerHTML'))
            countsTest3 = textTest3.count('ping: 1')
            if (countsTest3 == 4):
                dataTest3 = 'max-age'
            elif (countsTest3 == 1):
                dataTest3 = 'expires'
            else:
                dataTest3 = 'error'
            data = {'resultTest2':dataTest2,'resultTest3':dataTest3}
            self.data = data
        except:
            print('error')
            return 0
        return 1

    def evaluate(self):
        # to check if always 'max-age' was considered
        resultTest2 = self.data['resultTest2']
        resultTest3 = self.data['resultTest3']
        if ((resultTest2 == 'max-age') and (resultTest3 == 'max-age')):
            # max-age defines the life time
            self.result = 1
        elif ((resultTest2 == 'expires') and (resultTest3 == 'expires')):
            # expires defines the life time (deprecated)
            self.result = 2
        else:
            # differing results
            self.result = 0
