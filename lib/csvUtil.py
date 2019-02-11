#!/usr/bin/env python
# -*- coding: UTF-8 -*

###############################################################################
# Copyright (C), 2017 SongDehua
#
# Filename:     csvUtil.py
# Version:      1.0.0
# Description:  Module for pySuit frame to maniputlate the csv file.
# Author:       songdehua
# History:
#   1. 2017-04-25  songdehua, first create
###############################################################################

"""Module for pySuit frame

    This module exports a class to manipulate the csv file:
    class csvutil: manipulate the csv file
"""

import csv
import os
import logging
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

GLOBAL_CONFIG_SETTING = {
    "csv_list": ["caseId", "caseDesc", "isRun", "priority", "httpType", "apiPath", "verifyReCode", "paramUrl.xxx",
                    "paramBody.xxx", "paramHeader.xxxx", "jsonVerify.xxxx","dbInsert.xxx", "dbVerify.xxxx", "dbClean.xxxx"],
    "caseId": True,
    "caseDesc": True,

}
CSV_BASE_LIST = ["caseId", "caseDesc", "isRun", "priority", "httpType", "apiPath", "verifyReCode",
                 "paramBody", "verfiyJson",  "verfiyJsonMode", "paramHeader.xxx", "paramUrl.xxx", "dbInsert", "dbClean"]

verfiyJsonMode = ["KEY", "FULL", "REG"]

CASV_WRITE_DATA = [ ]


CSV_APPEND_LIST = ["paramUrl", "paramHeader", "jsonVerify",
                   "dbInsert", "dbVerify", "dbClean"]


class csvutil(object):
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.csv_append_list = CSV_APPEND_LIST
        self.csv_base_list = CSV_BASE_LIST
        self.csv_list = csvReader(csv_path)
        self.logger = logging.getLogger(self.__class__.__name__)

    def getCaseId(self, csv_list=None, index=0):
            """

            :param csv_list:
            :param index:
            :return: str(caseId) or none
            """
            if not csv_list:
                csv_list = self.csv_list
            if "caseId" not in csv_list[0].keys():
                return "Default Id" + str(index)
            else:
                return csv_list[index]["caseId"]

    def getCaseDesc(self, csv_list=None, index=0):
        """

        :param csv_list:
        :param index:
        :return: str(caseId) or none
        """
        if not csv_list:
            csv_list = self.csv_list
        if "caseDesc" not in csv_list[0].keys():
            return ""
        else:
            return csv_list[index]["caseDesc"]

    def getIsLogin(self, csv_list=None, index=0):
        if not csv_list:
            csv_list = self.csv_list
        if "isLogin" not in csv_list[0].keys():
            return True
        else:
            if "false" in csv_list[index]["isLogin"].lower():
                return False
            else:
                return True

    def getIsRun(self, csv_list=None, index=0):
        """

        :param csv_list:
        :param index:
        :return: true or false
        """
        if not csv_list:
            csv_list = self.csv_list
        if "isRun" not in csv_list[0].keys():
            return True
        else:
            if "false" in csv_list[index]["isRun"].lower():
                return False
            else:
                return True

    def getPriority(self, csv_list=None, index=0):
        """
        :param csv_list:
        :param index:
        :return: int 0 , 1, 2, 3, 4, 5, 6
        """
        if not csv_list:
            csv_list = self.csv_list
        if "priority" not in csv_list[0].keys():
            return 0
        else:
            priority = csv_list[index]["priority"]
            if priority == "" or priority == "none":
                return 0
            else:
                try:
                    priority = int(priority)
                    return priority
                except Exception:
                    return 0

    def getHttpType(self, csv_list=None, index=0):
        """
        :param csv_list:
        :param index:
        :return: the httpType in ["GET", "POST", "HEAD", "OPTIONS", "PUT", "DELETE", "TRACE"]
        """
        if not csv_list:
            csv_list = self.csv_list
        if "httpType" not in csv_list[0].keys():
            raise RuntimeError("httpType param not in csvFile...." + str(csv_list[0].keys()) )
        else:
            if csv_list[index]["httpType"].upper() in ["GET", "POST", "HEAD", "OPTIONS", "PUT", "DELETE", "TRACE"]:
                return csv_list[index]["httpType"].upper()
            else:
                raise RuntimeError("httpType must in " +
                                   str(["GET", "POST", "HEAD", "OPTIONS", "PUT", "DELETE", "TRACE"])
                                   + " but found " + csv_list[index]["httpType"].upper())

    def getApiPath(self, csv_list=None, index=0):
        """

        :param csv_list:
        :param index:
        :return:
        """
        if not csv_list:
            csv_list = self.csv_list
        if "apiPath" not in csv_list[0].keys():
            raise RuntimeError("apiPath param not in csvFile...." + str(csv_list[0].keys()))
        else:
            return csv_list[index]["apiPath"]

    def getVerifyReCode(self, csv_list=None, index=0):
        """

        :param csv_list:
        :param index:
        :return:
        """
        if not csv_list:
            csv_list = self.csv_list
        if "verifyReCode" not in csv_list[0].keys():
            raise RuntimeError("verifyReCode param not in csvFile...." + str(csv_list[0].keys()))
        else:
            return csv_list[index]["verifyReCode"]

    # end with not finish >>>>>>>>>>>>>>>>>>>>>>>>>>
    def getMapSendParam(self, csv_list=None, index=0):
        """
        :param csv_list:
        :param index:
        :return: collection.dict
        """
        if not csv_list:
            csv_list = self.csv_list
        keys = csv_list[0].keys()
        headers = {}
        # "paramHeader" in csv_list[0].keys()
        for item in keys:
            if "paramHeader." in item:
                _key = item.split(".")[1]
                headers[_key] = csv_list[index][item]
        return headers

    def getCdexpected(self, csv_list=None, index=0):
        """
        :param csv_list
        :param index:
        :return:
        """
        if not csv_list:
            csv_list = self.csv_list
        if "cd" not in csv_list[0].keys():
            raise RuntimeError("cd param not in csvFile...." + str(csv_list[0].keys()) )
        else:
            if csv_list[index]["cd"].isdigit():
                return csv_list[index]["cd"]
            else:
                raise RuntimeError("cd must be integer")

    def getVerfiyJson(self, csv_list=None, index=0):
        """

        :param csv_list:
        :param index:
        :return: None or "" or str
        """
        if not csv_list:
            csv_list = self.csv_list
        isExit = False
        if "verfiyJson" not in csv_list[0].keys():
            verfiyJsonDict = {}
            for item in csv_list[0].keys():
                if "verfiyJson" in item.lower():
                    isExit = True
                    verfiyJsonDict[item.split(".")[1]] = csv_list[index][item]
            if not isExit:
                self.logger.warning("verfiyJson Dict param not in csvFile...." + str(csv_list[0].keys()))
                return None
            return str(verfiyJsonDict)
            # raise RuntimeWarning("verfiyJson param not in csvFile...." + str(csv_list[0].keys()))
        else:
            _str = csv_list[index]["verfiyJson"]
            _parent = os.path.dirname(self.csv_path)
            if "@path=" in _str:
                path = _str.split("@path=")[1]
                _path = os.path.join(_parent, path)
                with open(_path, 'r+', encoding='UTF-8') as f:
                    _str_ = f.read()
                return _str_.strip().replace('\ufeff', '')
            else:
                return _str

    def getMapUserParam(self, csv_list=None, index=0):
        """

        :param csv_list:
        :param index:
        :return: dict
        """
        if not csv_list:
            csv_list = self.csv_list
        _dict = {}
        _keys = csv_list[0].keys()
        for item in _keys:
            if item in CSV_BASE_LIST:
                pass
            elif item in CSV_APPEND_LIST:
                pass
            else:
                _dict[item] = csv_list[index][item]
        return _dict

    def getMapHttpHeadParam(self, csv_list=None, index=0):
        """

        :param csv_list:
        :param index:
        :return: dict
        """
        if not csv_list:
            csv_list = self.csv_list
        _dict = {}
        _keys = csv_list[0].keys()
        for item in _keys:
            if item in CSV_BASE_LIST:
                pass
            elif item in CSV_APPEND_LIST:
                pass
            elif "paramheader" in item.lower():
                _dict[item.split(".")[1]] = csv_list[index][item]
        return _dict

    def getMapPostUrlParam(self, csv_list=None, index=0):
        """

        :param csv_list:
        :param index:
        :return:
        """
        if not csv_list:
            csv_list = self.csv_list
        _dict = {}
        _keys = csv_list[0].keys()
        for item in _keys:
            if item in CSV_BASE_LIST:
                pass
            elif item in CSV_APPEND_LIST:
                pass
            elif "paramurl." in item.lower():
                _dict[item.split(".")[1]] = csv_list[index][item]
        return _dict

    def getStrSendText(self, csv_list=None, index=0):
        """

        :param csv_list:
        :param index:
        :return: str or None
        """
        if not csv_list:
            csv_list = self.csv_list
        isExit = False
        if "paramBody" not in csv_list[0].keys():
            paramBodyDict = {}
            for item in csv_list[0].keys():
                if "parambody" in item.lower():
                    isExit = True
                    paramBodyDict[item.split(".")[1]] = csv_list[index][item]
            if not isExit:
                self.logger.warning("paramBody param not in csvFile...." + str(csv_list[0].keys()))
                return None
            return paramBodyDict
            # raise RuntimeWarning("paramBody param not in csvFile...." + str(csv_list[0].keys()))
        else:
            _str = csv_list[index]["paramBody"]
            _parent = os.path.dirname(self.csv_path)
            _str = _str.replace(" ", "")
            if "@path=" in _str:
                path = _str.split("@path=")[1]
                _path = os.path.join(_parent, path)
                with open(_path, 'r+', encoding='UTF-8') as f:
                    _str_ = f.read()
                return _str_.strip().replace('\ufeff', '')
            else:
                return _str

    def getHttpSendUrl(self, csv_list=None, index=0):
        """

        :param csv_list:
        :param index:
        :return:
        """
        apiPath = self.getApiPath(csv_list=csv_list, index=index)
        url_dict = self.getMapPostUrlParam(csv_list=csv_list, index=index)
        for item in url_dict.keys():
            _str = "&" + item + "=" + url_dict[item]
            apiPath += _str
        return apiPath

    def getHttpSendHeaders(self, csv_list=None, index=0):
        return self.getMapHttpHeadParam(csv_list=csv_list, index=index)
    
    def getVerifyJsonMode(self, csv_list=None, index=0):
        """

        :param csv_list:
        :param index:
        :return:
        """
        if not csv_list:
            csv_list = self.csv_list
        if "verfiyJsonMode" not in csv_list[0].keys():
            return None
            # raise RuntimeError("verfiyMode param not in csvFile...." + str(csv_list[0].keys()))
        else:
            return csv_list[index]["verfiyJsonMode"].upper()


def csvReader(filePath):
    """

    :param filePath:
    :return:  a list for csv
    """
    with open(filePath, 'r', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, quoting=csv.QUOTE_ALL, dialect="excel")
        rows = [row for row in reader]
    return rows


def csvWriterBase(filePath, quoting=csv.QUOTE_ALL):
    csvfile = open(filePath, 'w', encoding="utf-8")
    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL, dialect="excel")
    writer.writerow(CSV_BASE_LIST)
    csvfile.close()


def csvWriterList(filePath, csvlist, quoting=csv.QUOTE_ALL):
    csvfile = open(filePath, 'w', encoding="utf-8")
    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL, dialect="excel")
    writer.writerow(CSV_BASE_LIST)
    csvfile.close()


# class csvTest(object):
#     def testFunc(self):
#         csv_util = csvutil(csv_path=None)
#         print(csv_util.getApiPath(csv_list, 0))
#         print (csv_util.getCaseDesc(csv_list, 0))

        # assertTrue(csv_util.getApiPath(csv_list, 0))

if __name__ == "__main__":
    # csvtest = csvTest()
    # csvtest.testFunc()
    pass