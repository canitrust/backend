# ------------------------------------------------------------------------------------------------
#  Copyright (c) mgm security partners GmbH. All rights reserved.
#  Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
#-------------------------------------------------------------------------------------------------

import sys
import os
import constant
import pymongo
import json
import importlib
from datetime import datetime
from bson import json_util
from helpers import get_browser_support

def dynamic_import(abs_module_path):
    module_object = importlib.import_module(abs_module_path)
    return module_object

if get_browser_support(constant.USERBS, constant.API_KEY):
    print("Complete checking the latest browser versions support")
else:
    print("Incomplete checking the latest browser versions support")
with open('/testcases/map.json', "r") as read_it: 
    dataJson = json.load(read_it)
with open('/testcases/browsersupport.json', "r") as read_it: 
    browserSupport = json.load(read_it)

if len(sys.argv) > 1:
    data_to_get = []
    cases = sys.argv[1].split(',')
    for case in cases:
        if case  not in dataJson:
            continue
        else:
            print('Testcase to be run:', case, '\n')
            absPath = dataJson[case]['modulename']
            tmp = "case" + case
            exec("%s = dynamic_import(absPath)" % (tmp))
            client1 = pymongo.MongoClient(constant.DB_URL)
            db1 = client1[constant.DB_DATABASE]
            myCollection = db1[constant.DB_COLL]
            for infoBrowser in browserSupport:
                objectDic= {
                    "browser":infoBrowser['browser'],
                    "version": infoBrowser['browser_version'],
                    "platform": infoBrowser['os'],
                    "os_version":infoBrowser['os_version'],
                    "testCaseNum": int(case)
                }
                result = myCollection.count(objectDic)
                get_data = myCollection.find(objectDic)
                if result < 1:
                    try:
                        exec("%s.Case%s().run(infoBrowser['os'],infoBrowser['os_version'],infoBrowser['browser'],infoBrowser['browser_version'],constant.API_KEY, constant.USERBS,db1)" % (tmp,case) )
                    except:
                        continue
                else:
                    print('Test results were found for the browser, translating results and save to file. This file will be used to import data to the frontend database.', objectDic)
                    print('get_data', result, get_data)
                    for i in get_data:
                        print('To be executed:', "e = %s.Case%s.translate(i)" %(tmp, case))
                        print('Data to be translated: ', i)
                        exec("e = %s.Case%s.translate(i)" %(tmp, case))
                        print('Translated data (frontend structure)', e)
                        if e is not None and e != 1:
                            data_to_get.append(e)
            client1.close()

    # Below code "translates" existing test results (found in backend DB) to frontend DB format and stores the data in a file.
    # Todo: separate this part to another file
    if not(os.path.exists("/testcases/jsondata")):
        os.mkdir('/testcases/jsondata')
    with open("/testcases/jsondata/data" + datetime.now().strftime("%Y-%m-%d%H:%M") +  ".json",'w') as f:
        ignored_keys = ["date_lasttest"]
        filtered = {tuple((k, d[k]) for k in sorted(d) if k not in ignored_keys): d for d in data_to_get}
        dst_lst = list(filtered.values())
        json.dump(dst_lst,f,default=json_util.default)
        f.close()
else:
    for key in dataJson:
        absPath = dataJson[key]['modulename']
        tmp= "case"+ key
        exec("%s = dynamic_import(absPath)" % (tmp))
        for infoBrowser in browserSupport:
            objectDic= {
                "browser": infoBrowser['browser'],
                "version": infoBrowser['browser_version'],
                "platform": infoBrowser['os'],
                "testCaseNum": int(case)
            }
            client1 = pymongo.MongoClient(constant.DB_URL)
            db1 = client1[constant.DB_DATABASE]
            myCollection= db1[constant.DB_COLL]
            result= myCollection.count(objectDic)
            if result < 1:
                try:
                    exec("%s.Case%s().run(infoBrowser['os'],infoBrowser['os_version'],infoBrowser['browser'],infoBrowser['browser_version'],constant.API_KEY, constant.USERBS,db1)" % (tmp,case) )
                except:
                    continue
            client1.close()
sys.exit()
