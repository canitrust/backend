#  ------------------------------------------------------------------------------------------------
#   Copyright (c) mgm security partners GmbH. All rights reserved.
#   Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
#  #-------------------------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------------------------

__author__ = 'mgm-sp.com'

import requests
import json
import os
import sys
import logging
import pymongo
from config import constant
from browserstack.local import Local


def get_browser_support(bs_user, bs_key):
    logger = Logger(__name__).logger
    logger.info('Browser Support from Browser Stack')
    rq = 'https://api.browserstack.com/automate/browsers.json'
    rs = requests.get(rq, auth=(bs_user,bs_key), timeout=5)

    if rs.status_code == 200:
        list_bs_browsers = rs.json()
        list_cit_browsers = []
        for browser in list_bs_browsers:
            if (browser['os'] == 'Windows' and browser['os_version'] == '10') or (browser['os'] == 'OS X' and browser['browser'] == 'safari'):
                # Only need os, os version, browser, browser_version
                c = dict(browser)
                for (key, value) in c.items() :
                    if key not in ('os', 'os_version', 'browser', 'browser_version'):
                        del browser[key]
                list_cit_browsers.append(browser)
        logger.info('Browsers supported by BS: {}'.format(len(list_bs_browsers)))
        logger.info('Browsers supported by CIT: {}'.format(len(list_cit_browsers)))
        with open(os.path.abspath(os.path.dirname(__file__)) + '/config/browsersupport.json', 'w') as json_file:
            json.dump(list_cit_browsers, json_file, indent=4, sort_keys=True)
        return True

    return False


class Logger:
    def __init__(self, logger_name):
        self.formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.log_file = os.path.abspath(os.path.dirname(__file__)) + '/driver.log'
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.get_console_handler())
        logger.addHandler(self.get_file_handler())
        logger.propagate = False
        self.logger = logger

    def get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        return console_handler

    def get_file_handler(self):
        file_handler = logging.FileHandler(self.log_file, mode='w')
        file_handler.setFormatter(self.formatter)
        return file_handler


class BS:
    def __init__(self):
        # creates an instance of Local
        bs_local = Local()
        bs_local_args = {"key": constant.API_KEY, "forcelocal": "true", "binarypath": os.path.abspath(os.path.dirname(__file__)) + '/BrowserStackLocal'}

        # starts the Local instance with the required arguments
        bs_local.start(**bs_local_args)
        self.bs_local = bs_local

    def running(self):
        return self.bs_local.isRunning()

    # stop the Local instance
    def stop(self):
        self.bs_local.stop()


class Mongo:
    def __init__(self):
        self.client = pymongo.MongoClient(constant.DB_URL)
        self.db = self.client[constant.DB_DATABASE]
        self.coll = self.db[constant.DB_COLL]
        self.ignore_list = self.db[constant.DB_IGNORE_LIST]

    def close(self):
        self.client.close()
