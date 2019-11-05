#  ------------------------------------------------------------------------------------------------
#   Copyright (c) mgm security partners GmbH. All rights reserved.
#   Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
#  #-------------------------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------------------------

import os
from dotenv import load_dotenv

#load .env
load_dotenv()
#default_value 
default_value = "TEST"

#Constant
DB_URL = os.getenv('DB_URL', default_value)
DB_USERNAME = os.getenv('DB_USERNAME', default_value)
DB_PASSWORD = os.getenv('DB_PASSWORD', default_value)
DB_DATABASE = os.getenv('DB_DATABASE', default_value)
DB_COLL = os.getenv('DB_COLL',default_value)
DB_FAILED_TESTS = os.getenv('DB_FAILED_TESTS', 'failed_tests')
TEST_MAX_RETRY = os.getenv('TEST_MAX_RETRY', 3)
#git account
GIT_USER_NAME = os.getenv('GIT_USER_NAME', default_value)
GIT_PASSWORD = os.getenv('GIT_PASSWORD', default_value)
API_KEY = os.getenv("API_KEY",default_value)
USERBS = os.getenv("USER_BS",default_value)
