# ------------------------------------------------------------------------------------------------
#  Copyright (c) mgm security partners GmbH. All rights reserved.
#  Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
#-------------------------------------------------------------------------------------------------

from testcases.testCase import TestCase
from helper import Logger
logger = Logger(__name__).logger

class Case9(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 9

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """

        webDriver.get("https://ssl.test-canitrust.com/setHttpCookie.html")
        set_cookies = webDriver.get_cookies()
        
        span = webDriver.find_element_by_tag_name('span')
        read_cookies = ''
        if span:
            read_cookies = span.text

        webDriver.close()

        self.data = {'set_cookies': set_cookies, 'read_cookies': read_cookies}
        return 1

    def evaluate(self):
        result = 0
        cookie_set = 0
        cookie_read = 0

        for cookie in self.data['set_cookies']:
            try:
                if 'cookie3' in cookie['name']:
                  cookie_set = 1
            except TypeError:
                cookie_set = 0
        
        if 'cookie3' in self.data['read_cookies']:
            cookie_read = 1
        
        if cookie_set == 1 :
            if cookie_read == 1:
                result = 0
            else:
                result = 10
        else:
            result = 1
        self.result = result
