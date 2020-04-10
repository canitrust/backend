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
import time
import socket
from config import constant, settings
import subprocess
from prettytable import PrettyTable

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
        # creates an instance of browserstack Local
        self.key = constant.API_KEY
        self.binary_path = os.path.abspath(os.path.dirname(__file__)) + '/BrowserStackLocal'
        self.logfile = os.path.abspath(os.path.dirname(__file__)) + '/bs-local.log'
        self.proc = subprocess.Popen([self.binary_path, '-d', 'start', '-logFile', self.logfile, self.key, '-forcelocal', '--verbose','3'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out, err) = self.proc.communicate()
        os.system('echo "" > "'+ self.logfile +'"')
          
    def stop(self):
        try:
            proc = subprocess.Popen([self.binary_path, 'stop'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (out, err) = proc.communicate()
        except Exception as e:
            return

    def running(self):
        with open(self.logfile, 'r') as logfile:
            line = logfile.readline()
            while line:  
                if 'Error:' in line.strip():
                    raise Exception(line)
                elif line.strip() == 'Press Ctrl-C to exit':
                    return True
                line = logfile.readline()
        return False


class Mongo:
    def __init__(self):
        self.client = pymongo.MongoClient(constant.DB_URL)
        self.db = self.client[constant.DB_DATABASE]
        self.coll = self.db[constant.DB_COLL]
        self.failed_tests = self.db[constant.DB_FAILED_TESTS]

    def close(self):
        self.client.close()


logger = Logger(__name__).logger

def pretty_output(results):
    pretty_output = PrettyTable(["Case #", "Browser", "Version", "Elapsed", "Result", "Data"])
    for result in results:
        pretty_output.add_row([result["testCaseNum"], result["browser"], result["version"], round(result["elapsedTime"],1), result["result"], result["data"]])
    return pretty_output.get_string(sortby="Case #")


def get_browser_support(bs_user, bs_key):
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

# data
def get_config():
    with open(os.path.abspath(os.path.dirname(__file__)) + '/config/map.json', "r") as read_it:
        settings.dataJson = json.load(read_it)
    with open(os.path.abspath(os.path.dirname(__file__)) + '/config/container.lock', "w") as lock:
        lock.write('true')
    if settings.TESTENV == 'bs':
        get_browser_support(constant.USERBS, constant.API_KEY)
        logger.info('Successful checking latest browser versions')
        with open(os.path.abspath(os.path.dirname(__file__)) + '/config/browsersupport.json', "r") as read_it:
            settings.browserSupport = json.load(read_it)


def start_infra():
    if settings.TESTENV == 'bs':
        logger.debug('Create browserstack-local instance...')
        settings.BS_INSTANCE = BS()
        start_bs_time = time.time()
        while not settings.BS_INSTANCE.running():
            time.sleep(3)
            if (time.time() - start_bs_time) > 30:
                raise Exception('Waiting for BrowserStack timeout > 30 secs')
        logger.debug('Browserstack-local instance is running...')
    # Unlock dns_server and test_app containers
        with open(os.path.abspath(os.path.dirname(__file__)) + '/config/container.lock', "w") as lock:
            lock.write('browserstack')
    elif settings.TESTENV == 'local':
        with open(os.path.abspath(os.path.dirname(__file__)) + '/config/container.lock', "w") as lock:
            lock.write('local')
    logger.debug('Wait for dns_server and test_app containers up...')
    start_containers_time = time.time()
    while not check_connect('dns_server', 53) or not check_connect('test_app', 80):
        time.sleep(3)
        if (time.time() - start_containers_time) > 60:
            raise Exception('Waiting for dns_server and test_app containers up timeout > 60 secs')
    # Update DNS server
    os.system('echo "nameserver {}" > /etc/resolv.conf'.format(socket.gethostbyname('dns_server')))
    logger.debug('Dns_server and test_app containers already up...')


def check_connect(address, port):
    s = socket.socket()
    try:
      s.connect((address, port))
      s.shutdown(2)
      return True
    except:
      return False
