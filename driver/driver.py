#  ------------------------------------------------------------------------------------------------
#   Copyright (c) mgm security partners GmbH. All rights reserved.
#   Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
#  #-------------------------------------------------------------------------------------------------
#
#
#

import argparse
import os
import json
import socket
import importlib
import logging
import time
from helper import get_browser_support, BS, Logger, Mongo
from config import constant

logger = Logger(__name__).logger
DB = None
BS_INSTANCE = None

def get_config():
    global dataJson, browserSupport
    with open(os.path.abspath(os.path.dirname(__file__)) + '/config/map.json', "r") as read_it:
        dataJson = json.load(read_it)
    with open(os.path.abspath(os.path.dirname(__file__)) + '/config/container.lock', "w") as lock:
        lock.write('true')
    if TESTENV == 'bs':
        get_browser_support(constant.USERBS, constant.API_KEY)
        logger.info('Successful checking latest browser versions')
        with open(os.path.abspath(os.path.dirname(__file__)) + '/config/browsersupport.json', "r") as read_it:
            browserSupport = json.load(read_it)

def start_infra():
    try:
        if TESTENV == 'bs':
            logger.debug('Create browserstack-local instance...')
            global BS_INSTANCE
            BS_INSTANCE = BS()
            start_bs_time = time.time()
            while not BS_INSTANCE.running():
                time.sleep(3)
                if (time.time() - start_bs_time) > 30:
                    raise Exception('Waiting for BrowserStack timeout > 30 secs')
            logger.debug('Browserstack-local instance is running...')
        # Unlock dns_server and test_app containers
        with open(os.path.abspath(os.path.dirname(__file__)) + '/config/container.lock', "w") as lock:
            lock.write('false')
        logger.debug('Wait for dns_server and test_app containers up...')
        start_containers_time = time.time()
        while not check_connect('dns_server', 53):
            time.sleep(3)
            if (time.time() - start_containers_time) > 60:
                raise Exception('Waiting for dns_server and test_app containers up timeout > 60 secs')
        # Update DNS server
        os.system('echo "nameserver {}" > /etc/resolv.conf'.format(socket.gethostbyname('dns_server')))
        logger.debug('Dns_server and test_app containers already up...')
    except Exception as e:
        logger.error(e)
        BS_INSTANCE.stop()

def check_connect(address, port):
    s = socket.socket()
    try:
      s.connect((address, port))
      s.shutdown(2)
      return True
    except:
      return False

def dynamic_import(test_case):
    module_object = importlib.import_module('testcases.case{}'.format(test_case))
    return module_object


def format_mongo_object(info_browser, case):
    return {
        "browser": info_browser['browser'],
        "version": info_browser['browser_version'],
        "platform": info_browser['os'],
        "os_version": info_browser['os_version'],
        "testCaseNum": int(case)
    }


def run_test_local(test_case):
    logger.debug('Testcase running: {}'.format(test_case))
    module_object = dynamic_import(test_case)
    test_case_class = getattr(module_object, 'Case{}'.format(test_case))
    return test_case_class().runLocal()


def run_local_main():
    logger.info('Environment: Local')
    local_tests = []
    if TESTCASES:
        logger.info('List test cases:{}'.format(TESTCASES))
        for case in TESTCASES:
            if case not in dataJson:
                logger.info('Skip test case: {}'.format(case))
                continue
            else:
                local_tests.append(case)
    logger.info('AMOUNT LOCAL TESTS:{}'.format(len(local_tests)))
    logger.info(local_tests)
    if len(local_tests) > 0 and not DRY_RUN:       
        start_infra()
        local_tests_ok = []
        local_tests_fail = []
        for local_test in local_tests:
            if run_test_local(local_test):
                local_tests_ok.append(local_test)
            else:
                local_tests_fail.append(local_test)
        logger.info('Local tests running OK: {}'.format(local_tests_ok))
        logger.info('Local tests running Fail: {}'.format(local_tests_fail))

    elif len(new_tests) > 0 and DRY_RUN:
        logger.info('DRY RUN')

def run_test_bs_list(bs_tests):
    # Dry run skips executions
    if len(bs_tests) > 0 and not DRY_RUN:
        start_infra()
        bs_tests_ok = []
        bs_tests_fail = []
        for bs_test in bs_tests:
            object_dict = format_mongo_object(bs_test['info_browser'], bs_test['test_case'])
            if run_test_bs(bs_test['info_browser'], bs_test['test_case']):
                bs_tests_ok.append(bs_test)
                # Remove from ignore list if sucess
                if DB.ignore_list.count_documents(object_dict): DB.ignore_list.remove(object_dict)
            else:
                bs_tests_fail.append(bs_test)
                # Add to ignore list for next run if not already
                if not DB.ignore_list.count_documents(object_dict): DB.ignore_list.insert(object_dict) 

        logger.info('BS tests running OK: {}'.format(bs_tests_ok))
        logger.info('BS tests running Fail: {}'.format(bs_tests_fail))
        logger.info('BS tests running Ignored: {}'.format(bs_tests_ignored))
        BS_INSTANCE.stop()
    elif len(bs_tests) > 0 and DRY_RUN:
        logger.info('DRY RUN')


def run_test_bs(info_browser, test_case):
    logger.debug('Testcase running: {}'.format(test_case))
    module_object = dynamic_import(test_case)
    test_case_class = getattr(module_object, 'Case{}'.format(test_case))
    return test_case_class().run(info_browser['os'], info_browser['os_version'], info_browser['browser'],
                          info_browser['browser_version'], constant.API_KEY, constant.USERBS, DB.db)


def translate_test_bs(object_dict, test_case):
    logger.debug('Testcase running: {}'.format(test_case))
    module_object = dynamic_import(test_case)
    test_case_class = getattr(module_object, 'Case{}'.format(test_case))
    return test_case_class.translate(object_dict)


def run_bs_main():
    global DB
    DB = Mongo()
    data_to_get = []
    bs_tests = []
    bs_tests_ignored = []
            
    if TESTCASES:
        logger.info('List test cases:{}'.format(TESTCASES))
        for case in TESTCASES:
            if case not in dataJson:
                logger.info('Skip test case: {}'.format(case))
                continue
            else:
                logger.info('Test case:{}'.format(case))
                for info_browser in browserSupport:
                    object_dict = format_mongo_object(info_browser, case)
                    result = DB.coll.count_documents(object_dict)
                    if result < 1:
                        # Ignore if in the list
                        if DB.ignore_list.count_documents(object_dict):
                            bs_tests_ignored.append({"info_browser": info_browser, "test_case": case})
                            continue
                        logger.debug('New test detected {}'.format(object_dict))
                        bs_tests.append({"info_browser": info_browser, "test_case": case})
                    elif FORCE_RERUN:
                        logger.debug('Rerun test {}'.format(object_dict))
                        bs_tests.append({"info_browser": info_browser, "test_case": case})
                   
    elif TESTOBJECTS:
        logger.info('List test objects:{}'.format(TESTOBJECTS))
        for obj in TESTOBJECTS:
            if obj['test_case'] not in dataJson or obj['info_browser'] not in browserSupport:
                logger.info('Skip test object: {}'.format(obj))
                continue
            else:
                object_dict = format_mongo_object(obj['info_browser'], obj['test_case'])
                result = DB.coll.count_documents(object_dict)
                if result < 1:
                    # Ignore if in the list
                    if DB.ignore_list.count_documents(object_dict):
                        bs_tests_ignored.append({"info_browser": info_browser, "test_case": case})
                        continue
                    logger.debug('New test detected {}'.format(object_dict))
                    bs_tests.append(obj)
                elif FORCE_RERUN:
                    logger.debug('Rerun test {}'.format(object_dict))
                    bs_tests.append(obj)

    else:
        logger.info('No tests for driver')
    logger.info('IGNORE_TESTS:{}'.format(bs_tests_ignored))
    logger.info('AMOUNT_BS_TESTS:{}'.format(len(bs_tests)))
    logger.info(bs_tests)
    run_test_bs_list(bs_tests)
    DB.close()


def run_main_wrapper(args):
    logger.info('Run Test Cases')
    
    global TESTENV, TESTCASES, TESTOBJECTS, DRY_RUN, FORCE_RERUN
    TESTENV = args.env if args.env else 'bs'
    if args.testcases:
        TESTCASES = args.testcases
    elif args.json:
        TESTCASES = None
        with open(os.path.abspath(os.path.dirname(__file__))+'/'+ args.json, "r") as read_it:
            TESTOBJECTS = json.load(read_it)
    else:
        TESTOBJECTS = None
    logger.setLevel(logging.DEBUG) if args.verbose else logger.setLevel(logging.INFO)
    DRY_RUN = args.dry_run if args.dry_run else False
    FORCE_RERUN = args.force if args.force else False
    get_config()
    run_bs_main() if TESTENV == 'bs' else run_local_main()


def autoupdate_main():
    global DB
    DB = Mongo()
    new_tests = []
    bs_tests_ignored = []
    for key, val in dataJson.items():
        for info_browser in browserSupport:
            object_dict = format_mongo_object(info_browser, key)
            result = DB.coll.count_documents(object_dict)
            if result < 1:
                # Ignore if in the list
                if DB.ignore_list.count_documents(object_dict):
                    bs_tests_ignored.append({"info_browser": info_browser, "test_case": case})
                    continue
                logger.debug('New test detected {}'.format(object_dict))
                new_tests.append({"info_browser": info_browser, "test_case": key})
    logger.info('IGNORE_TESTS:{}'.format(bs_tests_ignored))
    logger.info('AMOUNT_NEW_TESTS:{}'.format(len(new_tests)))
    logger.info(new_tests)
    run_test_bs_list(new_tests)
    DB.close()


def autoupdate_main_wrapper(args):
    logger.info('Auto Update')
    global DRY_RUN, TESTENV
    DRY_RUN = args.dry_run if args.dry_run else False
    FORCE_RERUN = args.force if args.force else False
    # always use browserstack
    TESTENV = 'bs'
    logger.setLevel(logging.DEBUG) if args.verbose else logger.setLevel(logging.INFO)
    get_config()
    autoupdate_main()


def init_docker(args):
    logger.info('Start Docker Environment')


def parser_init():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='CIT toolset',
                                       description='CIT toolset: Run, Autoupdate, Check data test cases',  help='backend toolset help')
    parser_run = subparsers.add_parser('run')
    parser_run.add_argument('-e', '--env', choices=['bs', 'local'], default='bs', help='Choose test environment BrowserStack or Local')
    parser_run.add_argument('-t', '--testcases', type=lambda s: [str(item) for item in s.split(',')], help='run test cases, separate by comma')
    parser_run.add_argument('-j', '--json', type=str, help='Json file of test objects ex: sample_tests.json')
    parser_run.add_argument('-d', '--dry_run', action='store_true', help="Dry run")
    parser_run.add_argument('-v', '--verbose', action='store_true', help="Verbose")
    parser_run.add_argument('-f', '--force', action='store_true', help="Force re-run")
    parser_run.set_defaults(func=run_main_wrapper)
    parser_autoupdate = subparsers.add_parser('autoupdate')
    parser_autoupdate.add_argument('-d', '--dry_run', action='store_true', help="Dry run")
    parser_autoupdate.add_argument('-v', '--verbose', action='store_true', help="Verbose")
    parser_autoupdate.add_argument('-f', '--force', action='store_true', help="Force re-run")
    parser_autoupdate.set_defaults(func=autoupdate_main_wrapper)
    parser_docker = subparsers.add_parser('docker', help='For docker-compose environment')
    parser_docker.set_defaults(func=init_docker)
    args = parser.parse_args()
    args.func(args)


def main():
    parser_init()


if __name__ == '__main__':
    main()