# ------------------------------------------------------------------------------------------------
#  Copyright (c) mgm security partners GmbH. All rights reserved.
#  Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
#-------------------------------------------------------------------------------------------------

import sys
import os
import constant
import datetime
import json
import importlib

#function to import test case class by .py files
def dynamic_import(abs_module_path):
    module_object = importlib.import_module(abs_module_path)
    return module_object

#read map.json file to get the .py filename mapped with each testcase
with open('/testcases/map.json', "r") as read_it: 
    dataJson = json.load(read_it)

if len(sys.argv) > 1:
    cases = sys.argv[1].split(',')
    for case in cases:
        if case  not in dataJson:
            print ("Error in running Case \033[31m" + case + "\033[0m, test case not found! ")
            continue
        else:
          absPath = dataJson[case]['modulename']
          tmp = "case" + case
          exec("%s = dynamic_import(absPath)" % (tmp))
          try:
            exec("%s.Case%s().runLocal()" % (tmp,case))
          except Exception as e:
            print ("Error in running Case \033[31m" + case + "\033[0m, error in running test case! " + e)
            continue
print ("Finished running locally!")
          
