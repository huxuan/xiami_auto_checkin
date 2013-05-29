#!/usr/bin/python
# encoding:utf-8
# +-----------------------------------------------------------------------------
# | File: xiami_auto_checkin.py
# | Author: huxuan
# | E-mail: i(at)huxuan.org
# | Created: 2011-12-11
# | Last modified: 2012-02-06
# | Description:
# |     Description for xiami_auto_checkin.py
# |
# | Copyrgiht (c) 2012 by huxuan. All rights reserved.
# | License GPLv3
# +-----------------------------------------------------------------------------

import re
import os
import sys
import urllib
import urllib2
import datetime
import cookielib

def check(response):
    """Check whether checkin is successful

    Args:
        response: the urlopen result of checkin

    Returns:
        If succeed, return a string like '已经连续签到**天'
            ** is the amount of continous checkin days
        If not, return False
    """
    pattern = re.compile(r'<div class="idh">(已连续签到\d+天)</div>')
    result = pattern.search(response)
    if result: return result.group(1)
    return False

def main():
    """Main process of auto checkin
    """
    # Get log file
    LOG_DIR = os.path.join(os.path.expanduser("~"), '.log')
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    LOG_PATH = os.path.join(LOG_DIR, 'xiami_auto_checkin.log')
    f = LOG_FILE = file(LOG_PATH, 'a')

    # Get email and password
    if len(sys.argv) != 3:
        print >>f, '[Error] Please input email & password as sys.argv!'
        print >>f, datetime.datetime.now()
        return
    email = sys.argv[1]
    password = sys.argv[2]

    # Init
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    urllib2.install_opener(opener)

    # Login
    login_url = 'http://www.xiami.com/member/login'
    login_data = urllib.urlencode({
        'done': '/',
        'email':email,
        'password':password,
        'submit':'登 录',
    })
    login_headers = {
        'Referer':'http://www.xiami.com/web/login',
        'User-Agent':'Opera/9.60',
    }
    login_request = urllib2.Request(login_url, login_data, login_headers)
    login_response = urllib2.urlopen(login_request).read()

    # Checkin
    checkin_pattern = re.compile(r'<a.*>(.*?)天\s*?<span>已连续签到</span>')
    checkin_result = checkin_pattern.search(login_response)
    if checkin_result:
        # Checkin Already
        print >>f, datetime.datetime.now(), email, checkin_result, '[Already]'
        return
    checkin_url = 'http://www.xiami.com/task/signin'
    checkin_headers = {'Referer':'http://www.xiami.com/', 'User-Agent':'Opera/9.60',}
    checkin_request = urllib2.Request(checkin_url, None, checkin_headers)
    checkin_response = urllib2.urlopen(checkin_request).read()

    # Result
    result = checkin_pattern.search(checkin_response)
    print >>f, datetime.datetime.now(), email, checkin_response

if __name__=='__main__':
    main()
