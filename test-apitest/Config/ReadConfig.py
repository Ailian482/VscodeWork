import configparser
import os

'''读取配置文件'''


# 读取当前Project下的配置文件config.ini


class readconfig:
    def __init__(self):
        path = os.path.split(__file__)[0]
        self.filepath = os.path.join(path, 'config.ini')
        self.readconfig = configparser.ConfigParser()
        self.readconfig.read(self.filepath, encoding='UTF-8')
        # self.readconfig.write(filepath)

    # 获取HTTPURL配置信息
    def get_URL(self, name):
        self.name = self.readconfig.get('HTTPURL', name)
        return self.name

    # 获取HEADERS配置信息
    def get_Header(self, name):
        self.name = self.readconfig.get('HEADERS', name)
        return self.name

    # 获取HEADERS配置信息
    def get_STATUS(self, name):
        self.name = self.readconfig.get('STATUS', name)
        return self.name

    # 获取HEADERS配置信息
    def get_DATABASE(self, name):
        self.name = self.readconfig.get('DATABASE', name)
        return self.name

    # 获取LOG日志路径
    # 获取HEADERS配置信息
    def get_basepath(self, name):
        self.name = self.readconfig.get('BASEPATH', name)
        return self.name

    def set_Header(self, name, value):
        '''
        :param name: 需要设置的key
        :param value: 需要设置的value
        :return:
        '''

        self.readconfig.set('HEADERS', name, value)
        self.readconfig.write(open(self.filepath, 'w'))

    # 获取发送邮件的配置信息
    def getEmail(self, name):
        return self.readconfig.get('SEND_EMAIL', name)

    # 获取火车票接口URL
    def get_train_url(self, name):
        return self.readconfig.get('TRAINURL', name)

    # 获取国内机票接口URL
    def get_flight_url(self, name):
        return self.readconfig.get('FLIGHTURL', name)

    # 获取国际机票接口URL
    def get_intflight_url(self, name):
        return self.readconfig.get('INTFLIGHTURL', name)

    # 获取表格名称
    def get_table_name(self, name):
        return self.readconfig.get('TABLENAME', name)

    # 获取测试状态
    def get_status(self, name):
        return self.readconfig.get('STATUS', name)

    # 获取前台接口URL
    def get_customer_url(self, name):
        return self.readconfig.get('CUSTOMERURL', name)


if __name__ == '__main__':
    r = readconfig()
    name = r.get_table_name("flight")
    print(name)
    print(readconfig().get_table_name("flight"))
