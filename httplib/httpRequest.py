#!/usr/bin/env python
# -*- coding: UTF-8 -*

###############################################################################
# Copyright (C), 2017 SongDehua
#
# Filename:     httpRequest.py
# Version:      1.0.0
# Description:  Module for pySuit frame to execute the http method(get/post/head...)
# Author:       songdehua
# History:
#   1. 2017-04-25  songdehua, first create
###############################################################################

"""Module for pySuit frame
    This module exports a class to execute the http method and return the http result
    class http_request: exports the class tho the
    class httpResult  : exports the http response result
"""

import json
import unittest
import sys
import logging
sys.path.append('..')
try:
    import cookielib
except ImportError:
    import http.cookiejar as cookielib
try:
    import urllib2
except ImportError:
    import urllib.request as urllib2
# third part of lib
import requests

try:
    from lib.PyLogger import pyLogger
except Exception:
    import logging

logger = logging.getLogger("httpRequest")


SET_TIME_OUT = 60


class http_request(object):

    def __init__(self, loginUrl=None, username=None, password=None, _logger=None, **kwargs):
        self.loginUrl = loginUrl
        self.username = username
        self.password = password
        self.coookiejar = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar=self.coookiejar))
        urllib2.install_opener(self.opener)
        self.cookies = None
        if _logger is not None:
            logger = _logger

    def requestWithPost(self, url, headers={}, entity="", isLogin=False):
        """
        :param url:
        :param headers:
        :param entity: {} or a str obj
        :param isLogin:
        :return: a httpResult object
        """
        # r = requests.post(url=url, data=entity)
        cookies = None
        if self.cookies:
            cookies = self.cookies
        if isLogin:
            cookies = self.doLogin(username=self.username, password=self.password, url=self.loginUrl).getCookieJar()
        # respone = requests.get(url=url, data=entity, headers=headers, timeout=SET_TIME_OUT, cookies=self.cookies)
        if type(entity) is str:
            # entity = entity.encode("UTF-8")
            entity = entity.encode("utf-8")
        result = httpResult()
        # if isLogin:
        #     self.doLogin(username=self.username, password=self.password, url=self.loginUrl)
        # # logger.debug("Exec http post method...header %s, entity %s" %(unicode(headers), entity))
        # request = urllib2.Request(url, headers=headers, data=entity)
        # if "Connection" not in headers.keys():
        #     headers["Connection"] = "keep-alive"
        #
        # for key in headers.keys():
        #     request.add_header(key, headers[key])
        #
        # request.get_method = lambda: 'POST'
        # if self.check_json_format(entity):
        #     pass
        logger.debug("requestPost...url: %s , entity: %s, headers %s" % (url, entity, headers))
        respone = requests.post(url=url, data=entity, headers=headers, timeout=SET_TIME_OUT, cookies=cookies)
        result.setResponeMsg(respone.text)
        result.setCookieJar(respone.cookies)
        result.setResponeCode(respone.status_code)
        logger.debug("requestPost response...url: %s , entity: %s" % (url, result.getResponeMsg()))
        return result
        # result.setResponeCode(responeCode=response.code)
        # print(type(response.headers))
        # result.setCookieJar(CookieJar=self.coookiejar)
        # result.setResponeHeader(responeHeader=response.headers._headers)
        # msg = response.read()
        # print(msg)
        # result.setResponeMsg(msg)
        # print(request)
        # return requests

    def requestWithGet(self, url, headers={}, entity=None, isLogin=False):
        """
        :param url:
        :param headers:
        :param entity:
        :param isLogin:
        :return: httpResult object
        """
        result = httpResult()
        cookies = None
        # print(self.cookies)
        if self.cookies:
            cookies = self.cookies
        if isLogin:
            cookies = self.doLogin(username=self.username, password=self.password, url=self.loginUrl).getCookieJar()
        logger.debug("requestGet...url: %s , headers %s" % (url, headers))
        respone = requests.get(url=url, data=entity, headers=headers, timeout=SET_TIME_OUT, cookies=cookies)

        result.setResponeMsg(respone.text)
        result.setCookieJar(respone.cookies)
        result.setResponeCode(respone.status_code)
        logger.debug("requestGet response...url: %s , body %s" % (url, result.getResponeMsg()))
        return result
        # logger.debug("Exec http post method...header %s, entity %s" %(unicode(headers), entity))
        # request = urllib2.Request(url, headers=headers, data=entity)
        # if "Connection" not in headers.keys():
        #     headers["Connection"] = "keep-alive"
        #
        # for key in headers.keys():
        #     request.add_header(key, headers[key])
        # request.method = 'GET'
        # response = urllib2.urlopen(request)
        # result.setResponeCode(responeCode=response.code)
        # result.setCookieJar(CookieJar=self.coookiejar)
        # result.setResponeHeader(responeHeader=response.headers._headers)
        # result.setResponeType(responseType=response.headers._default_type)
        # msg = response.read()
        # msg =  str(msg, encoding = "utf-8")
        # result.setResponeMsg(responeMsg=msg)
        # result.isRetJson = self.check_json_format(msg)
        # return result

    def requestWithDelete(self, url, headers={}, entity="", isLogin=False):
        """

        :param url:
        :param headers:
        :param entity:
        :param isLogin:
        :return:
        """
        result = httpResult()
        cookies = None
        if self.cookies:
            cookies = self.cookies
        if isLogin:
            cookies = self.doLogin(username=self.username, password=self.password, url=self.loginUrl).getCookieJar()
        logger.debug("requestDelete...url: %s , entity: %s, headers %s" % (url, entity, headers))
        respone = requests.delete(url=url, data=entity, headers=headers, timeout=SET_TIME_OUT, cookies=cookies)

        result.setResponeMsg(respone.text)
        result.setCookieJar(respone.cookies)
        result.setResponeCode(respone.status_code)
        return result

    def requestWithPut(self, url, headers={}, entity="", isLogin=False):
        """

        :param url:
        :param headers:
        :param entity:
        :param isLogin:
        :return:
        """
        result = httpResult()
        cookies = None
        if self.cookies:
            cookies = self.cookies
        if isLogin:
            cookies = self.doLogin(username=self.username, password=self.password, url=self.loginUrl).getCookieJar()
        logger.debug("requestPut...url: %s , entity: %s, headers %s" % (url, entity, headers))
        respone = requests.put(url=url, data=entity, headers=headers, timeout=SET_TIME_OUT, cookies=cookies)

        result.setResponeMsg(respone.text)
        result.setCookieJar(respone.cookies)
        result.setResponeCode(respone.status_code)
        return result

    def requestWithOption(self, url, headers={}, entity="", isLogin=False):
        pass

    def downloadFile(self):
        pass

    def uploadFile(self):
        pass

    def doLogin(self, url, username, password, **kwargs):
        result = None
        if "kujiale" in url:
            _dict = {"email": username, "password": password, "account": username}
            result = self.requestWithPost(url=url, entity=_dict)

        self.cookies = result.getCookieJar()
        return result

    def init(self):
        pass

    def removeCookie(self):
        cookielib.CookieJar().clear()
        self.coookiejar = cookielib.CookieJar()

    def check_json_format(self, raw_msg):
        """
        用于判断一个字符串是否符合Json格式
        :param self:
        :return:
        """

        if isinstance(raw_msg, str):  # 首先判断变量是否为字符串
            try:
                json.loads(raw_msg, encoding='utf-8')
            except ValueError:
                return False
            return True
        else:
            return False


class httpResult(object):
    def __init__(self):
        """
                the construct data for the http Result
        """
        self.responeCode = None    # int
        self.isRetJson = False     # true or fault
        self.responeMsg = None     # str
        self.responeHeader = None  # list
        self.CookieJar = cookielib.CookieJar()   # instance for CookieJar()
        self.responeType = None

    def getResponeCode(self):
        return self.responeCode

    def setResponeCode(self, responeCode):
        self.responeCode = responeCode

    def setResponeMsg(self, responeMsg):
        self.responeMsg = responeMsg

    def getResponeJson(self):
        """

        :return: the json obj or None
        """
        try:
            _json = json.loads(self.getResponeMsg())
            return _json
        except Exception:
            return None

    def getResponeMsg(self):
        return self.responeMsg

    def getCookieJar(self):
        return self.CookieJar

    def setCookieJar(self, CookieJar):
        self.CookieJar = CookieJar

    def getResponeHeader(self):
        return self.responeHeader

    def setResponeHeader(self, responeHeader):
        self.responeHeader = responeHeader

    def accept(self):
        pass

    def setResponeType(self, responseType):
        self.responeType = responseType

    # @type_limit(int, int)
    def getResponeType(self):
        return self.responeType

    def check_json_format(self, raw_msg):
        """
        用于判断一个字符串是否符合Json格式
        :param self:
        :return:
        """

        if isinstance(raw_msg, str):  # 首先判断变量是否为字符串
            try:
                json.loads(raw_msg, encoding='utf-8')
            except ValueError:
                return False
            return True
        else:
            return False

    @staticmethod
    def type_limit(*typeLimit, **returnType):
        def test_value_type(func):
            def wrapper(*param, **kw):
                length = len(typeLimit)
                if length != len(param):
                    raise RuntimeWarning("The list of typeLimit and param must have the same length")
                for index in range(1, length):  # begin form 1
                    t = typeLimit[index]
                    p = param[index]
                    if not isinstance(p, t):
                        raise RuntimeWarning("The param %s should be %s,but it's %s now!"
                                             % (str(p), type(t()), type(p)))
                res = func(*param, **kw)
                if "returnType" in returnType:
                    limit = returnType["returnType"]
                    if not isinstance(res, limit):
                        raise RuntimeWarning("This function must return a value that is %s,but now it's %s"
                                             % (limit, type(res)))
                return res
            return wrapper
        return test_value_type


class httpLogin(object):
    pass


class uintTest(unittest.TestCase):
    def setUp(self):
        self.loginUrl = "xxx/login"
        self.username = "songdehua110@163.com"
        self.password = "123456"
        self.request = http_request()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)

    def testRequestPost(self):
        pass

    def testDoLogin(self):
        self.logMsg("***********************  testDoLogin Begin  ****************************")
        result = self.request.doLogin(username=self.username, password=self.password, url=self.loginUrl)
        self.logger.info("do login " + result.getResponeMsg())
        if result.responeCode != 200:
            self.assertFalse("Test Login failed " + result.getResponeCode())
        if "isBusinessAccount" not in result.getResponeJson().keys():
            self.assertFalse("isBusinessAccount not in json")
        if "userId" not in result.getResponeJson().keys():
            self.assertFalse("userId not in json")
        self.logMsg(result.getResponeJson())
        self.logMsg("***********************  testDoLogin PASS  ****************************\n")
        # self.assertTrue("************* PASS ********************\n")
        # if result.getResponeJson()[""]

    def logMsg(self, msg, level=None):
        print(msg)

    def testRequestGet(self):
        self.logMsg("******************** testRequestGet Begin ********************")
        result = self.request.doLogin(username=self.username, password=self.password, url=self.loginUrl)
        self.logger.info("do login " + result.getResponeMsg())
        if result.responeCode != 200:
            self.assertFalse("Test Login failed " + result.getResponeCode())
        if "isBusinessAccount" not in result.getResponeJson().keys():
            self.assertFalse("isBusinessAccount not in json")
        if "userId" not in result.getResponeJson().keys():
            self.assertFalse("userId not in json")
        url = "https://yun.kujiale.com/dds/api/c/floorplans" \
              "/3FO4J9NS8GYB?huxing-20170420R233B40=1&t=1492828805343"
        resultGet = self.request.requestWithGet(url=url)
        print(resultGet.getResponeCode())
        self.assertTrue(resultGet.getResponeCode()==200, "false")
        self.logMsg(resultGet.getResponeMsg())
        resultGet = self.request.requestWithGet(url="https://yun.kujiale.com/dds/api/c/layoutmodels"
                                                    "?huxing-20170420R233B40=1&t=1492828805252")
        self.assertTrue(resultGet.getResponeCode()==200, "false")
        self.logMsg(resultGet.getResponeMsg())
        self.logMsg("************************ testRequestGet PASS ********************")

    def testRequestPost(self):
        self.loginUrl = "xxx/api/login"
        self.username = "songdehua@163.com"
        self.password = "123456"
        self.logMsg("******************** testRequestPost Begin ********************")
        result = self.request.doLogin(username=self.username, password=self.password, url=self.loginUrl)
        self.logger.info("do login " + result.getResponeMsg())
        if result.responeCode != 200:
            self.assertFalse("Test Login failed " + result.getResponeCode())
        if "isBusinessAccount" not in result.getResponeJson().keys():
            self.assertFalse("isBusinessAccount not in json")
        if "userId" not in result.getResponeJson().keys():
            self.assertFalse("userId not in json")
        url = "https://sit.kujiale.com/dds/api/c/floorplans" \
              "/3FO4EFMC4B4Y?huxing-20170420R233B40=1&t=1492828805343"
        resultGet = self.request.requestWithGet(url=url)
        print(resultGet.getResponeCode())
        self.assertTrue(resultGet.getResponeCode()==200, "false")
        self.logMsg("************** get floorplan message succeed!....." + resultGet.getResponeMsg())
        resultGet = self.request.requestWithGet(url="https://yun.kujiale.com/dds/api/c/layoutmodels"
                                                    "?huxing-20170420R233B40=1&t=1492828805252")

        self.assertTrue(resultGet.getResponeCode() == 200, "false")
        postParm = resultGet.getResponeMsg()
        postParm = open('test_msg_save.txt', 'r',encoding= 'utf-8').read()
        # url = "http://sit.kujiale.com/dds/api/c/floorplans/mirror/3FO4EFMC4B4Y?axis=0&t=1492861776575"
        url = "http://sit.kujiale.com/dds/api/c/floorplans/3FO4EFMC4B4Y?t=1492862118433"
        postResult = self.request.requestWithPost(url=url, entity=postParm, headers={"Content-Type": "text/plain;charset=utf-8"})
        print(postResult.getResponeMsg())
        self.assertTrue(postResult.getResponeCode()==200, "post failed...." + str(postResult.getResponeCode()))
        print("tttttttttttttttt")
        self.logMsg(postResult.getResponeMsg())
        # self.logMsg(resultGet.getResponeMsg())
        self.logMsg("************************ testRequestPost PASS ********************")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(uintTest)
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
    print("\n")
    print('All case number')
    print(test_result.testsRun)
    print('Failed case number')
    print(len(test_result.failures))
    print('Failed case and reason')
    print(test_result.failures)
    a = json.loads('''{"name":"name"}''')

    for case, reason in test_result.failures:
        print
        case.id()
        print
        reason