#!/usr/bin/python
# encoding:utf-8

import re
import sys
import urllib
import urllib2
import cookielib

def check(response):
    """
    docstring for check
    """
    pattern = re.compile(r'<div class="idh">(已连续签到\d+天)</div>')
    result = pattern.search(response)
    if result: return result.group(1)
    return False
    pass

def main():
    """
    docstring for main
    """

    # Get email and password
    if len(sys.argv) != 3:
        print '[Error] Please input email & password as sys.argv!'
        return
    email = sys.argv[1]
    password = sys.argv[2]

    # Init
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    urllib2.install_opener(opener)

    # Login
    login_url = 'http://www.xiami.com/web/login'
    login_data = urllib.urlencode({'email':email, 'password':password, 'LoginButton':'登陆',})
    login_headers = {'Referer':'http://www.xiami.com/web/login', 'User-Agent':'Opera/9.60',}
    login_request = urllib2.Request(login_url, login_data, login_headers)
    login_response = urllib2.urlopen(login_request).read()

    # Checkin
    checkin_pattern = re.compile(r'<a class="check_in" href="(.*?)">')
    checkin_result = checkin_pattern.search(login_response)
    if not checkin_result:
        # Checkin Already | Login Failed
        result = check(login_response)
        if result :
            print '[Succeed] Checkin Already!', email, result
        else:
            print '[Error] Login Failed!'
        return
    checkin_url = 'http://www.xiami.com' + checkin_result.group(1)
    checkin_headers = {'Referer':'http://www.xiami.com/web', 'User-Agent':'Opera/9.60',}
    checkin_request = urllib2.Request(checkin_url, None, checkin_headers)
    checkin_response = urllib2.urlopen(checkin_request).read()

    # Result
    result = check(checkin_response)
    if result:
        print '[Succeed] Checkin Succeed!', email, result 
    else:
        print '[Error] Checkin Failed!'
    pass

if __name__=='__main__':
    main()
