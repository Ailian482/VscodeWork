#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import requests
import schedule
import time
from Common import Log
from Common.BaseHttp import SendHttp
from Utils.JsonPathUtil import jsonpath_util
from run import Run

def job():
    logger = Log.log('schedule_task').logger
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 获取前台网关状态
    customer_basehttp = SendHttp("Customer_url")
    customer_basehttp.set_url("")
    customer_response = customer_basehttp.http_post()
    # 获取后台网关状态
    staff_basehttp = SendHttp("Staff_url")
    staff_basehttp.set_url("")
    staff_response = staff_basehttp.http_post()
    # 判断consul服务健康
    consul_response = requests.get('http://20.20.20.90:30196/v1/health/node/consul-0')
    consconsul_status=[]
    straa =''
    for serve in consul_response.json():
        # print('serve:', jsonpath_util().get_values(serve, 'ServiceName'))
        # print('Status:', jsonpath_util().get_values(serve, 'Status'))
        servelist = jsonpath_util().get_values(serve, 'ServiceName')
        Statuslist = jsonpath_util().get_values(serve, 'Status')
        consconsul_status.append(servelist+Statuslist)
    for items in consconsul_status:
        straa = straa + '服务状态:' + str(items) + '\n'

    #判断tmc存活，执行用例
    if 'tmc-services' in servelist:
    # if(customer_response.status_code == 404 & staff_response.status_code == 404):
        logger.info("测试用例开始执行：" + nowTime)
        send_msg("测试用例开始执行:%s  \n" % nowTime + \
               "**********检测consul服务********** \n" + \
               straa
                 )
        test_result =Run().run_test()
        # 总用例数
        totol_tests = test_result.fields['testAll']
        # 跳过用例数
        skip_tests = test_result.fields['testSkip']
        # 失败用例数
        fail_tests = test_result.fields['testFail']
        # 错误用例数
        error_tests = test_result.error_count
        # 通过用例数
        success_tests = test_result.fields['testPass']
        # 运行总时间
        totalTime = test_result.fields['totalTime']
        end_Time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        send_msg("测试用例执行结束:%s  \n" % end_Time + \
                          "**********开始打印结果********** \n" + \
                          "总运行测试用例数:%d \n" % totol_tests + \
                          "通过测试用例数:%d \n" % success_tests + \
                          "跳过用例数:%d \n" % skip_tests + \
                          '失败的测试用例数:%d \n' % fail_tests + \
                          "错误用例数:%d \n" % error_tests + \
                          "运行总时间:%s\n" % totalTime
        )

    else:
        send_msg("服务错误，中断测试")
        logger.error("服务错误，中断测试")
        # raise ConnectionError("网关错误，中断测试")


def send_msg(msg):
    data = {"msgtype": "text", "text": {"content": msg}}
    waring_basehttp = SendHttp('wx_url')
    waring_basehttp.set_url(
        '/cgi-bin/webhook/send?key=55e178d6-9132-4dbc-a251-d34931063fd3')
    waring_basehttp.set_headers({'Content-Type': 'application/json'})
    waring_basehttp.set_data(data)
    waring_response = waring_basehttp.http_post()

#每8分钟执行一次
# schedule.every(8).minutes.do(job)
#每天固定时间执行一次
schedule.every().day.at("06:30").do(job)
#每4小时执行一次
# schedule.every(4).hours.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
