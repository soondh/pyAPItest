#!/usr/bin/env python
# -*- coding: UTF-8 -*

###############################################################################
# Copyright (C), 2017 SongDehua
#
# Filename:     configUtil.py
# Version:      1.0.0
# Description:  Module for pySuit frame to maniputlate the conf
#
# ig file.
# Author:       songdehua
# History:
#   1. 2017-04-25  songdehua, first create
###############################################################################

"""Module for pySuit frame

    This module exports a class to manipulate the config file:
    class configParser: manipulate the config file
"""

import configparser


class configParser(object):
    def __init__(self, configPath=None):
        self.config = configparser.ConfigParser()
        self.config.read(configPath, encoding="UTF-8")
        self.sessions = self.config.sections()

    def getSectionByName(self, section, name):
        return self.config.get(section=section, option=name)

    def getConfigByNmae(self, name):
        for item in self.sessions:
            # pass
            print(self.config.options(item))

    def writeSeesionByName(self, session, name):
        pass

    def __getitem__(self, item):
        for session in self.sessions:
            if self.config.has_option(session, item):
                return self.config.get(session, item)
        raise RuntimeError("Item not in the configFile..." + item)


if __name__ == "__main__":
    _path = r'''..\test_case\dds\config.properties'''
    config = configParser(configPath=_path)
    print(config.config.get("loginConfig", "remoteUrl"))
    print(config.getConfigByNmae("remoteUrl"))
    print(config.sessions)
    print(config.__dict__)
    print(config["remoteUrl"])
    print(config["loginHost"])
