# ------------------------------------------------------------------------------------------------
#  Copyright (c) mgm security partners GmbH. All rights reserved.
#  Licensed under the AGPLv3 License. See LICENSE.md in the project root for license information.
#-------------------------------------------------------------------------------------------------

__author__ = 'mgm-sp.com'

import requests
import sys, json
import os


def get_browser_support(bs_user, bs_key):
    print('======== Getting Browser Support from Browser Stack ========')
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
        print('Total browsers support by BrowserStack: ', len(list_bs_browsers))
        print('Total browsers support by CanITrust: ', len(list_cit_browsers))
        with open(os.path.abspath(os.path.dirname(__file__)) + '/browsersupport.json', 'w') as json_file:  
            json.dump(list_cit_browsers, json_file, indent=4, sort_keys=True)
        return True

    return False
  
if __name__ == '__main__':
  #for testing directly
  get_browser_support(os.environ['BS_USER'], os.environ['BS_KEY'])
