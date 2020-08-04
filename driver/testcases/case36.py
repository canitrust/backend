# ------------------------------------------------------------------------------------------------
#  Copyright (c) mgm security partners GmbH. All rights reserved.
#  Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
# ------------------------------------------------------------------------------------------------

from testcases.testCase import TestCase
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from helper import Logger
import urllib.parse
import time as time
import os
import signal

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

# Close session


def handler(signum, frame):
    raise Exception('Action took too much time')
    # source: https://stackoverflow.com/questions/3810869/python-timeout-of-try-except-statement-after-x-number-of-seconds


class Case36(TestCase):

    def __init__(self, variationId=None, variationData=None):
        TestCase.__init__(self)
        self.testCaseNum = 36
        self.variationId = variationId
        self.variationData = variationData

    def executeTest(self, webDriver):
        """ Definition of a testcase
            Test result MUST be set to self.data
        """

        if self.variationId is None:
            self.data = {"content_type": "text/html"}
        else:
            self.data = {"content_type": self.variationData["content_type"]}

        if "firefox" in self.browser.lower():
            logger.debug("Skipping " + self.browser)
            # this test does not runs in Firefox
            self.data["result"] = "aborted"
        else:
            # load defaulf page as a primary test
            webDriver.get("https://nosniff_dynamic.test-canitrust.com/")
            try:
                WebDriverWait(webDriver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'body')))
            except:
                # error with test
                logger.debug("error loading test site")

            # setup time for the case when webdriver stucks at the download window
            signal.signal(signal.SIGALRM, handler)
            # Set the parameter to the amount of seconds you want to wait
            signal.alarm(5)

            try:
                webDriver.get(
                    "https://nosniff_dynamic.test-canitrust.com/nosniff.php?nosniff=false&content_type=" + urllib.parse.quote(self.data["content_type"]))
                # server returns file with content-type and with X-Content-Type-Options: nosniff depending on the URL parameters
                # nosniff = true; XCTO = nosniff is set; nosniff = false; XCTO is not set
            except:
                # the exception rises when the time set (see above) exceeded when performing the steps in try
                # in the case the download window shows up, the webdriver hangs and needs to be killed
                self.data["result"] = "download"
                logger.debug(self.data["content_type"] + ": " + self.data["result"])
                webDriver.close()
                return 1

            signal.alarm(10)  # Resets the alarm to 10 new seconds
            signal.alarm(0)  # Disables the alarm

            # evaluation phase
            try:
                WebDriverWait(webDriver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'body')))
                oHeadline = webDriver.find_element_by_id('headline')
                textHeadline = str(oHeadline.get_attribute('innerHTML'))
                if (textHeadline == "XSS exploited" and self.data["content_type"] is not "text/html"):
                    self.data["result"] = "exploited"
                else:
                    self.data["result"] = "not sniffed"

            except:
                self.data["result"] = "not sniffed"

            webDriver.close()
            return 1

    def evaluate(self):
        logger.debug("--== Data evaluation ==--")
        if "exploited" in self.data["result"]:
            self.result = 0
        elif "aborted" in self.data["result"]:
            self.result = 8
        else:
            self.result = 1
