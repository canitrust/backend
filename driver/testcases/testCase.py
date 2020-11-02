# ------------------------------------------------------------------------------------------------
#  Copyright (c) mgm security partners GmbH. All rights reserved.
#  Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
#-------------------------------------------------------------------------------------------------

import sys
import json
import datetime
from pymongo import MongoClient
from config import constant
import time
from helper import Logger
import os
import re
import threading

#import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

logger = Logger(__name__).logger

#Defining generic class:
class TestCase:
    #Base params
    testCaseNum = None
    browser = ""
    platform = ""
    version = ""
    elapsedTime = 0
    date = None
    data = {}
    result = None
    os_version= ""
    isBeta = False
    deprecated = False
    variationId = None
    variationData = None

    # Constructor
    def __init__(self):
        self.date = datetime.datetime.utcnow()
        self.isBeta = False
        self.deprecated = False
    def get_data(self):
        #get dict to insert from class
        result = {
                    "date": self.date,
                    "testCaseNum": self.testCaseNum,
                    "result" : self.result,
                    "platform": self.info_browser['os'],
                    "os_version":self.info_browser['os_version'],
                    "browser": self.info_browser['browser'],
                    "device": self.info_browser['device'],
                    "version": self.info_browser['browser_version'],
                    "elapsedTime": self.elapsedTime,
                    "data" : self.data,
                    "isBeta": self.isBeta,
                    "deprecated": self.deprecated
                }
        # Only mobile test results have real_mobile field
        if self.info_browser['os'] in ['ios', 'android']:
            result["real_mobile"] = self.info_browser['real_mobile']
        if self.variationId is not None:
            result["variationId"] = self.variationId
        return result

    # save info to DB (param1: mongo client)
    def saveToDB(self,mongoClient):
        myCollection = mongoClient[constant.DB_COLL]
        #check Beta version and bs_version
        if(any(s in self.version for s in ('beta', 'insider preview'))):
            self.isBeta = True

        data = self.get_data()
        # Debug message:
        logger.debug('Result to be saved:{}'.format(data))
        #save data
        savedItem = myCollection.insert(data)

    #to String for printing
    def __str__(self):
        my_dict = {"date": self.date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                    "testCaseNum": self.testCaseNum,
                    "result" : self.result,
                    "platform": self.platform,
                    "version": self.version,
                    "browser": self.browser,
                    "os_version": self.os_version,
                    "elapsedTime": self.elapsedTime,
                    "data" : self.data,
                    "isBeta": self.isBeta,
                    "deprecated": self.deprecated
                    }
        return json.dumps(my_dict)

    # Run the testcase against a specific browser version
    def run(self, info_browser, key, user, db):
        """ Run the testcase against a specific browser version
            (String) platform: operation system, eg. 'OS X'
            (String) osversion: OS version, eg. 'Mojave'
            (String) browser: browser name, eg. 'firefox'
            (String) version: version, eg. '56.0'
            (String) key: Browserstack API key
            (String) user: Browserstack username
            (Object) db: MongoDb instance
        """
        self.info_browser = info_browser
        self.key = key
        self.user = user
        logger.debug('Running testcase - with configs:{} {} {} {} {} {}'.format(info_browser['os'], info_browser['os_version'], info_browser['browser'], info_browser['device'], info_browser['browser_version'], info_browser['real_mobile']))
        try:
            webDriver = self.testSpawnBS()

            # start time - will be used to calculate elapsed time
            start_time = time.time()
            logger.debug('Running testcase - spawn - done')
            # Run the actual test definition
            flag = self.executeTest(webDriver)
            logger.debug('Running testcase - execute - done')
            # Elapsed time
            self.elapsedTime = time.time() - start_time

            # Evaluate the raw data. An evaluate function must be defined in each testcase script
            self.evaluate()
            logger.debug('Running testcase - evaluate - done')
            # Save
            self.saveToDB(db)
            logger.debug('Running testcase - save - done')
        except Exception as e:
            logger.error('Running testcase - Failed')
            logger.error(e)
            self.data = "Failed"
            self.result = "Failed"
        finally:
            try:
                if flag is 3:
                    logger.debug("Quit webDriver with new thread")
                    quitThread = threading.Thread(target=webDriver.quit)
                    quitThread.start()
                else:
                    webDriver.quit()
            except Exception as e:
                logger.error('Quit webdriver - Failed')
            data = self.get_data()
            return data

    # Run the testcase against a specific browser version
    def runnotsave(self, info_browser, key, user):
        """ Run the testcase against a specific browser version
            (String) platform: operation system, eg. 'OS X'
            (String) osversion: OS version, eg. 'Mojave'
            (String) browser: browser name, eg. 'firefox'
            (String) version: version, eg. '56.0'
            (String) key: Browserstack API key
            (String) user: Browserstack username
        """
        self.info_browser = info_browser
        self.key = key
        self.user = user
        logger.debug('Running testcase - with configs:{} {} {} {}'.format(self.platform, self.os_version, self.browser, self.version))
        try:
            webDriver = self.testSpawnBS()

            # start time - will be used to calculate elapsed time
            start_time = time.time()
            logger.debug('Running testcase - spawn - done')
            # Run the actual test definition
            flag = self.executeTest(webDriver)
            logger.debug('Running testcase - execute - done')
            # Elapsed time
            self.elapsedTime = time.time() - start_time

            # Evaluate the raw data. An evaluate function must be defined in each testcase script
            self.evaluate()
            logger.debug('Running testcase - evaluate - done')
        except Exception as e:
            logger.error('Running testcase - Failed')
            logger.error(e)
            self.data = "Failed"
            self.result = "Failed"
        finally:
            try:
                if flag is 3:
                    logger.debug("Quit webDriver with new thread")
                    quitThread = threading.Thread(target=webDriver.quit)
                    quitThread.start()
                else:
                    webDriver.quit()
            except Exception as e:
                logger.error('Quit webdriver - Failed')
            data = self.get_data()
            # Debug message:
            logger.debug('Result:{}'.format(data))
            return data
    def runLocal(self):
        """ Run the testcase against a local Firefox(geckodriver)
            geckodriver: version 0.24.0
            Firefox: latest
        """

        # set all the necessary field for displaying result
        self.info_browser = {
            "os": "Ubuntu(Linux)",
            "os_version": "13",
            "browser": "Firefox/Gecko",
            "browser_version": "latest"
        }
        try:
            # spawn a local gecko driver
            webDriver = TestCase.spawnWebDriver()
            logger.info("Firefox version: {}".format(webDriver.capabilities['browserVersion']))
            # start time - will be used to calculate elapsed time
            start_time = time.time()
            logger.debug('Running testcase - spawn - done')
            # Run the actual test definition
            flag = self.executeTest(webDriver)
            logger.debug('Running testcase - execute - done')
            # Elapsed time
            self.elapsedTime = time.time() - start_time

            # Evaluate the raw data. An evaluate function must be defined in each testcase script
            self.evaluate()
            logger.debug('Running testcase - evaluate - done')
        except Exception as e:
            logger.debug('Running testcase - Failed')
            logger.error(e)
            self.data = "Failed"
            self.result = "Failed"
        finally:
            try:
                if flag is 3:
                    logger.debug("Quit webDriver with new thread")
                    quitThread = threading.Thread(target=webDriver.quit)
                    quitThread.start()
                else:
                    webDriver.quit()
            except Exception as e:
                logger.error('Quit webdriver - Failed')
            data = self.get_data()
            logger.debug('Result:{}'.format(data))
            return data


    def respawn(self):
        if self.browser == "Firefox/Gecko":
            return self.spawnWebDriver()
        else:
            return self.testSpawnBS()


    #spawn web driver
    def spawnWebDriver(self):
        capabilities = DesiredCapabilities.FIREFOX.copy()
        capabilities['marionette'] = True
        #capabilities['loggingPrefs'] = { 'browser':'ALL' }
        options = Options()
        options.add_argument("--headless")
        profile = webdriver.FirefoxProfile(os.path.abspath(os.path.dirname(__file__)) + "/profile")
        profile.set_preference("network.proxy.type",0)
        profile.set_preference("browser.cache.disk.enable", False)
        profile.set_preference("browser.cache.memory.enable", False)
        profile.set_preference("browser.cache.offline.enable", False)
        profile.set_preference("network.http.use-cache", False)
        profile.set_preference("security.csp.enable", True)
        webDriver = webdriver.Firefox(firefox_profile=profile, capabilities=capabilities,firefox_options=options)
        return webDriver



    def testSpawnBS(self):
        desired_cap = {
            'resolution': '1024x768',
            'browserstack.local' : 'true',
            #'browserstack.debug': 'true',
            'browserstack.networkLogs':'true',
            'browserstack.appiumLogs':'true',
            'acceptSslCerts': 'false',
            'acceptInsecureCerts': 'true'
        }
        desired_cap.update(self.info_browser)
        print(str(desired_cap))
        if self.info_browser['browser'] == 'firefox':
            profile = webdriver.FirefoxProfile()
            profile.set_preference("security.csp.enable", True)
            profile.update_preferences()
            driver = webdriver.Remote(
                command_executor='http://'+ self.user +':'+ self.key + '@hub.browserstack.com:80/wd/hub',
                desired_capabilities=desired_cap, browser_profile=profile)
        else:
            driver = webdriver.Remote(
                command_executor='http://'+ self.user +':'+ self.key + '@hub.browserstack.com:80/wd/hub',
                desired_capabilities=desired_cap)
        # Get browser version on mobile devices
        if self.info_browser['real_mobile']:
            agent = driver.execute_script("return navigator.userAgent;")
            if self.info_browser['browser'] == "iphone":
                version = re.search(r'Version/(\d+\.\d+)', agent)
                if (version):
                    self.info_browser['browser'] = "safari"
                    self.info_browser['browser_version'] = version.group(1)
            elif self.info_browser['browser'] == "android":
                version = re.search(r'Chrome/(\d+\.\d+)', agent)
                if (version):
                    self.info_browser['browser'] = "chrome"
                    self.info_browser['browser_version'] = version.group(1)
        return driver

    def evaluate(self):
        """ This function MUST be extended in testcase definition class
            Evaluate the raw data collected from browserstack to one of the expected results
            Evaluated result (int) must be compliant with the testcase definition
        """
        pass

