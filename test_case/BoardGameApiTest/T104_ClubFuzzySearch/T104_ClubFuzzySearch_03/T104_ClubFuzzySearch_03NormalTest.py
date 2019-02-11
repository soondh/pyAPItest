#!/usr/bin/env python
# -*- coding: UTF-8 -*
from test_suit.test_def import ApiTestSuit
from test_suit.script_def import TestScript
import unittest
import sys
import os
import csv
sys.path.append(r'../../../')

try:
    from PyLogger import logging
except:
    import logging

#搜索结果翻页
class T104_ClubFuzzySearch_03NormalTest(ApiTestSuit):
    """API接口测试类T104_ClubFuzzySearch_03NormalTest"""

    def setUp(self):
        """
            初始化脚本的配置
            :return:
        """
        ################################################################################
        self.script_dir = os.getcwd()
        self.script_file = __file__
        self.sub_class_name = T104_ClubFuzzySearch_03NormalTest.__name__
        self.testure_path = r"testure/T104_ClubFuzzySearch_03NormalTest.csv"
        self.config_path = r'''../config.properties'''
        self.logger = logging.getLogger(self.__class__.__name__)
        self.env_setup()
        self.initConfig()
        self.regist_func(self.testT104_ClubFuzzySearch_03Normal)
        ################################################################################

    def env_setup(self):
        """
        首先调用T101_00创建一个俱乐部
        :return:
        """
        test_script = TestScript.get_inistance()
        test_script.run_test_class(case_name=["T101_ClubCreate_00NormalTest"])

        # 修改csv
        headers = ['caseId', 'caseDesc', 'isRun', 'priority', 'httpType', 'apiPath', 'verifyReCode', 'cd', 'paramUrl.game_id', 'paramUrl.province',
                   'paramUrl.city', 'paramUrl.district', 'paramUrl.page']
        rows = [('01', '', 'true', 1, 'post', '/club/fuzzySearch?', 200, 0, 1, '浙江省', '杭州市', '西湖区', 2)]

        curr_path = os.path.dirname(__file__)
        with open(curr_path + r'\testure\T104_ClubFuzzySearch_03NormalTest.csv', 'w', encoding='utf-8') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(headers)
            f_csv.writerows(rows)

        f.close()

    def testT104_ClubFuzzySearch_03Normal(self):
        """
            测试用例主函数，若框架不能满足需求，可以重写相关beforeHttpTest, afterHttpTest, check, initConifg, checkJson
            等父类方法， 如:
            def beforeHttpTest(self, context):
                    super(T104_ClubFuzzySearch_03NormalTest, self).beforeHttpTest(context=context)
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
