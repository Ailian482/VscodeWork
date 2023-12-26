import unittest

from ApiData.UrlHeaderData import UrlHeaderData
from Common import Log, Base, operationExcel
from Utils import JsonPathUtil, JsonUtil
from datetime import date, timedelta

'''
    酒店详情接口
'''


class HotelGetHotelDetail(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger = Log.log("test_login").logger
        cls.jutil = JsonPathUtil.jsonpath_util()
        cls.data = JsonUtil.OperetionJson("Hotel_Customer_Json.json").get_data("getHotelDetail")
        cls.url = "/front/v1/hotel/getHotelDetail"
        cls.Send = UrlHeaderData('Customer_url')

    def setUp(self):
        loginResponseData = Base.Base().Customer_login()
        self.token = self.jutil.get_values(loginResponseData, "token")[0]
        header = {'Content-Type': 'application/json', 'Authorization': ''}
        self.header = self.jutil.set_values(header, 'Authorization', "Bearer " + self.token)
        self.test_result = "Fail"

    def tearDown(self):
        # 写入
        row_number = int(self.id()[-2:])
        self.operateExcel = operationExcel.operationExcel("hotel_interface.xls", "getHotelDetail")
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("id"), row_number)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("描述"), self.Test_name)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("path"), self.url)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("header"), self.header)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("请求数据"), self.data)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("预期结果"), self.expected_result)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("实际结果"), self.response)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("测试结果"), self.test_result)
        pass

    # 用例1--正常查询
    def test_search_case01(self):
        """酒店详情 --正常查询"""
        self.Test_name = '用例1 --酒店详情 --正常查询'
        self.logger.info(self.Test_name)
        self.data["checkInDate"] = (date.today()).strftime("%Y-%m-%d")
        self.data["checkOutDate"] = (date.today() + timedelta(days=+3)).strftime("%Y-%m-%d")
        # 预期结果
        self.expected_result = "code = 0 / Data ：深圳"
        # 实际结果
        response = self.Send.urlHeaderData(self.url, self.header, self.data)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 0, "返回的code不是0，是{0}".format(response.json()["code"]))
        # self.assertEqual(response.json()["data"]["hotelCode"], "M588936",
        #                  "返回错误，返回的hotelCode:{0}".format(response.json()["code"])
        self.test_result = "Pass"

    # 用例2 -- 登录态校验
    def test_search_case02(self):
        """酒店详情 --登录态校验"""
        self.Test_name = '用例2 --酒店详情 --登录态校验'
        self.logger.info(self.Test_name)
        self.data["checkInDate"] = (date.today()).strftime("%Y-%m-%d")
        self.data["checkOutDate"] = (date.today() + timedelta(days=+1)).strftime("%Y-%m-%d")
        header = {'Content-Type': 'application/json'}
        # 预期结果
        self.expected_result = "code = 401 / Data：尚未登陆"
        # 实际结果
        response = self.Send.urlHeaderData(self.url, header, self.data)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 401, "返回的code不是401，是{0}".format(response.json()["code"]))
        self.assertIn("您尚未登录", str(response.json()["message"]))
        self.test_result = "Pass"

    # 用例3 -- 入住时间过期
    def test_search_case03(self):
        """酒店详情 --入住时间过期"""
        self.Test_name = '用例3 --酒店详情 --入住时间过期'
        self.logger.info(self.Test_name)
        self.data["checkInDate"] = (date.today() + timedelta(days=-2)).strftime("%Y-%m-%d")
        self.data["checkOutDate"] = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
        # 预期结果
        self.expected_result = "code = 1 / Data：查无数据"
        # 实际结果
        response = self.Send.urlHeaderData(self.url, self.header, self.data)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 1, "返回的code不是1，是{0}".format(response.json()["code"]))
        self.assertIn("查无数据", str(response.json()["message"]))
        self.test_result = "Pass"

    # 用例4 -- 入离住时间过长（1个月）
    def test_search_case04(self):
        """酒店详情 --入离住时间过长"""
        self.Test_name = '用例4 --酒店详情 --入离住时间过长'
        self.logger.info(self.Test_name)
        self.data["checkInDate"] = (date.today()).strftime("%Y-%m-%d")
        self.data["checkOutDate"] = (date.today() + timedelta(days=+31)).strftime("%Y-%m-%d")
        # 预期结果
        self.expected_result = "code = 0 / Data：深圳"
        # 实际结果
        response = self.Send.urlHeaderData(self.url, self.header, self.data)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 0, "返回的code不是0，是{0}".format(response.json()["code"]))
        self.assertEqual(response.json()["message"], "OK")
        self.test_result = "Pass"

    # 用例5 -- 入住日期大于离店日期
    def test_search_case05(self):
        """酒店详情 --入住日期大于离店日期"""
        self.Test_name = '用例5 --酒店详情 --入住日期大于离店日期'
        self.logger.info(self.Test_name)
        self.data["checkInDate"] = (date.today()).strftime("%Y-%m-%d")
        self.data["checkOutDate"] = (date.today() + timedelta(days=-2)).strftime("%Y-%m-%d")
        # 预期结果
        self.expected_result = "code = 1 / 查无数据"
        # 实际结果
        response = self.Send.urlHeaderData(self.url, self.header, self.data)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 1, "返回的code不是1，是{0}".format(response.json()["code"]))
        self.assertIn("查无数据", str(response.json()["message"]))
        self.test_result = "Pass"

    # 用例6 -- 入离住日期相同
    def test_search_case06(self):
        """酒店详情 --入离住日期相同"""
        self.Test_name = '用例6 --酒店详情 --入离住日期相同'
        self.logger.info(self.Test_name)
        self.data["checkInDate"] = (date.today()).strftime("%Y-%m-%d")
        self.data["checkOutDate"] = (date.today()).strftime("%Y-%m-%d")
        # 预期结果
        self.expected_result = "code = 1 / 查无数据"
        # 实际结果
        response = self.Send.urlHeaderData(self.url, self.header, self.data)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 1, "返回的code不是1，是{0}".format(response.json()["code"]))
        self.assertIn("查无数据", str(response.json()["message"]))
        self.test_result = "Pass"

    # 用例7 -- 入离日期为空
    def test_search_case07(self):
        """酒店详情 --入离日期为空"""
        self.Test_name = '用例7 --酒店详情 --入离日期为空'
        self.logger.info(self.Test_name)
        self.data["checkInDate"] = ""
        self.data["checkOutDate"] = ""
        # 预期结果
        self.expected_result = "code = 98 / Data：不能为空"
        # 实际结果
        response = self.Send.urlHeaderData(self.url, self.header, self.data)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 98, "返回的code不是98，是{0}".format(response.json()["code"]))
        self.test_result = "Pass"

    # 用例8 -- 酒店(hotelcode)信息为空
    def test_search_case08(self):
        """酒店详情 --酒店(hotelcode)信息为空"""
        self.Test_name = '用例8 --酒店详情 --酒店(hotelcode)信息为空'
        self.logger.info(self.Test_name)
        self.data["checkInDate"] = (date.today()).strftime("%Y-%m-%d")
        self.data["checkOutDate"] = (date.today() + timedelta(days=+1)).strftime("%Y-%m-%d")
        self.data["hotelCode"] = ""
        # 实际结果
        response = self.Send.urlHeaderData(self.url, self.header, self.data)
        self.response = response.json()
        # 预期结果
        self.expected_result = "code = 98 / Data：不能为空"
        # 断言
        self.assertEqual(response.json()["code"], 98, "返回的code不是98，是{0}".format(response.json()["code"]))
        self.test_result = "Pass"


if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(testsuite)
