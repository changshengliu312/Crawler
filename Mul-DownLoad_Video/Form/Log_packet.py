# -*- coding:UTF-8 -*-
import logging
import logging.handlers
import configparser as CP

class CreateLog():
    def __init__(self):
        config = CP.ConfigParser()
        config.read( 'config.ini' )
        self.key = config.get( 'log', 'key' )
        self.level = config.get( 'log', 'level' )
        self.name = config.get( 'log', 'name' )
        self.path = config.get( 'log', 'path' )

        # 创建一个logger
        self.logger = logging.getLogger()

    def set_parameter(self):
        if self.level == 'Debug':
            self.logger.setLevel(logging.DEBUG)
        elif self.level == 'INFO':
            self.logger.setLevel( logging.INFO)
        elif self.level == 'WAERNING':
            self.logger.setLevel( logging.WARNING)
        elif self.level == 'ERROR':
            self.logger.setLevel( logging.ERROR)

    def get_loggger(self):
        self.set_parameter()
        filename = self.path + '/' + self.name
        fh = logging.FileHandler(filename=filename,mode='a', encoding='utf-8')
        # 定义handler的输出格式formatter
        formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s - %(message)s]')
        fh.setFormatter( formatter )
        self.logger.addHandler( fh )

        return self.logger
