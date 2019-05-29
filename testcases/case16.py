# ------------------------------------------------------------------------------------------------
#  Copyright (c) mgm security partners GmbH. All rights reserved.
#  Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
#-------------------------------------------------------------------------------------------------

from testCase import TestCase
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class Case16(TestCase):
    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 16

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """
        webDriver.get("https://ssl.test-canitrust.com/iframe3.html")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        iframe1 = webDriver.find_element(By.ID, 'iframe1')
        iframe2 = webDriver.find_element(By.ID, 'iframe2')

        webDriver.switch_to.frame(iframe1)
        isIframe1Loaded = "Hello" in webDriver.find_element(By.TAG_NAME, 'body').text
        webDriver.switch_to.default_content()

        webDriver.switch_to.frame(iframe2)
        isIframe2Loaded = "Hello" in webDriver.find_element(By.TAG_NAME, 'body').text
        webDriver.close()

        self.data = {'iframe1': isIframe1Loaded, 'iframe2': isIframe2Loaded}

        return 1

    def evaluate(self):
        isIframe1Loaded = self.data['iframe1']
        isIframe2Loaded = self.data['iframe2']

        # if only the first iframe was loaded, the last X-Frame-Options is used
        if (isIframe1Loaded and not isIframe2Loaded):
            self.result = 2
        
        # if only the second iframe was loaded, the first X-Frame-Options is used
        elif (not isIframe1Loaded and isIframe2Loaded):
            self.result = 3
        
        # if both iframes were loaded, Allow-From is more dominant
        elif (isIframe1Loaded and isIframe2Loaded):
            self.result = 4
        
        # If neither iframe was loaded, DENY is more dominant
        elif (not isIframe1Loaded and not isIframe2Loaded):
            self.result = 5
