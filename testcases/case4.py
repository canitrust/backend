# ------------------------------------------------------------------------------------------------
#  Copyright (c) mgm security partners GmbH. All rights reserved.
#  Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
#-------------------------------------------------------------------------------------------------

from testCase import TestCase
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

class Case4(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 4

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """
        httpsTargets = ["https://ssl.test-canitrust.com",
            "https://sslsub2.test-canitrust.com",
            "https://sslsub3.test-canitrust.com",
            "https://sslsub4.test-canitrust.com",
            "https://sslsub5.test-canitrust.com",
            "https://sslsub6.test-canitrust.com",
            "https://sslsub7.test-canitrust.com",
            "https://sslsub8.test-canitrust.com"]
        print(httpsTargets)
        self.data = {}
        counter = 1
        for target in httpsTargets:
            webDriver.get(target)
            WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            webDriver.get(target.replace('https','http'))
            WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            currentURL = webDriver.current_url
            data = {'case'+str(counter): ('https' in currentURL)}
            counter = counter + 1
            self.data.update(data)
            if ('https' in currentURL):
                print('HSTS header applied')
            else:
                print('HSTS not header applied')
            #webDriver.close()
            #webDriver = TestCase.spawnWebDriver()
            #webDriver = TestCase.testSpawnBS(self.platform, self.os_version, self.browser, self.version, self.key, self.user)
        webDriver.close()
        print(self.data)
        return 1
        

    def evaluate(self):
        # to check whether current url changed into https. this indicate hsts work or not
        result = 0
        for index in range(len(self.data)):
            if self.data['case'+str(index+1)] == True:
                print('case'+str(index+1) + ' yes')
                result = index+1
        self.result = result
        
        # if ('https' in self.data['subcase1_current_url']):
        #   self.result = 1
        # else:
        #   self.result = 0
        # if ('https' in self.data['subcase2_current_url']):
        #   print('case 2 yes')
        # else:
        #   print('case 2 no')
        