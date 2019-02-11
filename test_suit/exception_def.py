#!/usr/bin/env python
# -*- coding: UTF-8 -*
"""define the Excpetion class for pysuit"""


class http_requestException(Exception):
    pass


class ApiTestSuitException(Exception):
    pass


class runContextException(Exception):
    pass


class ContextException(Exception):
    pass


class ConfigDataException(Exception):
    pass


class PrepareDataException(Exception):
    pass


class csvUtilException(Exception):
    pass


class InvalidTestCase(IOError):
    pass


class InvalidTestSuite(IOError):
    pass


class InvalidTestScript(IOError):
    pass


class TestCaseSearchError(IOError):
    pass


class TestCaseRunningError(IOError):
    pass


class TestSuiteBreakExp(IOError):
    pass


class TestSuiteRuntimeError(IOError):
    pass


class InvalidTestResult(IOError):
    pass


class InvalidTestCaseParam(IOError):
    pass


class TestResultError(IOError):
    pass


class TestReportError(IOError):
    pass


class DevInfoNoSuchValue(IOError):
    pass


class DevInfoDuplicateDev(IOError):
    pass


class DevInfoNoSuchDev(IOError):
    pass

