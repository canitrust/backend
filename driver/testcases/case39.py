# ------------------------------------------------------------------------------------------------
#  Copyright (c) mgm security partners GmbH. All rights reserved.
#  Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
#-------------------------------------------------------------------------------------------------

from testcases.testCase import TestCase
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from helper import Logger
import time
logger = Logger(__name__).logger

class Case39(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 39

        websiteURL = "http://cors-cache-misc.test-canitrust.com/cors-cache-misc.website.php"
        websieAPIURL = "http://cors-cache-misc.test-canitrust.com/cors-cache-misc-websiteapi.php"
        foreignWebsiteURL = "http://cors-cache-misc.test-canitrust.com/cors-cache-misc-foreignwebsite.php"
        
    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """

        websiteURL = "http://cors-cache-misc.test-canitrust.com/cors-cache-misc-website.php"
        websieAPIURL = "http://cors-cache-misc.test-canitrust.com/cors-cache-misc-websiteapi.php"
        foreignWebsiteURL = "http://alternative-canitrust.com/cors-cache-misc-foreignwebsite.php"

        def checkAPIcontent(resultName):
            try:
                WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.ID, 'result')))
                status = webDriver.find_element_by_id("result").text
                if (status == "secret"):
                    self.data[resultName] = 1
                elif (status == "nosecret"):
                    self.data[resultName] = 0
                else:
                    self.data[resultName] = -1
            except TimeoutException:
                self.data[resultName] = 9



        self.data = {}
        #request website which contains the API-Call with creating the cookie
        webDriver.get(websiteURL)
        time.sleep(3)
        print("Original website requested")
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME,'body')))
        #check if the api call returns the secret
        checkAPIcontent('request_with_cookie')
        #visit the foreign website
        webDriver.get(foreignWebsiteURL)
        print("Called foreignWebsite")
        time.sleep(3)
        WebDriverWait(webDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        #now check the result of the subsequent api call from the foreing website
        checkAPIcontent('request_without_cookie')
        webDriver.close()
        return 1

    def evaluate(self):
        result = 0
        if(self.data['request_without_cookie'] == 1):
            result = 0
        elif(self.data['request_without_cookie'] == 0):
            result = 1
        else:
            result = 9

        if(self.data['request_with_cookie'] != 1):
            result = 9
            
        self.result = result
