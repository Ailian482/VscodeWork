'''
字符串判断工具类
'''
import json
import operator

class StrUtil:

    def is_contain(str_one, str_two):
        '''
        		判断一个字符串是否再另外一个字符串中
        		str_one:查找的字符串
        		str_two：被查找的字符串
        		'''
        flag = None
        '''python2.6解决STR编码问题'''
        # if isinstance(str_one, unicode):
        #     str_one = str_one.encode('unicode-escape').decode('string_escape')
        return operator.eq(str_one, str_two)
        # if str_one in str_two:
        #     flag = True
        # else:
        #     flag = False
        # return flag

    def is_equal_dict(self, dict_one, dict_two):
        '''
        判断两个字典是否相等
        '''
        if isinstance(dict_one, str):
            dict_one = json.loads(dict_one)
        if isinstance(dict_two, str):
            dict_two = json.loads(dict_two)
        return operator.eq(dict_one, dict_two)

if __name__=='__main__':
    equal_result=StrUtil().is_equal_dict({'aaa':'apppaa'},{'aaa':'aaaa'})
    print(equal_result)
    equal_result_str=StrUtil.is_contain('pppp','pppp')
    print(equal_result_str)