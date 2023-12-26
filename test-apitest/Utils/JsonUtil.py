import json
import os
from Config import ReadConfig

class OperetionJson():
    def __init__(self, file_name, file_path=None):
        if file_path is None:
            readconfig = ReadConfig.readconfig()
            dirpath = readconfig.get_basepath("base_path")
            self.file_path = os.path.join(dirpath, "TestFile", "JsonFile", file_name)
        else:
            self.file_path = os.path.join(file_path, file_name)
        self.data = self.read_data()

    # 读取json文件
    def read_data(self):
        with open(self.file_path, "r", encoding="utf-8") as fp:
            data = json.load(fp)
            return data

    # 根据关键字获取数据
    def get_data(self, id):
        return self.data[id]
        # try:
        #     jdata=self.data[id]
        # except KeyError as e:
        #     print('JSON找到该id：',e)
        # return jdata

    # 写json
    def write_data(self, data):
        with open(self.file_path, 'w') as fp:
            fp.write(json.dumps(data))


if __name__ == '__main__':
    opjson = OperetionJson("")
    print(opjson.get_data('data'))
