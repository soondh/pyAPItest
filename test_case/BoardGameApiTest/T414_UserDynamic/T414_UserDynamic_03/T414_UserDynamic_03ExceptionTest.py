#!/usr/bin/env python
# -*- coding: UTF-8 -*
import unittest
import sys
import os
sys.path.append(r'../../../')

from test_suit.test_def import ApiTestSuit

try:
    from PyLogger import logging
except:
    import logging


class T414_UserDynamic_03ExceptionTest(ApiTestSuit):
    """API接口测试类T414_UserDynamic_03ExceptionTest"""

    def setUp(self):
        """
            初始化脚本的配置
            :return:
        """
        ################################################################################
        self.script_dir = os.path.dirname(__file__)
        self.script_file = __file__
        self.sub_class_name = T414_UserDynamic_03ExceptionTest.__name__
        self.testure_path = r"testure/T414_UserDynamic_03ExceptionTest.csv"
        self.config_path = r'''../config.properties'''
        self.logger = logging.getLogger(self.__class__.__name__)
        self.initConfig()
        self.regist_func(self.testT414_UserDynamic_03Exception)
        ################################################################################

    def testT414_UserDynamic_03Exception(self):
        """
            测试用例主函数，若框架不能满足需求，可以重写相关beforeHttpTest, afterHttpTest, check, initConifg, checkJson
            等父类方法， 如:
            def beforeHttpTest(self, context):
                    super(T414_UserDynamic_03ExceptionTest, self).beforeHttpTest(context=context)
                    self.logger.info("before HttpTest in this..............")
        :return:
        """
        self.logger.info("#########################　Begin Test Method　#####################################")
        self.startTest(runContext=self.runContext)

    def beforeHttpTest(self, context):
        """
        调用runHttpTest 前先调用函数,子类重写可以自定义相关功能
        Parameters:
            context - this is the first param
        Returns:
            None
        Raises:
            None
        """
        self.logger.info("before HttpTest in this..............")

    def afterHttpTest(self, context):
        """
        调用runHttpTest 后调用函数,子类重写可以自定义相关功能
        Parameters:
            context - this is the first param
        Returns:
            None
        Raises:
            None
        """
        self.logger.info("After HttpTest in this...............")

    def tearDown(self):
        """
            脚本执行后函数
            :return:
        """
        self.logger.info("#################################　End Test　######################################")


if __name__ == "__main__":
    unittest.main()
