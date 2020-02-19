# ------------------------------------------------------------------------------------------------
#  Copyright (c) mgm security partners GmbH. All rights reserved.
#  Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
#-------------------------------------------------------------------------------------------------

from testcases.testCase import TestCase
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from helper import Logger
import urllib.parse
import time as time
import os, signal

logger = Logger(__name__).logger

content_types = [
    # "audio/aac",
    # "application/x-abiword",
    # "application/x-freearc",
    # "video/x-msvideo",
    # "application/vnd.amazon.ebook",
    "application/octet-stream",
    # "image/bmp",
    # "application/x-bzip",
    # "application/x-bzip2",
    # "application/x-csh",
    "text/css",
    # "text/csv",
    # "application/msword",
    # "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    # "application/vnd.ms-fontobject",
    # "application/epub+zip",
    # "application/gzip",
    "image/gif",
    "text/html",
    # "image/vnd.microsoft.icon",
    # "text/calendar",
    # "application/java-archive",
    "image/jpeg",
    "text/javascript",
    # "application/json",
    # "application/ld+json",
    # "audio/midi audio/x-midi",
    # "text/javascript",
    # "audio/mpeg",
    # "video/mpeg",
    # "application/vnd.apple.installer+xml",
    # "application/vnd.oasis.opendocument.presentation",
    # "application/vnd.oasis.opendocument.spreadsheet",
    # "application/vnd.oasis.opendocument.text",
    # "audio/ogg",
    # "video/ogg",
    # "application/ogg",
    # "audio/opus",
    # "font/otf",
    # "image/png",
    # "application/pdf",
    # "application/php",
    # "application/vnd.ms-powerpoint",
    # "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    # "application/x-rar-compressed",
    # "application/rtf",
    # "application/x-sh",
    # "image/svg+xml",
    # "application/x-shockwave-flash",
    # "application/x-tar",
    # "image/tiff",
    # "video/mp2t",
    # "font/ttf",
    # "text/plain",
    # "application/vnd.visio",
    "audio/wav",
    # "audio/webm",
    "video/webm",
    # "image/webp",
    "font/woff",
    # "font/woff2",
    # "application/xhtml+xml",
    # "application/vnd.ms-excel",
    # "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    # "application/xml",
    "text/xml",
    # "application/vnd.mozilla.xul+xml",
    "application/zip",
    # "video/3gpp",
    # "audio/3gpp ",
    # "video/3gpp2",
    # "audio/3gpp2",
    # "application/x-7z-compressed",
    "aaa",
    "some/thing" 
]

#Close session
def handler(signum, frame):
    raise Exception('Action took too much time')
    # source: https://stackoverflow.com/questions/3810869/python-timeout-of-try-except-statement-after-x-number-of-seconds

class Case36(TestCase):

    def __init__(self):
        TestCase.__init__(self)
        self.testCaseNum = 36

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """
        
        self.data = {}

        if "firefox" in self.browser.lower():
            # this test does not runs in Firefox
            for content_type in content_types:
                self.data[content_type] = "aborted"
        else:
            # start loop
            for content_type in content_types:
                # create new temp webDriver for each Content-Type test
                tmpWebDriver = TestCase.spawnWebDriver()

                # load defaulf page as a primary test
                tmpWebDriver.get("https://nosniff_dynamic.test-canitrust.com/")
                try:
                    WebDriverWait(tmpWebDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                except:
                    # error with test
                    logger.debug("error loading test site")

                # setup time for the case when webdriver stucks at the download window            
                signal.signal(signal.SIGALRM, handler)
                signal.alarm(5) #Set the parameter to the amount of seconds you want to wait
                
                try:
                    tmpWebDriver.get("https://nosniff_dynamic.test-canitrust.com/nosniff.php?nosniff=false&content_type=" + urllib.parse.quote(content_type))
                    # server returns file with content-type and with X-Content-Type-Options: nosniff depending on the URL parameters
                    # nosniff = true; XCTO = nosniff is set; nosniff = false; XCTO is not set
                except Exception as e:
                    # the exception rises when the time set (see above) exceeded when performing the steps in try
                    # in the case the download window shows up, the webdriver hangs and needs to be killed
                    self.data[content_type] = "download"
                    try:
                        os.system("ps -C firefox -o pid=|xargs kill -9") # kills all firefox sessions on linux based systems (local)
                        # only required for Firefox when running a local test
                    except:
                        pass
                    continue

                signal.alarm(10) #Resets the alarm to 10 new seconds
                signal.alarm(0) #Disables the alarm 

                # evaluation phase
                try:
                    WebDriverWait(tmpWebDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                    oHeadline = tmpWebDriver.find_element_by_id('headline')
                    textHeadline = str(oHeadline.get_attribute('innerHTML'))
                    if (textHeadline == "XSS exploited"):
                        self.data[content_type] = "exploited"
                    else:
                        self.data[content_type] = "not sniffed"
                except:
                    self.data[content_type] = "not sniffed"
                tmpWebDriver.close()
                #logger.debug(self.data)
                logger.debug(content_type + ": " + self.data[content_type])
            # end loop
            webDriver = TestCase.spawnWebDriver() # creates new webDriver (because original webDriver is probably killed)
            return 1

    def evaluate(self):
        logger.debug("--== Data evaluation ==--")
        logger.debug(self.data)
        counter = 0
        result = 1 # green
        for content_type in content_types:
            logger.debug(content_type + ": " + self.data[content_type])
            if ('exploited' in self.data[content_type]):
                # response sniffed, rendered and XSS exploited
                counter = counter + 1
        logger.debug("No. of exploited Content-Types: " + str(counter))
        if counter != 0:
            result = counter # 1=green, expected from text/html, all above will result in higher result/different color
        else:
            result = 8 # special case when Firefox test is skipped
        self.result = result
