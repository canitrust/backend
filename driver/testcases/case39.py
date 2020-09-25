# ------------------------------------------------------------------------------------------------
#  Copyright (c) mgm security partners GmbH. All rights reserved.
#  Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
# -------------------------------------------------------------------------------------------------

from testcases.testCase import TestCase
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from helper import Logger
logger = Logger(__name__).logger


class Case39(TestCase):

    def __init__(self, variationId=None, variationData=None):
        TestCase.__init__(self)
        self.testCaseNum = 39
        self.variationId = variationId
        self.variationData = variationData

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """

        if self.variationData is None:
            # This is the Default variant
            self.variationId = 0

        # Translating variation data into corresponding testapp
        testapp = {
            0: 'https://cors-cache-misc.test-canitrust.com/website-cookie-so-xhr.html',
            1: 'https://cors-cache-misc.test-canitrust.com/website-cookie-so-fetch.html',
            2: 'https://cors-cache-misc.test-canitrust.com/website-jwt-so-xhr.html',
            3: 'https://cors-cache-misc.test-canitrust.com/website-jwt-so-fetch.html',
            4: 'https://cors-cache-misc.test-canitrust.com/website-jwt-co-xhr.html',
            5: 'https://cors-cache-misc.test-canitrust.com/website-jwt-co-fetch.html',
            6: 'https://cors-cache-misc.test-canitrust.com/website-custom-so-fetch.html',
            7: 'https://cors-cache-misc.test-canitrust.com/website-custom-co-fetch.html',
            8: 'https://joe:5ecr3t@cors-cache-misc.test-canitrust.com',
            10: 'https://cors-cache-misc.test-canitrust.com/website-cookie-login.php?user=joe&pw=5ecr3t'
        }
        attackerapp = {
            0: 'http://alternative-canitrust.com/case39/foreignwebsite-so.html',
            1: 'http://alternative-canitrust.com/case39/foreignwebsite-so.html',
            2: 'http://alternative-canitrust.com/case39/foreignwebsite-so.html',
            3: 'http://alternative-canitrust.com/case39/foreignwebsite-so.html',
            4: 'http://alternative-canitrust.com/case39/foreignwebsite-co.html',
            5: 'http://alternative-canitrust.com/case39/foreignwebsite-co.html',
            6: 'http://alternative-canitrust.com/case39/foreignwebsite-so.html',
            7: 'http://alternative-canitrust.com/case39/foreignwebsite-co.html',
            8: 'http://alternative-canitrust.com/case39/foreignwebsite-basic.html',
            10: 'http://alternative-canitrust.com/case39/foreignwebsite-active.html'
        }
        websiteURL = testapp[self.variationId]
        foreignWebsiteURL = attackerapp[self.variationId]

        # This helper function gets the API response in the context of the front-end page that called the API
        def checkAPIcontent(resultName):
            try:
                WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.ID, 'result')))
                status = webDriver.find_element_by_id('result').text
                self.data[resultName] = status
            except TimeoutException:
                self.data['error'] = True

        self.data = {}
        # request website which contains the API-Call with creating the cookie
        webDriver.get(websiteURL)
        print('Original website requested')
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        # check if the api call returns the secret
        checkAPIcontent('authenticated_request')
        # visit the foreign website
        webDriver.get(foreignWebsiteURL)
        print('Called foreignWebsite')
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        # now check the result of the subsequent api call from the foreing website
        checkAPIcontent('unauthenticated_request')
        webDriver.close()
        return 1

    def evaluate(self):
        result = 9
        if 'error' in self.data or self.data['authenticated_request'] != 'secret':
            result = 9
        elif self.data['unauthenticated_request'] == 'secret':
            # the issue is exploitable (result code = 0/red)
            result = 0
        elif self.data['unauthenticated_request'] == 'nosecret':
            # the issue is not exploitable (result code = 1/green)
            result = 1
        else:
            result = 9

        self.result = result
