# ------------------------------------------------------------------------------------------------
#  Copyright (c) mgm security partners GmbH. All rights reserved.
#  Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
#-------------------------------------------------------------------------------------------------

from testCase import TestCase
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

class Case15(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 15

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """
        webDriver.get("https://csp3.test-canitrust.com/iframe2.html")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        seq = webDriver.find_elements_by_tag_name('iframe')
        self.data ={}
        for index in range(len(seq)):
            iframe = webDriver.find_elements_by_tag_name('iframe')[index]
            if iframe == []:
                var = 'text' + str(index)
                data = {var: 'iframe not loaded'}
                self.data.update(data)    
                break
            webDriver.switch_to.frame(iframe)
            try:
                element=webDriver.find_elements_by_tag_name('h1')
                if element:
                    var = 'text' + str(index)
                    data = {var: element[0].text}
                    self.data.update(data)
                else:
                    var = 'text' + str(index)
                    data = {var: 'iframe not loaded'}
                    self.data.update(data)
                webDriver.switch_to.default_content()
            except:
                var = 'text' + str(index)
                data = {var: 'iframe not loaded'}
                self.data.update(data)    
        webDriver.close()
        return 1

    def evaluate(self):
        # to check which iframes have been loaded
        frame1 = False
        frame2 = False
        if ('Hello World!' in self.data['text0']):
            frame1 = True
            self.result = 1
        if ('Hello World!' in self.data['text1']):
            frame2 = True
            self.result = 7
        if frame1 and frame2:
            self.result = 6
        if not frame1 and not frame2:
            self.result = 9
