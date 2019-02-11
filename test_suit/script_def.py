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

"""
    testModel---

        testCase ---

    testRuner---

    testResult---

    testLogger---

    testReporter --- html, log, file , db
"""
import os
import sys
#sys.path.append("/Users/ykadmin/projects/BGPlatform/code/pySuitTest")
sys.path.append(r"./")
sys.path.append(r"../../")
# sys.path.append(r"D:\Users\Administrator\PycharmProjects\untitled\pySuitTest-master")
_dir = os.path.dirname(__file__)
sys.path.append(os.path.dirname(_dir))
import unittest
import imp
import importlib
import inspect
import trace
import traceback
import queue
import threading

from test_suit.test_def import ApiTestSuit
from test_suit.exception_def import TestSuiteRuntimeError
from lib import HTMLTestRunner

try:
    from lib.PyLogger import pyLogger as pylogger
    from lib.PyLogger import logging
except ImportError:
    import logging

sys.path.append("..")
os.chdir("..")
TEST_CASE_DIR = "..//test_case"
SKIP_SCRIPT_LIST = ["__init__", "ApiTestSuit"]
SKIP_SCAN_CLASS = ["ApiTestSuit"]
HTTP_BASE_CLASS = ApiTestSuit

DEBUG = True
if DEBUG:
    pylogger.setStreamHander()
    # cn = logging.StreamHandler()
    # cn.setLevel(logging.DEBUG)
    # cn.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    # logging.getLogger().addHandler(cn)

def get_test_script_obj():
    pass


class TestScript(object):
    __instance = None
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        # pylogger.set_logger_config(logger=self.logger, filepath="debug.log")
        self.logger.setLevel(logging.DEBUG)
        self.path = __file__
        self.http_case_list = queue.Queue()  # the list for obj list TestCase
        self.protobuf_case_list = []
        self.automation_case_list = []
        self.DEFAULT_FILE_ID = "DEFAULT_FILE_ID"
        self._STOP_RUNNING_FLAG = False  # the flag for running suit
        self._running_threading = None     # the
        self.test_suite_result = []
        self.file_list = None
        # self.test_case_list_cache = queue.Queue()

    @classmethod
    def get_inistance(cls):
        if cls.__instance is not None:
            return cls.__instance
        else:
            cls.__instance = TestScript()
            return cls.__instance

    def run_test_class(self, case_name, report_path=None, title=u"test_report", description=u"用例测试情况"):
        """
            :param case_name: 
            :param report_path: 
            :param title: 
            :param description: 
            :return: 
        """
        case_name_list = []
        if type(case_name) == str:
            case_name_list = [case_name]
        elif type(case_name) == list:
            case_name_list = case_name

        if self.file_list is None:
            self.scan_case_dir()
        case_queue = queue.Queue()
        for name in case_name_list:
            if name.endswith(".py"):
                name = name[0: len(name)-3]
            for item in self.file_list:
                file_name = item["file_name"]
                if item["file_name"].endswith(".py"):
                    file_name = file_name[0: len(file_name)-3]
                elif item["file_name"].endswith(".pyc"):
                    file_name = file_name[0: len(file_name)-4]
                if name == file_name:
                    print("+++++++++++++++++++++++++++++")
                    print(name,file_name)
                    print("+++++++++++++++++++++++++++++")
                    model = self.import_model_from_file(file_path=item["file_path"], model_name=item["file_name"])
                    if model is None:
                        raise RuntimeError("用例脚本不符合规范:" + name)
                    case_obj = self.get_test_case_obj(model_obj=model)
                    case_queue.put(case_obj)
                    # case_obj.run_http_test()
        if report_path is None:
            while not case_queue.empty():
                case_obj = case_queue.get()
                case_obj.run_http_test()
        else:
            self.generator_report(case_queue=case_queue, report_path=report_path,
                                  title=title, description=description)

    def run_all_test(self):
        self.logger.info("Running all test suit.....")
        suite = unittest.TestSuite()
        def register_func():
            assert (True == True)
        while not self.http_case_list.empty():
            http_case_obj = self.http_case_list.get()
            # self.logger.step()
            self.logger.debug("\n Running test case...." + http_case_obj.__class__.__name__ + "\n")
            # result = http_case_obj.run_http_test()
            # self.test_suite_result.append(result)
            # suite_object = http_case_obj.class_obj()
            http_case_obj.run_http_test()
            # http_case_obj.class_obj()
            # _suite.
            # suite = unittest.TestLoader().loadTestsFromTestCase(class_obj)
            # unittest.TestLoader.loadTestsFromTestCase()
            # self.suite_result = unittest.TextTestRunner(verbosity=2).run(suite)
            # suite.addTest(http_case_obj)
        # self.suite_result = unittest.TestResult()
        # unittest.TextTestRunner.run(test=suite)
        # suite = unittest.TestLoader().loadTestsFromTestCase(GetFloorPlanTest)
        # test_result = unittest.TextTestRunner(verbosity=2).run(suite)
        # unittest.TextTestRunner
        # suite.run(result=self.suite_result)

    def run_test_suite(self):
        # self._running_process = multiprocessing.Process(target=self._test_case_runner, args=(self.path,))
        # self._running_process.start()
        self._running_threading = threading.Thread(target=self._test_case_runner, args=(self.path,))
        self._STOP_RUNNING_FLAG = False
        self._running_threading.start()

    def stop_test_suit(self):
        self._STOP_RUNNING_FLAG = True
        self.logger.info("User make a stop test suite request")
        if self._running_threading is None:
            self.logger.info("No test suite running .....")
            return None
        assert isinstance(self._running_threading, threading.Thread)
        # self._running_threading.
        try:
            self._running_threading.join(timeout=10)
        except RuntimeError as e:
            err_msg = 'Failed to join the test suite running thread: %s' % e
            self.logger.error(err_msg)
            raise TestSuiteRuntimeError(err_msg)

        # check if the test suite has been stopped
        if self._running_threading.isAlive():
            err_msg = 'Failed to join the test suite running thread, the test' \
                      'suite is still running'

            self.logger.error(err_msg)
            raise TestSuiteRuntimeError(err_msg)
        else:
            self.logger.info('The test suite has been stopped')

    def _test_case_runner(self, case_list):
        self.logger.info("Start running the test suite....")
        self.test_suite_result = []
        while not self.http_case_list.empty():
            http_case_obj = self.http_case_list.get()
            result = http_case_obj.run_http_test()
            self.test_suite_result.append(result)

    def stop_run_test(self):
        pass

    def scan_case_dir(self, path=None):
        """

        :param path:
        :return: a dirt list such as
                    [
                        {
                            "file_name": "name",
                            "file_path": "path",
                            "file_id" : "id"
                        },
                        ....
                    ]
        """
        if path is None:
            path = TEST_CASE_DIR

        if not os.path.isabs(path):
            path = os.path.join(os.path.dirname(self.path), path)

        file_list = []
        for root, dirs, files in os.walk(path):
            for file in files:
                info = {}
                if file.endswith(".py") or file.endswith(".pyc"):
                    # print(file)

                    file_path = os.path.join(root, file)
                    file_path = os.path.abspath(file_path)
                    # file_list.append(file_path)
                    info["file_name"] = file
                    info["file_path"] = file_path
                    info["file_id"] = self.DEFAULT_FILE_ID
                    file_list.append(info)
                    # print(file_path)
        self.file_list = file_list
        return file_list

    def import_case_from_dir(self, dir_path=None):
        """
            import the case from directory..... return the case object....
            :param dir_path:
            :return:
        """
        file_list = self.scan_case_dir(path=dir_path)
        model_list = []
        for item in file_list:
            file_name = item["file_name"]
            file_id = item["file_id"]
            file_path = item["file_path"]
            model_obj = self.import_model_from_file(file_path=file_path, model_name=file_name)
            model_list.append(model_obj)
        for item in model_list:
            self.import_script_from_model(model_obj=item)

    def import_model_from_file(self, file_path=None, model_name=None):
        """

            :param file:
            :return: model obj fro the script
        """
        # model = None
        try:
            # moedel = __import__(file)
            # result = sys.modules[file]
            # model = importlib.import_module(file)
            model = imp.load_source(model_name, file_path)
            return model
            # importlib.find_loader()
        except Exception as ex:
            self.logger.error('Import script %s error: %s, then skip' % (file_path, ex))
            return None

    def import_script_from_model(self, model_obj):
        # _model_obj = model_obj
        self.get_test_case(model_obj=model_obj)

    def get_test_case_obj(self, model_obj):
        # print(dir(model_obj))
        if inspect.ismodule(model_obj):
            # skip_flag = False
            for name in dir(model_obj):
                attr = getattr(model_obj, name)
                if attr is None:
                    continue
                else:
                    skip_flag = False
                    if inspect.isclass(attr):
                        for item in SKIP_SCAN_CLASS:
                            if item in attr.__name__:
                                skip_flag = True
                                # self.logger.debug("Class %s in skip list %s, then skip it"
                                #                  % (attr.__name__, str(SKIP_SCRIPT_LIST)))
                        if not skip_flag:  # skip the class define
                            if self.is_http_case(class_obj=attr):  # the test cases is http case
                                test_case_obj = TestCase(class_obj=attr)
                                # test_case_obj.run_http_test(class_obj=attr)
                                return test_case_obj
                                # test_case_obj.run_http_test(class_obj=attr)
                            elif self.is_automation_case(class_obj=attr):
                                pass
                                #
                            elif self.is_automation_case(class_obj=attr):
                                pass

        else:
            return None

    def get_test_case(self, model_obj):
        # print(dir(model_obj))
        if inspect.ismodule(model_obj):
            # skip_flag = False
            for name in dir(model_obj):
                attr = getattr(model_obj, name)
                if attr is None:
                    continue
                else:
                    skip_flag = False
                    if inspect.isclass(attr):
                        for item in SKIP_SCAN_CLASS:
                            if item in attr.__name__:
                                skip_flag = True
                                # self.logger.debug("Class %s in skip list %s, then skip it"
                                #                  % (attr.__name__, str(SKIP_SCRIPT_LIST)))
                        if not skip_flag:  # skip the class define
                            if self.is_http_case(class_obj=attr):  # the test cases is http case
                                test_case_obj = TestCase(class_obj=attr)
                                # test_case_obj.run_http_test(class_obj=attr)
                                self.logger.debug("Adding test case to the case list ...."
                                                  "" + attr.__name__)
                                self.add_http_test_case(test_case_obj=test_case_obj)
                                return test_case_obj
                                # test_case_obj.run_http_test(class_obj=attr)
                            elif self.is_automation_case(class_obj=attr):
                                pass
                                #
                            elif self.is_automation_case(class_obj=attr):
                                pass

        else:
            return None

    def add_http_test_case(self, test_case_obj):
        """

        :param test_case_obj:
        :return:
        """
        self.http_case_list.put(test_case_obj)

    def pop_http_test_case(self, test_case_obj):
        return self.http_case_list.get()

    def is_http_case(self, class_obj):
        """
        :param class_obj: the class_boj father object must be the HTTP_BASE_CLASS
        :return:
        """
        # print(type(HTTP_BASE_CLASS))
        # return issubclass(class_obj, HTTP_BASE_CLASS)
        BASE_HTTP_OBJ = HTTP_BASE_CLASS()
        # print(class_obj.__bases__)
        # print(issubclass(class_obj, BASE_HTTP_OBJ.__class__))
        # print(class_obj.__bases__[0].__name__)
        # print(BASE_HTTP_OBJ.__class__.__name__)
        if class_obj.__bases__[0].__name__ == HTTP_BASE_CLASS.__name__:

            return True
            # print(class_obj.__bases__[0].__name__, class_obj)
        # print(type(HTTP_BASE_CLASS.__bases__[0]) == BASE_HTTP_OBJ.__class__)
        # isinstance(class_obj.__bases__, )
        return issubclass(class_obj, BASE_HTTP_OBJ.__class__)
        # return True

    def is_automation_case(self, class_obj):
        pass

    def is_protobuf_case(self, class_obj):
        pass

    def import_case_from_file_list(self, file_list):
        for file in file_list:
            # a = "" #("")
            for item in SKIP_SCRIPT_LIST:
                if item in file:
                    continue
            model = None
            try:
                model = exec("import %s" % file)
            except Exception:
                raise Exception("")

    def generator_simple_report(self, report_path="./ResultReport/test_report.html",
                                title=u"test_report", description=u"用例测试情况"):
        def register_func():
            assert(True == True)
        suite = unittest.TestSuite()
        while not self.http_case_list.empty():
            http_case_obj = self.http_case_list.get()
            suite_object = None
            # print(dir(http_case_obj.class_obj))
            for item in dir(http_case_obj.class_obj):

                if item.startswith("test"):
                    if callable(getattr(http_case_obj.class_obj, item)):
                        # print(item)
                        suite_object = http_case_obj.class_obj(item)
                    # print(item)
            # if hasattr(suite_object, "runTest"):
            #     pass
            # else:
            #
            #     suite_object.runTest = register_func
            # suite.addTest()
            if suite_object is not None:
                suite.addTest(suite_object)
        # test_result = unittest.TestResult()
        # suite.run(result=test_result)
        # unittest.TextTestRunner(verbosity=2).run(suite)
        fp = open(report_path, "wb")
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=title, description=description)
        runner.run(suite)
        # result = runner.sortResult(result_list=self.test_suite_result)
        # runner.generateReport(test=None, result=self.suite_result)

    def generator_report(self, case_queue, report_path="./ResultReport/test_report.html",
                                title=u"test_report", description=u"用例测试情况"):
        def register_func():
            assert(True == True)
        suite = unittest.TestSuite()
        while not case_queue.empty():
            http_case_obj = case_queue.get()
            suite_object = None
            for item in dir(http_case_obj.class_obj):

                if item.startswith("test"):
                    if callable(getattr(http_case_obj.class_obj, item)):
                        # print(item)
                        suite_object = http_case_obj.class_obj(item)
            if suite_object is not None:
                suite.addTest(suite_object)
        fp = open(report_path, "wb")
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=title, description=description)
        runner.run(suite)
        fp.close()

class TestModel(object):
    def __init__(self, fileName):
        try:
            model = exec("import %s" % fileName)
        except Exception:
            pass

    # def _import_model_from_d


class TestCase(object):
    MODEL = ["HTTP_INTERFACE, PROTOBUF_INTERFACE, AUTOMATION_SCRIPT"]
    HTTP_MODEL = "HTTP_MODEL"

    def __init__(self, class_obj, case_type=HTTP_MODEL, case_id=None, case_info_obj=None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.class_obj = class_obj
        self.case_type = case_type
        self.case_id = case_id
        if case_info_obj is None:
            case_info_obj = CaseInfo()
        self.case_info_obj = case_info_obj

    def get_case_mode(self):
        """
            test case 种类， 分为http接口测试，protobuf接口测试， 自动化测试
        :return:
        """
        pass

    def _run_http_test(self, class_obj=None):
        pass

    def run_http_test(self, class_obj=None):
            # multiprocessing.Process
        test_result = None
        if class_obj is not None:
            suite = unittest.TestLoader().loadTestsFromTestCase(class_obj)
            test_result = unittest.TextTestRunner(verbosity=2).run(suite)
        else:
            suite = unittest.TestLoader().loadTestsFromTestCase(self.class_obj)
            test_result = unittest.TextTestRunner(verbosity=2).run(suite)
        return test_result

    def run_script_test(self, class_obj=None):
        return None

    def get_class_obj_instance(self):
        return self.class_obj()

    def get_test_method_name(self):
        for item in dir(self.class_obj()):
            if item.startswith("test"):
                pass
                # print(item)


class CaseInfo(object):
    pass


if __name__ == "__main__":
    inputs=len(sys.argv)
    case_list=[]
    test_script_obj = TestScript.get_inistance()
    if(inputs>1):
        for case_item in sys.argv[1:]:
            case_list.append(case_item)
        test_script_obj.run_test_class(case_name=case_list, report_path="test003.html")
    else:
        #run all test cases
        test_script_obj.run_test_class(case_name=["T101_ClubCreate_01NormalTest","T101_ClubCreate_00NormalTest"], report_path="test002.html")
        pass

    # file_list = test_script_obj.import_case_from_dir(dir_path=r"D:\Users\Administrator\PycharmProjects\untitled\pySuitTest-master\test_case\BoardGameApiTest\T101_ClubCreate")
    # print(file_list)
    # model = test_script_obj.import_model_from_file(file_path="D:\\Users\Administrator\IdeaProjects\pySuitTest\\test_case\dds"
    #                                                "\ApiGetFloorPlan\\apiGetFloorPlan.py", model_name="aipGetFlooriPlan")
    # test_script_obj.import_script_from_model(model_obj=model)
    # test_script_obj.run_all_test()
    #print(test_script_obj.http_case_list)
    # test_script_obj.run_all_test()
    #test_script_obj.run_test_class(case_name=["T101_ClubCreate_00NormalTest"],report_path="test001.html")
    # test_script_obj.generator_simple_report(report_path="test.html")
    # test_script_obj.run_test_suite()
    # test_script_obj.stop_test_suit()
    # b=2