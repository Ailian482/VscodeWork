import unittest
from Common.Base import Base
from Common import operationExcel, Log
from Utils import JsonUtil, JsonPathUtil
from TestCase.TestCase_flight.FlightProcess import FlightProcess
from ApiData.UrlHeaderData import UrlHeaderData
from Config.ReadConfig import readconfig


'''
国内机票提交退票申请
'''
status = str(readconfig().get_status("status"))


class TestReturnFlight(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.logger = Log.log("test_login").logger
        cls.url = readconfig().get_flight_url("return")
        cls.operateExcel = operationExcel.operationExcel(readconfig().get_table_name("flight"), "return")

    def setUp(self):
        # 获取token
        self.jutil = JsonPathUtil.jsonpath_util()
        login_response = Base().Customer_login()
        self.api = UrlHeaderData()
        self.token = self.jutil.get_values(login_response, "token")[0]
        self.headers = {"Content-Type": "application/json", "Authorization": "Bearer {0}".format(self.token)}
        self.data = JsonUtil.OperetionJson("flight.json").get_data("returnFlight")
        self.test_result = "FAIL"
        self.message = ""
        self.response_code = 0

    def tearDown(self):
        col_num1 = self.operateExcel.get_col_name_num("实际结果")
        col_num2 = self.operateExcel.get_col_name_num("测试结果")
        row_number = int(self.id()[-2:])

        try:
            self.operateExcel.write_value(row_number, col_num1, self.response.json())
        except Exception as e:
            self.logger.error(repr(e))
            self.operateExcel.write_value(row_number, col_num1, "写入失败：%s" %repr(e))
        self.operateExcel.write_value(row_number, col_num2, self.test_result)

    def get_error(self, response):
        if self.response.json().__contains__("code"):
            self.response_code = self.response.json()["code"]
        if self.response.json().__contains__("message"):
            self.message = response.json()["message"]
        else:
            self.message = response.json()

    # 用例1--正常退票(订单号票号均正确)
    @unittest.skipIf(status=='200', "产生数据：用例1--正常退票(订单号票号均正确)")
    def test_return_case01(self):
        """正常退票(订单号票号均正确)"""
        self.logger.info('国内机票退票--用例01--正常退票（订单号和票号均正确）')
        order_id, ticket_id, header = FlightProcess().get_ticket_id()
        if not order_id:
            self.assertFalse("下单失败，订单ID为空")
        if not ticket_id:
            self.assertFalse("自动出票失败，不可退票")
        self.data['orderId'] = order_id
        self.data['ticketIds'] = ticket_id
        self.response = self.api.urlHeaderData(self.url, header, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertEqual(self.response.json()["message"], "OK", )
        self.test_result = "PASS"

    # 用例2--订单号-空
    def test_return_case02(self):
        """订单号--空"""
        self.logger.info('国内机票退票--用例02--订单号为空')
        self.data['orderId'] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定订单id", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例3--订单号--不存在
    def test_return_case03(self):
        """订单号--不存在"""
        self.logger.info('国内机票退票--用例03--订单号不存在')
        self.data['orderId'] = "235325462314335"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("不存在", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例4--票号-为空  ----票号为空能成功
    @unittest.skipIf(status=='200', "产生数据：用例4--票号-为空  ----票号为空能成功")
    def test_return_case04(self):
        """票号--为空"""
        self.logger.info('国内机票退票--用例04--票号为空')
        self.data['ticketIds'] = ""
        response, order_id, header = FlightProcess().pay_flight()
        if not response:
            self.assertFalse("下单失败，订单ID为空")
        self.data['orderId'] = order_id
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("不存在", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例5--票号-不存在
    @unittest.skipIf(status=='200', "产生数据：用例5--票号-不存在")
    def test_return_case05(self):
        """票号--不存在"""
        self.logger.info('国内机票退票--用例05--票号不存在')
        self.data['ticketIds'] = "132869405225914368"
        response, order_id, header = FlightProcess().pay_flight()
        if not response:
            self.assertFalse("下单失败，订单ID为空")
        self.data['orderId'] = order_id
        self.response = self.api.urlHeaderData(self.url, header, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("不存在", str(self.response.json()["message"]))
        self.test_result = "PASS"


if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(testsuite)


