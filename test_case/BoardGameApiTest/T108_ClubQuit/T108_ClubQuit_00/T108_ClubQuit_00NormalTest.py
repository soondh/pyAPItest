#!/usr/bin/env python
# -*- coding: UTF-8 -*
from test_suit.test_def import ApiTestSuit
import unittest
import sys
import os
sys.path.append(r'../../../')

try:
    from PyLogger import logging
except:
    import logging

#首先调用加入俱乐部的case，在加入俱乐部的case中会调用创建俱乐部，所以在此case中不需要再调用创建俱乐部
class T108_ClubQuit_00NormalTest(ApiTestSuit):
    """API接口测试类T108_ClubQuit_00NormalTest"""

    def setUp(self):
        """
            初始化脚本的配置
            :return:
        """
        ################################################################################
        self.script_dir = os.getcwd()
        self.script_file = __file__
        self.sub_class_name = T108_ClubQuit_00NormalTest.__name__
        self.testure_path = r"testure/T108_ClubQuit_00NormalTest.csv"
        self.config_path = r'''../config.properties'''
        self.logger = logging.getLogger(self.__class__.__name__)
        self.initConfig()
        self.regist_func(self.testT108_ClubQuit_00Normal)
        ################################################################################

    def env_setup(self):
        """
        调用T604_ApplicationResult, 加入俱乐部，然后测试退出
        :return:
        """
    def testT108_ClubQuit_00Normal(self):
        """
            测试用例主函数，若框架不能满足需求，可以重写相关beforeHttpTest, afterHttpTest, check, initConifg, checkJson
            等父类方法， 如:
            def beforeHttpTest(self, context):
                    super(T108_ClubQuit_00NormalTest, self).beforeHttpTest(context=context)
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
