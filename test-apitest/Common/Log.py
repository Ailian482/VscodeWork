import logging
import os
import time
import threading
from Config import ReadConfig

'''AutoInterface 日志类'''


class log(object):
    # 初始化日志
    _instance_lock = threading.Lock()

    def __init__(self, name=None):
        readconfig = ReadConfig.readconfig()
        now_time = time.strftime("%Y-%m-%d", time.localtime())
        path = readconfig.get_basepath("base_path")
        self.filepath = os.path.join(
            path, 'Log', 'AutoInterfacelog_{0}.log' .format(now_time))
        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            self.file_hander = logging.FileHandler(self.filepath, encoding='UTF-8')
            self.system_hander = logging.StreamHandler()
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s')
            self.file_hander.setFormatter(file_formatter)
            self.system_hander.setFormatter(file_formatter)
            self.logger.addHandler(self.system_hander)
            self.logger.addHandler(self.file_hander)

    def get_logger(self):
        return self.logger


if __name__ == '__main__':
    f = log('LOG运行main方法')
    f.get_logger().info(u'这是我的一个日志测试')

