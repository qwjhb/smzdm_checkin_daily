# coding: UTF-8
import http.cookiejar
import urllib.request
import urllib.parse
import re
import time
import configparser
class Smzdm:
    def __init__(self):
        self.cookies = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookies))
        self.headers = {
            'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36',
            'Referer' : 'http://www.smzdm.com/',
            'Origin' : 'http://www.smzdm.com/'
        }

    def login(self,account):
        url = "https://zhiyou.smzdm.com/user/login/ajax_check"
        data = urllib.parse.urlencode({
            'username' : account['username'],
            'password' : account['password'],
            'rememberme' : 'on',
            'redirect_url' : 'http://www.smzdm.com'
        }).encode()
        request = urllib.request.Request(url, headers=self.headers, data=data)
        content = self.opener.open(request)
        return content

    def logout(self):
        url = "http://zhiyou.smzdm.com/user/logout"
        request = urllib.request.Request(url, headers=self.headers,)
        self.opener.open(request)

    def checkin(self):
        url = "http://zhiyou.smzdm.com/user/checkin/jsonp_checkin"
        request = urllib.request.Request(url, headers=self.headers)
        self.opener.open(request)

    def is_checkin(self):
        url = "http://zhiyou.smzdm.com/user/info/jsonp_get_current?"
        request = urllib.request.Request(url, headers = self.headers)
        response = self.opener.open(request)
        content = response.read().decode('utf-8')
        pattern = re.compile('\"has_checkin\"\:(.*?),')
        item = re.search(pattern, content)
        if item and item.group(1).strip() == 'true':
            return 'SUCCEED'
        else:
            return 'FAILED'



    def start_checkin(self):
        parser = configparser.RawConfigParser()
        parser.read("account.ini")
        log = open('log.txt','a', newline='')
        for user in parser.sections():
            account = {}
            account['username'] = parser.get(user, 'username')
            account['password'] = parser.get(user, 'password')
            self.login(account)
            self.checkin()
            if self.is_checkin()=='SUCCEED':
                log.write(time.strftime('%Y-%m-%d',time.localtime(time.time()))+','+ account['username'] +',SUCCEED\n')
            else:
                log.write(time.strftime('%Y-%m-%d',time.localtime(time.time()))+','+ account['username'] +',FAILED\n')
            self.logout()
        log.close()

smzdm = Smzdm()
smzdm.start_checkin()

