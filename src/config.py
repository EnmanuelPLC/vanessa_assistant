""" Config handler of entire assistant """
import configparser as cfg
import os.path
from os.path import isfile


class AssistantConf:
    """ Core assistant config handler"""
    first_use: bool
    app_conf: cfg.ConfigParser
    user_conf: cfg.ConfigParser
    sys_conf: cfg.ConfigParser

    def __init__(self):
        self.app_conf = cfg.ConfigParser()
        self.user_conf = cfg.ConfigParser()
        self.sys_conf = cfg.ConfigParser()
        self.init_conf_files()

    def init_conf_files(self):
        if not isfile('conf/assistant.ini'):
            self._create_cfg_files()
        else:
            self._read_cfg_files()

    def _read_cfg_files(self):
        self.app_conf.read('conf/assistant.ini')
        self.save('assistant', 'first_use', 'False')
        self.user_conf.read('conf/user.ini')
        self.sys_conf.read('conf/sys.ini')

    def _create_cfg_files(self):
        if not os.path.isdir('conf'):
            os.mkdir('conf')
        with open('conf/assistant.ini', 'w+') as configfile:
            self.app_conf.add_section('assistant')
            self.app_conf['assistant']['first_use'] = 'True'
            self.app_conf.write(configfile)
        with open('conf/user.ini', 'w+') as configfile:
            self.user_conf.add_section('user')
            self.user_conf.write(configfile)
        with open('conf/sys.ini', 'w+') as configfile:
            self.sys_conf.add_section('system')
            self.sys_conf.write(configfile)

    def save(self, section, field, value):
        if section == 'assistant':
            self.app_conf['assistant'][field] = value
            with open('conf/assistant.ini', 'w+') as configfile:
                self.app_conf.write(configfile)
        elif section == 'system':
            self.sys_conf['system'][field] = value
            with open('conf/sys.ini', 'w+') as configfile:
                self.sys_conf.write(configfile)
        elif section == 'user':
            self.user_conf['user'][field] = value
            with open('conf/user.ini', 'w+') as configfile:
                self.user_conf.write(configfile)
        else:
            print(f"There's no configuration available for {section} type")

    def read(self, section, field):
        if section == 'assistant':
            return self.app_conf[section][field]
        elif section == 'system':
            return self.sys_conf[section][field]
        elif section == 'user':
            return self.user_conf[section][field]
        else:
            print(f"There's no configuration available for {section} type")
