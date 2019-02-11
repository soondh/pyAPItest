#!/usr/bin/env python
# -*- coding: UTF-8 -*
from test_suit.test_def import ApiTestSuit
from test_suit.script_def import TestScript
import unittest
import sys
import os
import csv
import pymysql
sys.path.append(r'../../../')

try:
    from PyLogger import logging
except:
    import logging

#通过申请
class T602_ApplicationCheck_00NormalTest(ApiTestSuit):
    """API接口测试类T602_ApplicationCheck_00NormalTest"""

    def setUp(self):
        """
            初始化脚本的配置
            :return:
        """
        ################################################################################
        self.script_dir = os.getcwd()
        self.script_file = __file__
        self.sub_class_name = T602_ApplicationCheck_00NormalTest.__name__
        self.testure_path = r"testure/T602_ApplicationCheck_00NormalTest.csv"
        self.config_path = r'''../config.properties'''
        self.logger = logging.getLogger(self.__class__.__name__)
        self.env_setup()
        self.initConfig()
        self.regist_func(self.testT602_ApplicationCheck_00Normal)
        ################################################################################

    def env_setup(self):
        """
        调用T603_00,创建加入申请
        :return:
        """
        test_script = TestScript.get_inistance()
        test_script.run_test_class(case_name=["T603_ApplicationCreate_00NormalTest"])

        # 获取user_id以及club_id
        conn = pymysql.connect(host='10.225.136.162', port=3306, user='root', passwd='zhouyang123',
                               db='zhuoyou')
        cur = conn.cursor()
        cur.execute("SELECT MAX(id) FROM zhuoyou_user")
        user_id = cur.fetchone()[0]

        cur.execute("SELECT MAX(id) FROM zhuoyou_club_user_application")
        application_id = cur.fetchone()[0]
        conn.close()

        # 修改csv
        headers = ['caseId', 'caseDesc', 'isRun', 'priority', 'httpType', 'apiPath', 'verifyReCode', 'paramUrl.user_id',
                   'paramUrl.application_id', 'paramUrl.result']
        rows = [('01', '', 'true', 1, 'post', '/application/check?', 200, user_id, application_id, 1)]

        curr_path = os.path.dirname(__file__)
        with open(curr_path + r'\testure\T602_ApplicationCheck_00NormalTest.csv', 'w', encoding='utf-8') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(headers)
            f_csv.writerows(rows)

        f.close()

    def testT602_ApplicationCheck_00Normal(self):
        """
            测试用例主函数，若框架不能满足需求，可以重写相关beforeHttpTest, afterHttpTest, check, initConifg, checkJson
            等父类方法， 如:
            def beforeHttpTest(self, context):
                    super(T602_ApplicationCheck_00NormalTest, self).beforeHttpTest(context=context)
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
