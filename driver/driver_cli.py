#  ------------------------------------------------------------------------------------------------
#   Copyright (c) mgm security partners GmbH. All rights reserved.
#   Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
#  #-------------------------------------------------------------------------------------------------
#
#
#

import os
import argparse
import logging
import json
from config import settings
from helper import Logger, get_config
from driver import run_bs_main, run_local_main, runlocal_main, runbs_main, autoupdate_main
logger = Logger(__name__).logger

def run_main_wrapper(args):
    settings.TESTENV = args.env if args.env else 'bs'
    settings.SAVE_DB = True
    if args.testcases: settings.TESTCASES = args.testcases
    elif args.json:
        settings.TESTCASES = None
        with open(os.path.abspath(os.path.dirname(__file__))+'/'+ args.json, "r") as read_it:
            settings.TESTOBJECTS = json.load(read_it)
    else:
        settings.TESTCASES, settings.TESTOBJECTS = None, None
    logger.setLevel(logging.DEBUG) if args.verbose else logger.setLevel(logging.INFO)
    settings.DRY_RUN = args.dry_run if args.dry_run else False
    settings.FORCE_RERUN = args.force if args.force else False
    get_config()
    run_bs_main() if settings.TESTENV == 'bs' else run_local_main()

def runlocal_main_wrapper(args):
    settings.TESTENV = 'local'
    settings.DRY_RUN = args.dry_run if args.dry_run else False
    settings.CATCH_FAIL = args.catch_fail if args.catch_fail else False
    logger.setLevel(logging.DEBUG)
    get_config()
    if args.testcases: settings.TESTCASES = args.testcases
    elif args.all:
        settings.TESTCASES = []
        for key, value in settings.dataJson.items():
            settings.TESTCASES.append(key)        
    elif args.all_live:
        settings.TESTCASES = []
        for key, value in settings.dataJson.items():
            if settings.dataJson[key]['isLive']:
                settings.TESTCASES.append(key)
    runlocal_main()

def runbs_main_wrapper(args):
    settings.IS_RUNBS = True
    settings.TESTENV = 'bs'
    logger.setLevel(logging.INFO) if args.save_db else logger.setLevel(logging.INFO)
    if args.testcases: settings.TESTCASES = args.testcases
    elif args.json:
        settings.TESTCASES = None
        with open(os.path.abspath(os.path.dirname(__file__))+'/'+ args.json, "r") as read_it:
            settings.TESTOBJECTS = json.load(read_it)
    else:
        settings.TESTCASES, settings.TESTOBJECTS = None, None
    settings.DRY_RUN = args.dry_run if args.dry_run else False
    settings.SAVE_DB = args.save_db if args.save_db else False
    logger.setLevel(logging.INFO) if settings.SAVE_DB else logger.setLevel(logging.DEBUG)
    get_config()
    runbs_main()

def autoupdate_main_wrapper(args):
    logger.info('Auto Update')
    settings.DRY_RUN = args.dry_run if args.dry_run else False
    settings.FORCE_RERUN = args.force if args.force else False
    # always use browserstack
    settings.TESTENV = 'bs'
    settings.SAVE_DB = True
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
    parser_run.add_argument('-e', '--env', choices=['bs', 'local'], default='bs', help='Choose test environment BrowserStack (default) or Local')
    parser_run.add_argument('-t', '--testcases', type=lambda s: [str(item) for item in s.split(',')], help='run test cases, separate by comma')
    parser_run.add_argument('-j', '--json', type=str, help='Json file of test objects ex: sample_tests.json')
    parser_run.add_argument('-d', '--dry_run', action='store_true', help="Dry run")
    parser_run.add_argument('-v', '--verbose', action='store_true', help="Verbose")
    parser_run.add_argument('-f', '--force', action='store_true', help="Force re-run")
    parser_run.set_defaults(func=run_main_wrapper)
    parser_runlocal = subparsers.add_parser('runlocal')
    parser_runlocal.add_argument('-t', '--testcases', type=lambda s: [str(item) for item in s.split(',')], help='run test cases, separate by comma')
    parser_runlocal.add_argument('--all', action='store_true', help="Run all test cases")
    parser_runlocal.add_argument('--all_live', action='store_true', help="Run all (live) test cases")
    parser_runlocal.add_argument('--catch_fail', action='store_true', help="Exit on failure")
    parser_runlocal.add_argument('-d', '--dry_run', action='store_true', help="Dry run")
    parser_runlocal.set_defaults(func=runlocal_main_wrapper)
    parser_runbs = subparsers.add_parser('runbs')
    parser_runbs.add_argument('-t', '--testcases', type=lambda s: [str(item) for item in s.split(',')], help='run test cases, separate by comma')
    parser_runbs.add_argument('-j', '--json', type=str, help='Json file of test objects ex: sample_tests.json')
    parser_runbs.add_argument('-d', '--dry_run', action='store_true', help="Dry run")
    parser_runbs.add_argument('-s', '--save_db', action='store_true', help="Save to database which is specified in .env")
    parser_runbs.set_defaults(func=runbs_main_wrapper)
    parser_autoupdate = subparsers.add_parser('autoupdate', help='Only support browserstack testing')
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