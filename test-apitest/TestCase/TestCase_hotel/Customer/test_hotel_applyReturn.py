import unittest

from ApiData.UrlHeaderData import UrlHeaderData
from Common import Log, Base, operationExcel
from TestCase.TestCase_hotel.hotel_Customer import HotelProcess
from Utils import JsonPathUtil, JsonUtil
import time

'''
    订单退订
'''


class HotelApplyReturn(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger = Log.log("test_login").logger
        cls.url = "/front/v1/hotel/applyReturn "
        cls.jutil = JsonPathUtil.jsonpath_util()
        cls.Send = UrlHeaderData('Customer_url')

    def setUp(self):
        loginResponseData = Base.Base().Customer_login()
        self.token = self.jutil.get_values(loginResponseData, "token")[0]
        header = {'Content-Type': 'application/json', 'Authorization': ''}
        self.header = self.jutil.set_values(header, 'Authorization', "Bearer " + self.token)
        self.whole_data = JsonUtil.OperetionJson("Hotel_Customer_Json.json").get_data("applyReturn_Whole")
        self.part_data = JsonUtil.OperetionJson("Hotel_Customer_Json.json").get_data("applyReturn_part")
        self.data = ""
        self.test_result = "Fail"

    def tearDown(self):
        # # 写入
        row_number = int(self.id()[-2:])
        self.operateExcel = operationExcel.operationExcel("hotel_interface.xls", "applyReturn")
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("id"), row_number)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("描述"), self.Test_name)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("path"), self.url)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("header"), self.header)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("请求数据"), self.data)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("预期结果"), self.expected_result)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("实际结果"), self.response)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("测试结果"), self.test_result)
        pass

    # 用例1-- 订单退订（整单退订）
    def test_search_case01(self):
        """订单退订 --整单退订"""
        self.Test_name = '用例1 --订单退订 --整单退订'
        self.logger.info(self.Test_name)
        DependData, header = HotelProcess().preBill()
        time.sleep(10)
        self.data = self.jutil.set_values(self.whole_data, "orderId", DependData["data"])
        # 预期结果
        self.expected_result = "code = 0 / message=OK"
        # 实际结果
        response = self.Send.urlHeaderData(self.url, header, self.data)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 0)
        self.assertEqual(response.json()["message"], "OK")
        self.test_result = "Pass"

    # 用例2 -- 订单退订（部分退订）
    def test_search_case02(self):
        """订单退订 --部分退订"""
        self.Test_name = '用例2 --订单退订 --部分退订'
        self.logger.info(self.Test_name)
        DependData, header = HotelProcess().preBill()
        time.sleep(10)
        # 获取订单id详情信息
        orderData, header = HotelProcess().getOrderDetail(DependData['data'])
        # 获取订单id中的房间ID与对应dayid
        orderId = orderData["data"]["id"]
        first_roomId = self.jutil.get_values(orderData, "guests")[0][0]["subOrderId"]
        first_dayinfo = self.jutil.get_values(orderData, "guests")[0][0]["dayInfos"][0]["id"]
        second_roomId = self.jutil.get_values(orderData, "guests")[0][1]["subOrderId"]
        second_dayinfo = self.jutil.get_values(orderData, "guests")[0][1]["dayInfos"][0]["id"]
        # List 格式存储dayid信息
        list_firstday = [first_dayinfo]
        list_seconday = [second_dayinfo]
        # 写入相关订单信息数据，编写request请求
        self.jutil.set_values(self.part_data, "orderId", orderId)
        self.jutil.set_values((self.part_data["returnRooms"][0]), "subOrderId", first_roomId)
        self.jutil.set_values((self.part_data["returnRooms"][0]), "dayIds", list_firstday)
        self.jutil.set_values((self.part_data["returnRooms"][1]), "subOrderId", second_roomId)
        self.jutil.set_values((self.part_data["returnRooms"][1]), "dayIds", list_seconday)
        self.data = self.part_data
        # 预期结果
        self.expected_result = "code = 0 / message=OK"
        # 实际结果
        response = self.Send.urlHeaderData(self.url, header, self.part_data)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 0)
        self.assertEqual(response.json()["message"], "OK")
        self.test_result = "Pass"


if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(testsuite)
