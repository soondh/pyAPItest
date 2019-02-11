#!/usr/bin/env python
# -*- coding: UTF-8 -*
import logging
import sys
reload(sys)
# sys.setdefaultencoding('gbk')

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='logger_static_ui.log',
                    filemode='w')
logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)
