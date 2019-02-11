# -*- coding: utf-8 -*-

import unittest
import time,sys
import HTMLTestRunner


class Baidu(unittest.TestCase):
    """百度首页搜索测试用例"""

    def setUp(self):
        pass

    def testAdd(self):
        self.assertTrue(True, "123")

    def tearDown(self):
        pass
        # self.driver.quit()


if __name__ == "__main__":
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    testunit = unittest.TestSuite()
    testunit.addTest(Baidu("testAdd"))
    HtmlFile = "HTMLtemplate.html"
    fp = open(HtmlFile, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"百度测试报告", description=u"用例测试情况")
    HTMLTestRunner.HTMLTestRunner
    runner.run(testunit)