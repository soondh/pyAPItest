#!/usr/bin/env python
# -*- coding: UTF-8 -*

###############################################################################
# Copyright (C), 2017 SongDehua
#
# Filename:     test_def.py
# Version:      1.0.0
# Description:  Module for pySuit frame to manage the test procedure
# Author:       songdehua
# History:
#   1. 2017-04-25  songdehua, first create
###############################################################################

"""Module for pySuit frame
    class ApiTestSuit: exports to manage the test procedure
                runContext ---
                        configData(global)
                        prepareDataList(list obj for prepareData)
                        currentContext(Context obj) ---
                                                        prepareData
                                                        httpResult
                                                        configData
                                                        httpClient
                        httpResultList(list obj for httpResult)
    class runContext : the global context for the procedure
    class Context    : the running context for the procedure
    class ConfigData : the config obj for the runContext
    class PrepareData: the csv prepare data for the context
    class HttpMethod : enum for http method
"""

import unittest
import sys
import time
import os
import traceback
import copy
import urllib
from enum import Enum
sys.path.append("..")
try:
    from httplib.httpRequest import http_request
    from lib.csvUtil import csvutil as PrepareDataUtil
    from lib.configUtil import configParser
    from lib.jsonUtil import *
except ImportError:
    sys.path.append("..")
    from httplib.httpRequest import http_request
    from lib.csvUtil import csvutil as PrepareDataUtil
    from lib.configUtil import configParser
try:
    from lib.PyLogger import pyLogger as pylogger
    from lib.PyLogger import logging
except ImportError:
    import logging

logger = pylogger.getLogger("ApiTestSuit")
logger.setLevel(logging.DEBUG)
STEP = 25  # between INFO and WARN


class ApiTestSuit(unittest.TestCase):
    """
    """

    def initConfig(self):
        self.step = """
                            Step1 初始化运行上下文对象 initContext
                            Step2 加载测试配置文件config，包含登陆信息、域名信息等
                            Step3 加载测试脚本的数据csv文件，并且生成测试用例,每一个用例包含一个context对象
                            Step4 根据生成测试用例调用runHttpTest
                            Step5 根据csv文件对比返回结果
        """
        """
        PySuit
        1.技术方案选型 (python + unittest)
        2.python，java
        3.后端、前端 django + react
        4.设计思路、思想
        5.数据结构设计
        6.流程图设计
        """
        """
            runContext ---
                        configData(global)
                        prepareDataList(list obj for prepareData)
                        currentContext(Context obj) ---
                                                        prepareData
                                                        httpResult
                                                        configData
                                                        httpClient
                        httpResultList(list obj for httpResult)
        """
        # if self.logger is None:
        self.logger = pylogger.getLogger(self.__class__.__name__)
        self.logger = logger
        self.setLogger()
        # pylogger.setSreamHandler()
        self.logger.step(self.step)
        self.logger.step("初始化上下文对象....")
        self.logger.debug("创建全局runContext对象.....")
        self.runContext = runContext()
        if os.name == "nt":
            pass
        # os.path.dirname(self.script_dir)
        self.script_dir = os.path.dirname(self.script_file)
        _path = os.path.join(os.path.abspath(self.script_dir), self.config_path)

        # print(os.path.dirname(self.script_dir))
        _path = os.path.abspath(_path)
        self.logger.debug("初始化配置数据,生成configData对象..." + _path)
        self.runContext.configData = ConfigData(configPath=_path)
        self.logger.debug("加载配置文件成功..." + str(self.runContext.configData))
        obs_path = os.path.abspath(self.script_file)
        if obs_path.endswith(".py"):
            obs_path = os.path.dirname(obs_path)
        _path = os.path.join(obs_path, self.testure_path)
        _path = os.path.abspath(_path)
        self.logger.step("加载csv数据文件，生成prepareDataList对象...." + _path)
        self.caseNum = PrepareData(csv_file_path=_path, index=0).caseNum
        self.runContext.prepareDataList = []
        for i in range(self.caseNum):
            self.runContext.prepareDataList.append(PrepareData(csv_file_path=_path, index=i))
        if not self.runContext.prepareDataList:
            self.logger.warn("csv数据为空....退出")
            return None
        logger.debug("加载csv数据文件成功...." + str(self.runContext.prepareDataList[0]) + "...")
        # self.runContext.prepareDataList = PrepareData(csv_file_path=_path, index=0)
        self.logger.debug("创建全局runContext对象成功.....包含csv数据、配置数据信息...")
        self.logger.debug("创建运行的http_request对象.....httpClient\n")
        self.httpClient = http_request()

    def getScriptServerName(self, file_path):
        _path = os.path.dirname(file_path)
        return os.path.basename(_path)

    def getScriptFileName(self, file_path):
        return os.path.basename(file_path)

    def startTest(self, runContext):
        """

            :param runContext:
            :return:
        """
        self.logger.debug("start run test...." + self.__class__.__name__)
        self.logger.debug("")
        result = True
        self.logger.step("开始运行测试用例.....共有" + str(self.caseNum) + "个测试用例")
        for i in range(len(self.runContext.prepareDataList)):
            self.logger.step("开始运行第 " + str(i+1) + " 个测试用例")

            self.currentContex = Context(runContext.prepareDataList[i], runContext.configData)
            self.runContext.currentContext = self.currentContex
            isRun = self.currentContex.getPrepareData().getIsRun()
            if not isRun:
                self.logger.debug("当前第 %s 个用例设置为不运行.... 跳过..." % str(i+1))
                continue
            try:
                self.currentContex.httpClient = self.httpClient
                self.beforeHttpTest(context=self.currentContex)
                self.runHttpTest(context=self.currentContex)
                self.checkResult(context=self.currentContex)
                self.afterHttpTest(context=self.currentContex)
            except Exception:
                result = False
                self.logger.warning("TestCase error....")
                self.logger.error(traceback.print_exc(Exception))
                self.assertTrue(result, "Test Result failed...")
            finally:
                runContext.currentCaseNum += 1
                self.logger.step("运行第 %s 个用例完毕....\n" % (i + 1))
            # try:
            #     self.beforeHttpTest(context=self.currentContex)
            #     self.runHttpTest(context=self.currentContex)
            #     self.afterHttpTest(context=self.currentContex)
            # except Exception:
            #     result = False
            #     self.logger.warning("TestCase error....")
            #     self.logger.error(traceback.print_exc(Exception))
            # finally:
            # runContext.currentCaseNum += 1
            # self.logger.step("运行第 %s 个用例完毕....\n" % (i + 1))

        self.afterClassTest(context=Context)
        self.assertTrue(result, "Test Result ....")

    def beforeHttpTest(self, context):
        pass

    def afterHttpTest(self, context):
        pass

    def beforeClassTest(self, context):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def afterClassTest(self, context):
        pass

    def runHttpTest(self, context):
        id = context.prepareData.getCaseId()
        desc = context.prepareData.getCaseDesc()
        self.logger.debug("运行用例id:" + str(id))
        self.logger.debug("运行用例description:" + str(desc))
        # print(Context.isNeedLogin)
        if not context.isNeedLoginFirst():
            self.logger.info("当前用例不需要登录....跳过登录")
        else:
            # self.logger.debug()
            self.logger.debug("开始登录....")
            _str = str(self.doLogin(context=context))
            self.logger.debug("登录成功....返回:" + _str)
        self.logger.info("开始执行http方法....")

        strMsg = context.getStrSendText()
        headers = context.getHttpSendHeaders()
        httpType = context.getHttpType()

        url = context.getBaseUrl() + context.getHttpSendUrl()

        if httpType is None or httpType == "":
            self.logger.warning("httpType is none")
            httpType = HttpMethod.GET

        httpResult = None

        if httpType.upper() == HttpMethod.GET.value:
            httpResult = context.httpClient.requestWithGet(url=url, headers=headers, isLogin=False, entity=None)
        elif httpType.upper() == str(HttpMethod.POST.value):
            httpResult = context.httpClient.requestWithPost(url=url, headers=headers, isLogin=False, entity=strMsg)
        elif httpType.upper() == HttpMethod.HEAD.value:
            httpResult = context.httpClient.requestWithHead(url=url, headers=headers, isLogin=False, entity=strMsg)
        elif httpType.upper() == HttpMethod.OPTIONS.value:
            httpResult = context.httpClient.requestWithOption(url=url, headers=headers, isLogin=False, entity=strMsg)
        elif httpType.upper() == HttpMethod.DELETE.value:
            httpResult = context.httpClient.requestWithDelete(url=url, headers=headers, isLogin=False, entity=strMsg)
        elif httpType.upper() == HttpMethod.PUT.value:
            httpResult = context.httpClient.requestWithPut(url=url, headers=headers, isLogin=False, entity=strMsg)
        else:
            pass
            # raise RuntimeError("httpType do not exit..." + httpType)
        context.setHttpResult(httpResult)
        if self.logger_file_fp is not None:
            if hasattr(self.logger_file_fp, "close"):
                self.logger_file_fp.close()

        self.logger.info("执行完毕....")

        # logging.getLogger().removeHandler()

    def doLogin(self, context):
        pass
        #_str = Context.

    def setLogger(self):

        ISOTIMEFORMAT ='%Y-%m-%d_%H_%M_%S'
        _time = time.strftime(ISOTIMEFORMAT, time.localtime())
        # self.logger = self.logger
        # self.logger.step = self.logger_step
        self.logger.step = self.logger_step
        serverNmae = self.getScriptServerName(self.script_dir)
        file_name = self.getScriptFileName(self.script_dir)
        logger_name = self.sub_class_name + "_" + _time + ".log"
        log_ = r"../../../log/%s/%s/" % (serverNmae, file_name)
        # os.path.dirname(__file__)

        log_ = os.path.join(os.path.dirname(self.script_dir), r"../log")
        log_ = log_ + "/" + logger_name
        self.log_file = os.path.abspath(log_)
        # print(self.log_file)
        script_dir = os.path.dirname(self.script_file)
        log_file = os.path.join(os.path.dirname(self.script_file), logger_name)
        if "test_case" in log_file:
            log_file = log_file.replace("test_case", "log")

        if os.path.exists(log_file):
            return
        # logging.getLogger("").addHandler()
        self.logger_file_fp = pylogger.set_logger_config(logger=self.logger, filepath=log_file)
        pylogger.setStreamHander()

    def logger_step(self, message, *args, **kws):
        # Yes, self.logger takes its '*args' as 'args'.
        if self.logger.isEnabledFor(STEP):
            self.logger._log(STEP, message, args, **kws)

    def getRelativePath(self, fatherPath, subPath):
        pass

    def checkResult(self, context):
        self.checkResponseCode(context=context)
        self.checkResponseContent(context=context)
        verfiyJson = context.getPrepareData().getVerfiyJson()
        if verfiyJson:
            self.logger.step("csv文件 verFiyJson 不为空... %s, 校验返回结果" % str(verfiyJson))
            self.checkResponseMsg(context=context)
        self.checkDb(context=context)

    def checkResponseCode(self, context):
        responseCode = context.getHttpResult().getResponeCode()
        prepareCode = context.prepareData.getExceptRetCode()
        if responseCode == prepareCode:
            self.logger.info("状态码对比成功...." + str(responseCode))
            self.assertTrue(True, "返回状态码匹配成功" + str(responseCode))
        else:
            self.logger.error("状态码对比失败....返回:" + str(responseCode))
            self.assertTrue(False, "返回状态码不匹配，期望 %s, 实际返回 %s" % (str(prepareCode), str(responseCode)))

    def checkDb(self, context):
        pass

    def checkResponseJson(self, context):
        resultJson = context.getHttpResult().getResponeJson()
        cmpJson = context.getPrepareData().getVerfiyJson()
        # exchange the str msg to the json
        if cmpJson is not None:
            self.logger.debug("CSV进行Json对比..." + str(cmpJson))
            jsonUtil = JsonUtil.getInstance()
            resultJson = jsonUtil.exchangeStrToJson(resultJson)
            cmpJson = jsonUtil.exchangeStrToJson(cmpJson)
            result = JsonUtil.comJsonAllReg(resultJson, cmpJson)
            self.assertTrue(result.getResult(), result.getMsg())
            self.logger.debug("Json对比结果：" + result.getMsg())
        else:
            self.logger.debug("CSV文件没有设置json对比，跳过...")

    def checkResponseMsg(self, context):
        self.logger.debug("准备进行返回值json/str校验....")
        cmpJson = context.getPrepareData().getVerfiyJson()
        responseMsg = context.getHttpResult().getResponeMsg()
        if not context.httpClient.check_json_format(cmpJson):
            self.logger.info("检查josnVerfiy为字符串模式...")
            self.checkResponseStr(context=context)
            self.logger.debug("str校验完成...")

        elif context.httpClient.check_json_format(cmpJson) and context.httpClient.check_json_format(responseMsg):
            self.logger.step("检查jsonVerfiy为json对比模式...")
            self.checkResponseJson(context=context)
            self.logger.step("json校验完成...")
        else:
            self.logger.error("返回值和准备数据....格式不一致,退出校验...")

    def checkResponseContent(self,context):
        resultJson = context.getHttpResult().getResponeJson()
        cdexpected = resultJson['cd']
        #responseMsg = context.getHttpResult().getResponeMsg()
        #cdexpected = responseMsg.split('":"')[1].split('"')[0]
        prepareCd = context.prepareData.getExceptCd()

        if cdexpected == prepareCd:
            self.logger.info("消息码对比成功...." + str(cdexpected))
            self.assertTrue(True, "返回消息码匹配成功" + str(cdexpected))
        else:
            self.logger.error("消息码对比失败....返回:" + str(cdexpected))
            self.assertTrue(False, "返回消息码不匹配，期望 %s, 实际返回 %s" % (str(prepareCd), str(cdexpected)))



    def checkResponseStr(self, context):
        self.logger.debug("进行字符串模式对比....")
        cmpJson = context.getPrepareData().getVerfiyJson()
        responseMsg = context.getHttpResult().getResponeMsg()
        reg = cmpJson
        if "@r=" in cmpJson:
            reg = cmpJson.split("@r=")[1]
            msg = "对比失败， %s 不在返回值中， %s" % (str(cmpJson), str(responseMsg))
            self.assertRegex(responseMsg, reg, msg=msg)
            self.logger.info("对比成功， %s 在返回值中， %s" % (str(reg), str(responseMsg)))
        else:
            msg = "对比失败， %s 不在返回值中， %s" % (str(cmpJson), str(responseMsg))
            self.assertRegex(responseMsg, reg, msg=msg)
            self.logger.info("对比成功， %s 在返回值中， %s" % (str(reg), str(responseMsg)))

    def generatorTestResult(self, path, classname):
        pass
        # self.

    def regist_func(self, func, **kwargs):
        self.register_func = func

    def Run(self):

        pass

    # def runTest(self):
    #     pass
        # self.logger.info("hee eee")

    def run_other_dir_case(self, dir_path, pattern):
        """

        :param dir_path: 
        :param pattern: 
        :return: 
        """
        suite_result = []
        # sys.path.append(dir_path)
        try:
            discover = unittest.defaultTestLoader.discover(dir_path, pattern=pattern, top_level_dir=dir_path)
        except Exception as ex:
            sys.path.append(dir_path)
            discover = unittest.defaultTestLoader.discover(dir_path, pattern=pattern, top_level_dir=dir_path)

        for test_suite in discover:
            result = unittest.TextTestRunner(verbosity=2).run(test_suite)
            suite_result.append(result)
        return suite_result

class ApiTestSuitRunner(object):

    pass


class runContext(object):
    def __init__(self):
        """
                runContext 代表一个脚本中的运行上下文

        """
        # *** 当前http返回的结果
        self.currentHttpResult = None  # a obj of httpResult
        # *** 所有的http 返回结果
        self.httpResultList = None  # a list of currentHttpResult list
        # *** 当前csv配置数据
        self.currentPareData = None
        # *** 所有的csv 配置文件 parepareDataList, a [] for obj parepareData
        self.prepareDataList = None  # a list of PrepareData object
        # ***
        # 服务中的配置文件
        self.configData = None
        #
        # 当前用例运行的位置 【】
        self.currentCaseNum = 0
        #
        self.contextList = []

        self.currentContext = None

    def isNeedLoginFirst(self):
        pass

    def getConfigData(self):
        return self.configData

    def setConfigData(self, configData):
        self.configData = configData

    def __setitem__(self, key, value):
        if key not in self.__dict__.keys():
            raise RuntimeError("Could not define the key by yourself "
                               "in runContext obj..." + key)
        self.__dict__[key] = value

    def __getitem__(self, item):
        return self.__dict__[item]

    def __getattr__(self, item):
        if item.startswith("get"):
            _str = ""
            item = item[3:len(item)]
            _str = item[0].lower() + item[1:len(item)]
            if hasattr(self, _str):
                obj = getattr(self, _str)
                if callable(obj):
                    pass  # skip callable object
                else:
                    return lambda: self.__getitem__(_str)
            else:
                # print(hasattr(self, _str))
                raise AttributeError("The param do not exit in PrepareData object..." + _str)
        elif item.startswith("set"):
            _str = ""
            item = item[3:len(item)]
            _str = item[0].lower() + item[1:len(item)]
            if hasattr(self, _str):
                obj = getattr(self, _str)
                if callable(obj):
                    pass  # skip callable object
                else:
                    return lambda word: self.__setitem__(_str, word)
            else:
                # print(hasattr(self, _str))
                raise AttributeError("The param do not exit in PrepareData object..." + _str)

        else:
            raise AttributeError("The param do not exit in PrepareData object..." + item)

    def __repr__(self):
        return ""


class Context(object):
    """
        一个用例可以认为是一行csv数据，
        Context代表一个用例运行的上下文，
        一个脚本可以包含多个用例
    """
    def __init__(self, PrepareDataObj, ConfigDataObj):
        self.logger = pylogger.getLogger(self.__class__.__name__)
        self.prepareData = PrepareDataObj

        self.configData = ConfigDataObj
        # *************   当前用例的http配置  ****************
        #             Http类型，头部，body，url部分
        self.httpType = PrepareDataObj["httpType"]
        # http发送的
        self.strSendText = PrepareDataObj["strSendText"]
        # http的发送的url链接
        self.httpSendUrl = PrepareDataObj["httpSendUrl"]
        #
        self.httpSendHeaders = PrepareDataObj["httpSendHeaders"]
        #
        self.isRun = PrepareDataObj["isRun"]
        #
        self.httpClient = None
        #
        # ************ 当前用例的登录配置  ****************
        self.isNeedLogin = PrepareDataObj["isNeedLogin"]
        # ***
        self.caseId = PrepareDataObj["caseId"]
        # ***
        self.baseUrl = ConfigDataObj["reomveUrl"]
        #
        self.loginUrl = ConfigDataObj["loginUrl"]
        # ************ 结果返回配置   ******************
        self.httpResult = None

    def getHttpClient(self):
        if self.httpClient is None:
            self.httpClient = http_request()
        return self.httpClient

    def setHttpClient(self, httpClient):
        self.httpClient = http_request()

    def getPrepareData(self):
        return self.prepareData

    def getConfigData(self):
        return self.configData

    def getBaseUrl(self):
        return self.baseUrl
    
    def isNeedLoginFirst(self):
        return self.isNeedLogin

    def getHttpResult(self):
        return self.httpResult

    def setHttpResult(self, httpResult):
        self.httpResult = httpResult

    def getStrSendText(self):
        return self.strSendText

    def setStrSendText(self, text):
        self.strSendText = text

    def getHttpSendUrl(self):
        return self.httpSendUrl

    def setHttpSendUrl(self, url):
        self.httpSendUrl = url

    def getHttpSendHeaders(self):
        return self.httpSendHeaders

    def setHttpSendHeaders(self, headers):
        self.httpSendHeaders = headers

    def getHttpType(self):
        return self.httpType

    def setHttpType(self, httpType):
        self.httpType = httpType


class ConfigData(object):
    def __init__(self, configPath=""):
        self.configPath = configPath
        self.loginUrl = None
        self.reomveUrl = None
        self.dbType = None
        self.dbPassword = None
        self.dbUsername = None
        self.dbUrl = None
        self.usernameInfo = None  # a dirt such as {"account":ApiTest@163.com}
        self.passwordInfo = None    # a dirt such as {"password":"1233456"}
        self.username = None
        self.password = None
        self.configParase = configParser(configPath=configPath)
        self.initParam()

    def initParam(self):
        if not os.path.isfile(self.configPath):
            raise RuntimeError("配置文件路径错误..." + self.configPath)
        _parse = self.configParase
        self.loginUrl = _parse["loginHost"]
        self.reomveUrl = _parse["remoteUrl"]
        self.dbUrl = _parse["db_url"]
        self.dbUsername = _parse["db_username"]
        self.dbPassword = _parse["db_password"]

        self.passwordInfo = _parse["logginPassword"]
        self.usernameInfo = _parse["logginName"]
        if ":" in self.passwordInfo:
            self.usernameInfo = self.usernameInfo.replace(" ", "")
            self.username = self.usernameInfo.split(":")[1]
            # self.usernameInfo = {self.username}
        else:
            self.username = self.usernameInfo

        if ":" in self.passwordInfo:
            self.passwordInfo = self.passwordInfo.replace(" ", "")
            self.password = self.passwordInfo.split(":")[1]
        else:
            self.password = self.passwordInfo

    def getLoginDict(self):
        pass

    def getLoginUrl(self):
        return self.loginUrl

    def setLoginUrl(self, url):
        self.loginUrl = url

    def __setitem__(self, key, value):
        if key not in self.__dict__.keys():
            raise RuntimeError("Could not define the key by yourself "
                               "in runContext obj..." + key)
        self.__dict__[key] = value

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return str(self.__dict__)

    def getConfig(self, section, name):
        return self.configParase.getSectionByName(section=section, name=name)


class PrepareData(object):
    def __init__(self, csv_file_path, index):
        self.logger = pylogger.getLogger(self.__class__.__name__)
        # / ** 测试用例ID * /
        self.caseId = None
        # / ** 测试用例详情 * /
        self.caseDesc = ""
        # / ** 当前用例是否运行 * /
        self.isRun = True
        # /** 测试用例优先级，P0做为冒烟测试用例 */
        self.priority = None
        # /**  HTTP请求方式  */
        self.httpType = None
        # /**  请求服务 */
        self.apiPath = None  # str
        # /**  发送请求的参数 */
        self.mapSendParam = None  # dict
        # /**  post请求中，直接在url中的参数 */
        self.mapPostUrlParam = None   # dict
        # /**  发送请求的http 的Header参数 */
        self.mapHttpHeadParam = None  # dict
        # /**  需要比较的JSON内容  */
        self.retMapJsonAssert = None
        # /**  其他需要的参数  */
        self.mapUserParam = None  # dict
        # /**  期望返回的返回码  */
        self.exceptRetCode = None  # int
        # /**  期望返回的消息状态  */
        self.expectCd = None  # int
        # /** 是否需要登录
        self.isNeedLogin = True
        # / **　期望比较的json 对象
        self.verfiyJson = None
        # key/rkey 代表键对、正则表达式
        # 同理 val/rVal 代表普通对比、正则表达式

        # / ** 期望对比结果方式
        self.compareJsonType = ["OnlyKey", "ALL", "R"]
        # 1.对比是否包含json的key
        # 2.对比包含json 的 key--value
        # 3.对比正则表达式匹配json的 key -- value 字段
        # /**** http param ******/
        self.strSendText = None
        # / **url, headers={} , entity=None
        self.httpSendUrl = None
        # /
        self.httpSendHeaders = None  # {} dict
        # /
        # ***************  not user *************************************
        # /**  需要先进行构造的数据库数据  */
        self.mapInsertDb = None
        # /**  需要比较的数据库  */
        self.retMapDbAssert = None
        # ***************  not user *************************************
        self.csvList = None
        self._prepareDataUtil = PrepareDataUtil(csv_file_path)
        self.caseNum = len(self._prepareDataUtil.csv_list)
        self.initParam(csv_file_path=csv_file_path, index=index)
        # ***************************  not finish ***************************************

    def getExceptCd(self):
        return self.expectCd

    def serExceptCd(self, exceptcd):
        self.expectCd = exceptcd

    def getExceptRetCode(self):
        return self.exceptRetCode

    def setExceptRetCode(self, exceptRetCode):
        self.exceptRetCode = exceptRetCode

    def getCaseId(self):
        return self.caseId

    def setCaseId(self, caseId):
        self.caseId = caseId

    def getCaseDesc(self):
        return self.caseDesc

    def setCaseDesc(self, caseDesc):
        self.caseDesc = caseDesc

    def getHttpType(self):
        return self.httpType

    def setHttpType(self, httpType):
        self.httpType = httpType

    def getApiPath(self):
        return self.apiPath

    def setApiPath(self, apiPath):
        self.apiPath = apiPath

    def getMapSendParam(self):
        return self.mapSendParam

    def setMapSendParam(self, mapSendParam):
        self.mapSendParam = mapSendParam

    def getMapPostUrlParam(self):
        return self.mapPostUrlParam

    def setMapPostUrlParam(self, mapPostUrlParam):
        self.mapPostUrlParam = mapPostUrlParam

    def getMapHttpHeadParam(self):
        return self.mapHttpHeadParam

    def setMapHttpHeadParam(self, mapHttpHeadParam):
        self.mapHttpHeadParam = mapHttpHeadParam

    def getRetMapJsonAssert(self):
        return self.retMapJsonAssert

    def setRetMapJsonAssert(self, retMapJsonAssert):
        self.retMapJsonAssert = retMapJsonAssert

    def getMapUserParam(self):
        return self.mapUserParam

    def setMapUserParam(self, mapUserParam):
        self.mapUserParam = mapUserParam

    def getVerfiyJson(self):
        return self.verfiyJson

    def setVerfiyJson(self, verfiyJson):
        self.verfiyJson = verfiyJson

    def getCompareJsonType(self):
        return self.compareJsonType

    def setCompareJsonType(self, compareJsonType):
        self.compareJsonType = compareJsonType

    def getMapInsertDb(self):
        return self.mapInsertDb

    def setMapInsertDb(self, mapInsertDb):
        self.mapInsertDb = mapInsertDb

    def getRetMapDbAssert(self):
        return self.retMapDbAssert

    def setRetMapDbAssert(self, retMapDbAssert):
        self.retMapDbAssert = retMapDbAssert

    def getIsNeedLogin(self):
        return self.isNeedLogin

    def setIsNeedLogin(self, isNeedLogin):
        self.isNeedLogin = isNeedLogin

    def setIsRun(self, isRun):
        self.isRun = isRun

    def getIsRun(self):
        return self.isRun

    def getPriority(self):
        return self.priority

    def initParam(self, csv_file_path="", index=0):
        """

        :param csv_file_path:
        :param index:
        :return:
        """
        if self._prepareDataUtil:
            _prepareData = PrepareDataUtil(csv_file_path)
        else:
            _prepareData = self._prepareDataUtil
        if self.caseNum == 0:
            self.logger.warning("csv数据文件数据为空...")
            return None

        self.setCaseId(_prepareData.getCaseId(index=index))
        self.caseDesc = _prepareData.getCaseDesc(index=index)
        self.isRun = _prepareData.getIsRun(index=index)
        self.priority = _prepareData.getPriority(index=index)
        self.httpType = _prepareData.getHttpType(index=index)
        self.apiPath = _prepareData.getApiPath(index=index)
        self.exceptRetCode = int(_prepareData.getVerifyReCode(index=index))
        self.mapSendParam = _prepareData.getMapSendParam(index=index)
        self.expectCd = _prepareData.getCdexpected(index=index)

        self.mapUserParam = _prepareData.getMapUserParam(index=index)
        self.verfiyJson = _prepareData.getVerfiyJson(index=index)
        self.mapHttpHeadParam = _prepareData.getMapHttpHeadParam(index=index)
        self.mapPostUrlParam = _prepareData.getMapPostUrlParam(index=index)
        self.strSendText = _prepareData.getStrSendText(index=index)
        self.httpSendHeaders = _prepareData.getHttpSendHeaders(index=index)
        self.httpSendUrl = _prepareData.getHttpSendUrl(index=index)
        self.isNeedLogin = _prepareData.getIsLogin(index=index)

    def getInstance(self, index=0):
        pass

    def getMapSendParamFromCsv(self, csv_list, index):
        """

        :param csv_list:   LIST 、                this list for csv file
        :param index:      int  、                the index of row for the csv file
        :return:           Objcet(PrepaareData)、 the PrepareData Objcet

        """
        pass

    def getCaseIdFromCsv(self, csv_list, index):
        pass

    def getPrepareDataObjFromCsv(self, csv_list, index):
        pass

    def __setitem__(self, key, value):
        if key not in self.__dict__.keys():
            raise RuntimeError("Could not define the key by yourself "
                               "in runContext obj..." + key)
        self.__dict__[key] = value

    def __getitem__(self, item):

        return self.__dict__[item]

    def __getattr__(self, item):
        if item.startswith("get"):
            _str = ""
            item = item[3:len(item)]
            _str = item[0].lower() + item[1:len(item)]
            if hasattr(self, _str):
                obj = getattr(self, _str)
                if callable(obj):
                    pass  # skip callable object
                else:
                    return lambda: self.__getitem__(_str)
            else:
                # print(hasattr(self, _str))
                raise AttributeError("The param do not exit in PrepareData object..." + _str)
        elif item.startswith("set"):
            _str = ""
            item = item[3:len(item)]
            _str = item[0].lower() + item[1:len(item)]
            if hasattr(self, _str):
                obj = getattr(self, _str)
                if callable(obj):
                    pass  # skip callable object
                else:
                    return lambda word: self.__setitem__(_str, word)
            else:
                # print(hasattr(self, _str))
                raise AttributeError("The param do not exit in PrepareData object..." + _str)

        else:
            raise AttributeError("The param do not exit in PrepareData object..." + item)

    def __str__(self):
        return str(self.__dict__)


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PUT = "PUT"
    DELETE = "DELETE"
    TRACE = "TRACE"


if __name__ == "__main__":
    pass
