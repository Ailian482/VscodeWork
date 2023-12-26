import requests
import jsonpath
import json
"""
遍历swagger接口文档

"""
class swagerlist:
    #获取swagger全部接口
    def get_swagger(self):
        i=0         #全量统计接口数量
        response = requests.get('http://172.19.1.103:30866/v2/api-docs?group=Default')
        result=jsonpath.jsonpath(response.json(),'$.paths')     #获取paths下所有接口路径，返回为list
        for z in result:
            # str =key
            str=z
            print(type(str))
        for key in str:
            print(key)
            i=i+1

        print(i)

if __name__== "__main__":
    swagerlist().get_swagger()
