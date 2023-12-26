#!/usr/bin/env python3
# _*_ coding: utf-8 _*_   

# 导入系统模块
import datetime
import sys
import os
import unittest
import time
import requests
from BeautifulReport import BeautifulReport

# 导入项目中依赖模块
from Common.Email import send_email
from Common import Log
from Config.ReadConfig import readconfig
from Utils.JsonPathUtil import jsonpath_util

'''
定义Run()类及其方法
'''
class Run:
    def __init__(self):
        self.logger = Log.log('run_main').logger
        # Get the work directory from the configuration.
        self.dirpath = readconfig().get_basepath("base_path")
        # Auto test report directory
        self.report_path = os.path.join(self.dirpath, 'Report/')
        # Notify users list
        # user_list = ["chenjunan@tehang.com", "tanchunjie@tehang.com", "zhengwenpei@tehang.com", "liulang@tehang.com"]
        self.user_list = "chenjunan@tehang.com, tanchunjie@tehang.com, zhengwenpei@tehang.com, liulang@tehang.com"

    def run_test(self):
        now_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        # Get test case methods
        test_suite = unittest.defaultTestLoader.discover('./TestCase/', pattern='test*.py')
        end_Time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Run the test cases
        result = BeautifulReport(test_suite)
        result.report(filename='自动化测试报告%s' % now_time, description='特航接口自动化测试报告', report_dir = self.report_path)
        #总用例数
        totol_tests = result.fields['testAll']
        #跳过用例数
        skip_tests = result.fields['testSkip']
        #失败用例数
        fail_tests = result.fields['testFail']
        #错误用例数
        error_tests = result.error_count
        #通过用例数
        success_tests = result.fields['testPass']
        #运行总时间
        totalTime =result.fields['totalTime']
        self.logger.info("================运行完成，请查看结果===============")
        context = "测试用例执行结束:%s  \n" % end_Time + \
                         "**********开始打印结果********** \n" +\
                         "总运行测试用例数:%d \n" % totol_tests + \
                            "通过测试用例数:%d \n" % success_tests + \
                          "跳过用例数:%d \n" % skip_tests + \
                          '失败的测试用例数:%d \n' % fail_tests +\
                         "错误用例数:%d \n" % error_tests +\
                         "运行总时间:%s\n" % totalTime
        # send_email().send_mail(user_list, u'自动化测试报告', context)
        return result

    # def get_net_status(self)
    #     # 获取前台网关状态
    #     customer_basehttp = SendHttp("baseurl1")
    #     customer_basehttp.set_url("")
    #     customer_response = customer_basehttp.http_post()
    #     # 获取后台网关状态
    #     staff_basehttp = SendHttp("staffurl1")
    #     staff_basehttp.set_url("")
    #     staff_response = staff_basehttp.http_post()
    #     if customer_response.status_code == 404 & staff_response.status_code == 404:
    #         return True
    #     else:
    #         return False


if __name__ == '__main__':
    r = Run()
    r.run_test()
    # Run().run_test()
    # consul_response = requests.get('http://20.20.20.90:30196/v1/health/node/consul-0')
    # consconsul_status=[]
    # straa =''
    # for serve in consul_response.json():
    #     # print('serve:', jsonpath_util().get_values(serve, 'ServiceName'))
    #     # print('Status:', jsonpath_util().get_values(serve, 'Status'))
    #     servelist = jsonpath_util().get_values(serve, 'ServiceName')
    #     Statuslist = jsonpath_util().get_values(serve, 'Status')
    #     consconsul_status.append(servelist+Statuslist)
    # for items in consconsul_status:
    #      straa =straa+'服务状态:'+str(items) + '\n'
    # # print(straa)
    # context = "测试用例开始执行结束:%s  \n" % 'nowTime' + \
    #            "**********检测consul服务********** \n" + \
    #            straa
    #
    # print(context)
# 

