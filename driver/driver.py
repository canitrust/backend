#  ------------------------------------------------------------------------------------------------
#   Copyright (c) mgm security partners GmbH. All rights reserved.
#   Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
#  #-------------------------------------------------------------------------------------------------
#
#
#

import importlib
from helper import BS, Logger, Mongo, pretty_output, start_infra
from config import constant, settings
from functools import wraps

logger = Logger(__name__).logger

def dynamic_import(test_case):
    module_object = importlib.import_module('testcases.case{}'.format(test_case))
    return module_object


def format_mongo_object(info_browser, case):
    return {
        "browser": info_browser['browser'],
        "version": info_browser['browser_version'],
        "platform": info_browser['os'],
        "os_version": info_browser['os_version'],
        "testCaseNum": int(case),
        "deprecated": False
    }


def count_docs_success(info_browser, case):
    object_dict = format_mongo_object(info_browser, case)
    result = settings.DB.coll.count_documents(object_dict)
    return result


def count_docs_failed(info_browser, case):
    object_dict = format_mongo_object(info_browser, case)
    object_dict.update({'retry_count': {'$gte': constant.TEST_MAX_RETRY }})
    result = settings.DB.failed_tests.count_documents(object_dict)
    return result

def get_test_cases():
    tests = []
    logger.info('test-cases from input:{}'.format(settings.TESTCASES))
    logger.info('test-object from input:{}'.format(settings.TESTOBJECTS))
    if settings.TESTCASES and settings.TESTENV == 'local':
        tests = [ case for case in settings.TESTCASES if case in settings.dataJson ]
    # "runbs" command
    elif settings.TESTCASES and settings.TESTENV == 'bs' and settings.IS_RUNBS and settings.SAVE_DB:
        tests = [ {"info_browser": info_browser, "test_case": case} for case in settings.TESTCASES if case in settings.dataJson and settings.dataJson[case]['isLive'] 
            for info_browser in settings.browserSupport]
    # "runbs" command
    elif settings.TESTCASES and settings.TESTENV == 'bs' and settings.IS_RUNBS:
        tests = [ {"info_browser": info_browser, "test_case": case} for case in settings.TESTCASES if case in settings.dataJson 
            for info_browser in settings.browserSupport]
    # "run" command with settings.FORCE_RERUN option
    elif settings.TESTCASES and settings.TESTENV == 'bs' and settings.FORCE_RERUN:
        tests = [ {"info_browser": info_browser, "test_case": case} for case in settings.TESTCASES if case in settings.dataJson and settings.dataJson[case]['isLive'] 
            for info_browser in settings.browserSupport ] 
    # "run" command 
    elif settings.TESTCASES and settings.TESTENV == 'bs':
        tests = [ {"info_browser": info_browser, "test_case": case} for case in settings.TESTCASES if case in settings.dataJson and settings.dataJson[case]['isLive'] 
            for info_browser in settings.browserSupport if count_docs_success(info_browser, case) < 1 and count_docs_failed(info_browser, case) ]         
    # "runbs" command
    elif settings.TESTOBJECTS and settings.IS_RUNBS and settings.SAVE_DB:
        tests = [ obj for obj in settings.TESTOBJECTS if obj['test_case'] in settings.dataJson and settings.dataJson[obj['test_case']]['isLive'] ]
    # "runbs" command
    elif settings.TESTOBJECTS and settings.IS_RUNBS:
        tests = [ obj for obj in settings.TESTOBJECTS if obj['test_case'] in settings.dataJson ]
    # "run" command with settings.FORCE_RERUN option
    elif settings.TESTOBJECTS and settings.FORCE_RERUN:
        tests = [ obj for obj in settings.TESTOBJECTS if obj['test_case'] in settings.dataJson and settings.dataJson[obj['test_case']]['isLive'] ]
     # "run" command 
    elif settings.TESTOBJECTS:
        tests = [ obj for obj in settings.TESTOBJECTS if obj['test_case'] in settings.dataJson and settings.dataJson[obj['test_case']]['isLive'] 
            and count_docs_success(obj['info_browser'], obj['test_case']) < 1 and count_docs_failed(obj['info_browser'], obj['test_case'])]
    logger.info('test-cases processing:{}'.format(tests))
    return tests

def check_failure_data(f):
    @wraps(f)
    def checked(bs_tests):
        if bs_tests and settings.FORCE_RERUN and not settings.DRY_RUN:
            for bs_test in bs_tests:
                object_dict = format_mongo_object(bs_test['info_browser'], bs_test['test_case'])
                # Clear from the list of failed tests 
                if settings.DB.failed_tests.count_documents(object_dict): settings.DB.failed_tests.remove(object_dict)
                # search for current result not deprecated
                current_results = settings.DB.coll.find(object_dict)
                for current_result in current_results:
                    settings.DB.coll.find_one_and_update(current_result, {'$set': {'deprecated': True }})
                    logger.debug("DEPRECATED: {}".format(current_result))

        return f(bs_tests)    
    return checked


def exec_local_test(test_case):
    logger.debug('test-case running: {}'.format(test_case))
    module_object = dynamic_import(test_case)
    test_case_class = getattr(module_object, 'Case{}'.format(test_case))
    return test_case_class().runLocal()

def exec_bs_test(info_browser, test_case):
    logger.info('test-case running: {}'.format(test_case))
    module_object = dynamic_import(test_case)
    test_case_class = getattr(module_object, 'Case{}'.format(test_case))
    #if test_case not live never save to database
    if settings.SAVE_DB and settings.dataJson[test_case]['isLive']:
        return test_case_class().run(info_browser['os'], info_browser['os_version'], info_browser['browser'],
                            info_browser['browser_version'], constant.API_KEY, constant.USERBS, settings.DB.db)
    return test_case_class().runnotsave(info_browser['os'], info_browser['os_version'], info_browser['browser'],
                          info_browser['browser_version'], constant.API_KEY, constant.USERBS) 


@check_failure_data
def exec_bs_test_list(bs_tests):
    # Dry run skips executions
    if bs_tests and not settings.DRY_RUN:
        start_infra()
        bs_tests_ok = []
        bs_tests_fail = []
        results = []
        for bs_test in bs_tests:
            object_dict = format_mongo_object(bs_test['info_browser'], bs_test['test_case'])
            result = exec_bs_test(bs_test['info_browser'], bs_test['test_case']) 
            if result["result"] != "Failed" and result["data"] != "Failed"  :
                bs_tests_ok.append(bs_test)
                # Remove from the list of failed tests if sucess
                if settings.DB.failed_tests.count_documents(object_dict): settings.DB.failed_tests.remove(object_dict)
            else:
                bs_tests_fail.append(bs_test)
                # Add to the list of failed tests for next run if not exist
                if not settings.DB.failed_tests.count_documents(object_dict): 
                    object_dict.update({'retry_count': 0})
                    settings.DB.failed_tests.insert(object_dict) 
                # Increment retry_count if already 
                else:
                    settings.DB.failed_tests.find_one_and_update(object_dict, {'$inc': {'retry_count': 1}})
            results.append(result)
        logger.info('BS tests running OK: {}'.format(bs_tests_ok))
        logger.info('BS tests running Fail: {}'.format(bs_tests_fail))
        logger.info('(*) TEST SUMMARY \n{}'.format(pretty_output(results))) 
        settings.BS_INSTANCE.stop()
    elif bs_tests and settings.DRY_RUN:
        logger.info('DRY RUN')
    settings.DB.close()


def run_local_main():
    logger.info('testing environment: local')
    local_tests = get_test_cases()
    logger.info('AMOUNT_LOCAL_TESTS:{}'.format(len(local_tests)))
    logger.info('LOCAL_TESTS:{}'.format(local_tests))
    if len(local_tests) > 0 and not settings.DRY_RUN:       
        start_infra()
        local_tests_ok = []
        local_tests_fail = []
        results = []
        for local_test in local_tests:
            result = exec_local_test(local_test)
            if result["result"] != "Failed" and result["data"] != "Failed"  :
                local_tests_ok.append(local_test)
            else:
                local_tests_fail.append(local_test)
                # Exit on failure
                if settings.CATCH_FAIL:
                    logger.error("Driver stops - Fix testcase {} and try again".format(local_test))
                    exit(1)
            results.append(result)
        logger.info('Local tests running OK: {}'.format(local_tests_ok))
        logger.info('Local tests running Fail: {}'.format(local_tests_fail))
        logger.info('(*) TEST SUMMARY \n{}'.format(pretty_output(results))) 
    elif len(local_tests) > 0 and settings.DRY_RUN:
        logger.info('DRY RUN')


def run_bs_main():
    settings.DB = Mongo()
    bs_tests = get_test_cases()
    logger.info('AMOUNT_BS_TESTS:{}'.format(len(bs_tests)))
    exec_bs_test_list(bs_tests)
    settings.DB.close()


def runlocal_main():
    # same with run command
    run_local_main()


def runbs_main():
    settings.DB = Mongo()
    bs_tests = get_test_cases()
    logger.info('BS_TESTS:{}'.format(bs_tests))
    logger.info('AMOUNT_BS_TESTS:{}'.format(len(bs_tests)))
    exec_bs_test_list(bs_tests)


def autoupdate_main():
    settings.DB = Mongo()
    bs_tests = []
    bs_tests_ignored = []
    for key, val in settings.dataJson.items():
        for info_browser in settings.browserSupport:
            object_dict = format_mongo_object(info_browser, key)
            result = settings.DB.coll.count_documents(object_dict)
            object_dict.update({'retry_count': {'$lt': constant.TEST_MAX_RETRY }})
            # Add if lesser than max retry
            if settings.DB.failed_tests.count_documents(object_dict):
                bs_tests.append({"info_browser": info_browser, "test_case": key})
                continue
            if result < 1 and val['isLive']:
                # Ignore if reach max retry
                object_dict.update({'retry_count': {'$gte': constant.TEST_MAX_RETRY }})
                if settings.DB.failed_tests.count_documents(object_dict) and not settings.FORCE_RERUN:
                    bs_tests_ignored.append({"info_browser": info_browser, "test_case": key})
                    continue
                # clean the filter
                object_dict.pop('retry_count', None)
                logger.debug('New test detected {}'.format(object_dict))
                bs_tests.append({"info_browser": info_browser, "test_case": key})
    logger.info('IGNORE_TESTS:{}'.format(bs_tests_ignored))
    logger.info('BS_TESTS:{}'.format(bs_tests))
    logger.info('AMOUNT_IGNORE_TESTS:{}'.format(len(bs_tests_ignored)))
    logger.info('AMOUNT_BS_TESTS:{}'.format(len(bs_tests)))
    exec_bs_test_list(bs_tests)
    settings.DB.close()