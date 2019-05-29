# ------------------------------------------------------------------------------------------------
#  Copyright (c) mgm security partners GmbH. All rights reserved.
#  Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
#-------------------------------------------------------------------------------------------------

from testCase import TestCase

class Case12(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 12

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """
        webDriver.get("https://ssl.test-canitrust.com/setHttpCookie.html")
        alert_box = webDriver.switch_to_alert()
        alert_box.dismiss()
        cookies = webDriver.get_cookies()
        webDriver.close()
        first_time = cookies

        new_browser = TestCase.spawnWebDriver('Linux','Firefox','63')
        new_cookies = new_browser.get_cookies()
        new_browser.delete_all_cookies()
        new_browser.close()
        second_time = new_cookies

        self.data = {'first_cookies': cookies,'new_cookies': new_cookies}
        return 1

    def evaluate(self):
        # Todo
        pass