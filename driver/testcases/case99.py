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

class Case99(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 99

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """
        webDriver.get("http://jsonpinc.test-canitrust.com/case99/index.html")
        WebDriverWait(webDriver, 10).until(EC.title_contains(('finished')))
        div_result = webDriver.find_element_by_tag_name("div").text

        webDriver.close()

        if (div_result == 'div_result'):
            self.data = {'div_result': '9'}
        else:
            self.data = {'div_result': div_result}

        return 1

    def evaluate(self):
	# Possible results:
	#  9 = driver issue
	#  8  = JS/page issue
	#  0  = test succeeded, nothing executed
	# >0  = test succeeded, something executed ("something" defined by value)
        self.result = self.data['div_result']
