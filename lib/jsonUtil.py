#!/usr/bin/env python
# -*- coding: UTF-8 -*

###############################################################################
# Copyright (C), 2017 SongDehua
#
# Filename:     jsonUtil.py
# Version:      1.0.0
# Description:  Module for pySuit frame to compare the json(dict) obj
# Author:       songdehua
# History:
#   1. 2017-04-25  songdehu, first create
###############################################################################

"""Module for pySuit frame
    This module exports a class to compare the json(dict) obj:
    class JsonUtil: comparison for the json
"""

import json
import re
import unittest


class JsonUtil(object):
    """
        JSON 对比的方式

    """
    JSON_CMP_MODEL = ["FULL", "KEY", "FULL_R"]
    Reg_Prefix = "@r="
    instance = None
    def __init__(self):
        # self.instance = None
        pass

    def cmpJosnFull(self, baseJson={}, cmpJson={}):
        """

        :param json:
        :param cmpJson:
        :return:
        """
        result = JsonCmpResult(result=True, Msg="")
        for item in baseJson.keys():
            if item in cmpJson.keys():
                if baseJson[item] != cmpJson[item]:
                    msg = "key-value:" + str(item) + ":" + baseJson[item] + \
                          " ,do not match compared json, real:" + item + ":" \
                          + cmpJson[item] + "..." + str(cmpJson)
                    result.setMsg(msg)
                    result.setResult(False)
                    return result
            else:
                msg = "key-value: " + '''{'%s': '%s'}''' % (str(item), baseJson[item]) + \
                      " ,do not match compared json," + "\n..." + str(cmpJson)
                result.setMsg(msg)
                result.setResult(False)
                return result
        result.setMsg("%s baseJson match %s compared json" % (str(baseJson), str(cmpJson)))
        result.setResult(True)
        return result

    def comJsonKeys(self, baseJson={}, cmpJson={}):
        """
        :param json:
        :param cmpJson:
        :return:
        """
        result = JsonCmpResult(result=True, Msg="")
        for item in baseJson.keys():
            if item not in cmpJson.keys():
                msg = "key:" + str(item) + " do not in compared json..." + str(cmpJson)
                result.setMsg(msg)
                result.setResult(False)
                return result
        result.setMsg("%s baseJson match %s compared json" % (str(baseJson), str(cmpJson)))
        result.setResult(True)
        return result

    def comJsonAllReg(self, baseJson={}, cmpJson={}):
        """

        :param baseJson:
        :param comJson:
        :return:
        """
        result = JsonCmpResult(result=True, Msg="")
        for item in baseJson.keys():
            if item in cmpJson.keys():
                if isinstance(baseJson[item], str) and JsonUtil.Reg_Prefix in baseJson[item]:  # define as reg
                    if isinstance(baseJson[item], str) and isinstance(cmpJson[item], str):
                        baseStr = baseJson[item]
                        cmpStr = str(cmpJson[item])
                        # JsonUtil.Reg_Prefix
                        reMsg = baseStr.split(JsonUtil.Reg_Prefix)[1]
                        m = re.match(reMsg, cmpStr)
                        if m is None:
                            Msg = "Regular..." + '''{'%s': '%s'}''' % (item, reMsg) + \
                                  ", do not match...{'%s': '%s'}" % (item, cmpStr)
                            result.setResult(result=False)
                            result.setMsg(msg=Msg)
                            return result
                else:
                    if baseJson[item] != cmpJson[item]:
                        msg = "key-value: " + '''{'%s': '%s'}''' % (str(item), baseJson[item]) + \
                              " ,do not match compared json,  {'%s': '%s'}"  %(str(item), str(cmpJson[item])) \
                              + "\n..." + str(cmpJson)
                        result.setMsg(msg)
                        result.setResult(False)
                        return result
            else:
                msg = "key:" + str(item) + " do not in compared json..." + str(cmpJson)
                result.setMsg(msg)
                result.setResult(False)
                return result
        result.setMsg("%s baseJson match %s compared json" % (str(baseJson), str(cmpJson)))
        result.setResult(True)
        return result

    def exchangeStrToJson(self, message=None):
        return json.loads(message)

    @staticmethod
    def getInstance():
        if JsonUtil.instance is None:
            JsonUtil.instance = JsonUtil()
        return JsonUtil.instance


class JsonCmpResult(object):
    def __init__(self, result=False, Msg="", **kwargs):
        self.result = result
        self.msg = Msg

    def setResult(self, result):
        self.result = result

    def getResult(self):
        return self.result

    def setMsg(self, msg):
        self.msg = msg

    def getMsg(self):
        return self.msg


class JsonUtilTest(unittest.TestCase):

    def testJsonUtil_cmpJsonFull(self):
        baseJson = {"name": 1, "name2": False, "name3": "test"}
        cmpJson = {"name": 1, "name2": False, "name3": "test3"}
        result = JsonUtil.getInstance().cmpJosnFull(baseJson, cmpJson)
        print(result.getMsg())
        self.assertFalse(result.getResult(), result.getMsg())
        cmpJson_2 = {"name": 1, "name2": False, "name3": "test"}
        result = JsonUtil.getInstance().cmpJosnFull(baseJson, cmpJson_2)
        print(result.getMsg())
        self.assertTrue(result.getResult(), result.getMsg())
        cmpJson_3 = {"name": 1, "name2": False}
        result = JsonUtil.getInstance().cmpJosnFull(baseJson, cmpJson_3)
        print(result.getMsg())
        self.assertFalse(result.getResult(), result.getMsg())

    def testJsonUtil_cmpJsonKeys(self):
        baseJson = {"name": 1, "name2": False, "name3": "test"}
        cmpJson = {"name": 1, "name2": False, "name3": "test3", "name4":None}
        result = JsonUtil.getInstance().comJsonKeys(baseJson, cmpJson)
        print(result.getMsg())
        self.assertTrue(result.getResult(), result.getMsg())
        # cmpJson_2 = {"name": 1, "name2": False, "name3": "test"}
        # result = JsonUtil.getInstance().cmpJosnFull(baseJson, cmpJson_2)
        # print(result.getMsg())
        # self.assertTrue(result.getResult(), result.getMsg())
        # cmpJson_3 = {"name": 1, "name2": False}
        # result = JsonUtil.getInstance().cmpJosnFull(baseJson, cmpJson_3)
        # print(result.getMsg())
        # self.assertFalse(result.getResult(), result.getMsg())
        pass

    def testJsonUtil_comJsonAllReg(self):
        baseJson = {"name": 1, "name2": False, "name3": "@r=.+test"}
        cmpJson = {"name": 1, "name2": False, "name3": "---test3", "name4":None}
        result = JsonUtil.getInstance().comJsonAllReg(baseJson, cmpJson)
        print(result.getMsg())
        self.assertTrue(result.getResult(), result.getMsg())
        baseJson = {"name": 1, "name2": False, "name3": "@r=.+test4"}
        result = JsonUtil.getInstance().comJsonAllReg(baseJson, cmpJson)
        self.assertFalse(result.getResult(), result.getMsg())
        baseJson = {"name": 1, "name2": False, "name3": "@r=---test3"}
        result = JsonUtil.getInstance().comJsonAllReg(baseJson, cmpJson)
        self.assertTrue(result.getResult(), result.getMsg())

if __name__ == "__main__":
    # unittest.main()
    _json = {"name"}
    baseJson = {"name": 1, "name2": False, "name3": "test"}
    cmpJson = {"name": 1, "name2": False, "name3": "test3"}
    result = JsonUtil.getInstance().cmpJosnFull(baseJson, cmpJson)
    _str = '''{name:1, '项目':2}'''
    _str2 = '''{"name":false, "test":"@r=123"}'''
    # _str = json.dumps(_str)
    # json_string = json.dumps(_str2)
    j = json.loads(_str2)
    print(j)
