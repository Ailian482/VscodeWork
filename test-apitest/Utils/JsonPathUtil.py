import jsonpath
from Common.Base import Base
from Utils import JsonUtil


class jsonpath_util:

    def get_values(self, json_obj, key):
        '''根据json获取key的values'''
        values = None
        if isinstance(json_obj, dict):
            values = jsonpath.jsonpath(json_obj, '$..%s' % (key))
            return values
        else:
            values = jsonpath.jsonpath(json_obj.json(), '$..%s' % (key))
            return values

    def set_values(self, dic_json, key, value):  # 根据key写入value
        if isinstance(dic_json, dict):
            for keys in dic_json:
                if keys == key:
                    dic_json[keys] = value
                elif isinstance(dic_json[keys], dict):
                    self.set_values(dic_json[keys], key, value)
        return dic_json

    def set_values_list(self, dic_json, Key, Value):  # 根据Key列表，写入value列表。批量修改。
        for index in range(len(Key)):
            if isinstance(dic_json, dict):
                for keys in dic_json:
                    if keys == Key[index]:
                        dic_json[keys] = Value[index]
                    elif isinstance(dic_json[keys], dict):
                        self.set_values(dic_json[keys], Key[index], Value[index])
        return dic_json


if __name__ == "__main__":
    pass
