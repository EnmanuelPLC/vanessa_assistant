""" Config handler of entire assistant """
import configparser as cfg
from os.path import isfile


class AssistantConf:
    """ Core assistant config handler"""
    first_use: bool
    app_conf: cfg.ConfigParser
    user_conf: cfg.ConfigParser
    sys_conf: cfg.ConfigParser

    def __init__(self):
        self.first_use = False
        self.app_conf = self.user_conf = self.sys_conf = cfg.ConfigParser()
        self.init_conf_files()

    def init_conf_files(self):
        if not isfile('conf/assistant.ini'):
            self.first_use = True
            self._create_cfg_files()
        else:
            self._read_cfg_files()

    def _read_cfg_files(self):
        self.app_conf.read('conf/assistant.ini')
        self.user_conf.read('conf/user.ini')
        self.sys_conf.read('conf/sys.ini')

    def _create_cfg_files(self):
        with open('conf/assistant.ini', 'w+') as configfile:
            self.app_conf.write(configfile)
        with open('conf/user.ini', 'w+') as configfile:
            self.user_conf.write(configfile)
        with open('conf/sys.ini', 'w+') as configfile:
            self.sys_conf.write(configfile)
