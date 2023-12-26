import re
import unittest
from Common.Base import Base
from Common import operationExcel, Log
from Utils import JsonUtil, JsonPathUtil
from TestCase.TestCase_flight.FlightProcess import FlightProcess
from ApiData.UrlHeaderData import UrlHeaderData
from Config.ReadConfig import readconfig

'''
国内机票提交改签申请
'''


class TestChangeFlight(unittest.TestCase):
    status = str(readconfig().get_status("status"))

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger = Log.log("test_login").logger
        cls.operateExcel = operationExcel.operationExcel(readconfig().get_table_name("flight"), "change")
        cls.url = readconfig().get_flight_url("change")
        login_response = Base().Customer_login()
        cls.api = UrlHeaderData()

    def setUp(self):
        # 获取token
        self.jutil = JsonPathUtil.jsonpath_util()
        login_response = Base().Customer_login()
        self.token = self.jutil.get_values(login_response, "token")[0]
        self.headers = {"Content-Type": "application/json", "Authorization": "Bearer {0}".format(self.token)}
        self.data = JsonUtil.OperetionJson("flight.json").get_data("changeFlight")
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

    # 构造改签接口的请求数据
    def get_change_data(self):
        flights_id, flight_id, bunk_id = FlightProcess().search_flight()
        order_id, ticket_id, header = FlightProcess().get_ticket_id()
        self.data["orderId"] = order_id
        self.data["ticketIds"] = ticket_id
        self.data["segment"]["bunkId"] = bunk_id
        self.data["segment"]["flightId"] = flight_id
        self.data["segment"]["flightsId"] = flights_id
        return self.data, header, order_id, ticket_id

    # 用例1--正常改签
    @unittest.skipIf(status=='200', "产生数据：用例1--正常改签")
    def test_change_case01(self):
        """正常改签"""
        self.logger.info('国内机票改签--用例01--正常改签')
        data, header, order_id, ticket_id = self.get_change_data()
        if not order_id:
            self.assertFalse("下单失败，订单ID为空")
        if not ticket_id:
            self.assertFalse("自动出票失败，不可退票")
        self.response = self.api.urlHeaderData(self.url, header, data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}",self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例2--改签票补差价--为空
    def test_change_case02(self):
        """改签票补差价--为空"""
        self.logger.info('国内机票改签--用例02--改签票补差价--为空')
        self.data["changePriceDiffer"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("改签票价补差", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例3--改签票补差价--数据无效
    def test_change_case03(self):
        """改签票补差价--数据无效"""
        self.logger.info('国内机票改签--用例03--改签票补差价--数据无效')
        self.data["changePriceDiffer"] = "`da"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.assertIn("not a valid representation", str(self.response.json()))
        self.test_result = "PASS"

    # 用例4--改签手续费--为空
    def test_change_case04(self):
        """改签手续费--为空"""
        self.logger.info('国内机票改签--用例04--改签手续费--为空')
        self.data["changeTicketFee"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("改签手续费", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例5--改签手续费--数据无效
    def test_change_case05(self):
        """改签手续费--数据无效"""
        self.logger.info('国内机票改签--用例05--改签手续费--数据无效')
        self.data["changeTicketFee"] = "`da"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.assertIn("not a valid representation", str(self.response.json()))
        self.test_result = "PASS"

    # 用例6--操作来源--Web
    @unittest.skipIf(status=='200', "产生数据：用例6--操作来源--Web")
    def test_change_case06(self):
        """操作来源--Web"""
        self.logger.info('国内机票改签--用例06--操作来源--Web')
        data, header, order_id, ticket_id = self.get_change_data()
        if not order_id:
            self.assertFalse("下单失败，订单ID为空")
        if not ticket_id:
            self.assertFalse("自动出票失败，不可退票")
        data["operateSource"] = "Web"
        self.response = self.api.urlHeaderData(self.url, header, data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{17}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例7--操作来源--Ios
    @unittest.skipIf(status=='200', "产生数据：用例7--操作来源--Ios")
    def test_change_case07(self):
        """操作来源--Ios"""
        self.logger.info('国内机票改签--用例07--操作来源--Ios')
        data, header, order_id, ticket_id = self.get_change_data()
        if not order_id:
            self.assertFalse("下单失败，订单ID为空")
        if not ticket_id:
            self.assertFalse("自动出票失败，不可退票")
        data["operateSource"] = "Ios"
        self.response = self.api.urlHeaderData(self.url, header, data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{17}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例8--操作来源--Android
    @unittest.skipIf(status=='200', "产生数据：用例8--操作来源--Android")
    def test_change_case08(self):
        """操作来源--Android"""
        self.logger.info('国内机票改签--用例08--操作来源--Ios')
        data, header, order_id, ticket_id = self.get_change_data()
        if not order_id:
            self.assertFalse("下单失败，订单ID为空")
        if not ticket_id:
            self.assertFalse("自动出票失败，不可退票")
        data["operateSource"] = "Android"
        self.response = self.api.urlHeaderData(self.url, header, data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{17}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例9--操作来源--Admin
    @unittest.skipIf(status=='200', "产生数据：用例9--操作来源--Admin")
    def test_change_case09(self):
        """操作来源--Admin"""
        self.logger.info('国内机票改签--用例09--操作来源--Admin')
        data, header, order_id, ticket_id = self.get_change_data()
        if not order_id:
            self.assertFalse("下单失败，订单ID为空")
        if not ticket_id:
            self.assertFalse("自动出票失败，不可退票")
        data["operateSource"] = "Admin"
        self.response = self.api.urlHeaderData(self.url, header, data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{17}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例10--操作来源--空
    @unittest.skipIf(status=='200', "产生数据：用例10--操作来源--空--未校验")
    def test_change_case10(self):
        """操作来源--空"""
        self.logger.info('国内机票改签--用例10--操作来源--空')
        data, header, order_id, ticket_id = self.get_change_data()
        if not order_id:
            self.assertFalse("下单失败，订单ID为空")
        if not ticket_id:
            self.assertFalse("自动出票失败，不可退票")
        data["operateSource"] = ""
        self.response = self.api.urlHeaderData(self.url, header, data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定操作来源", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例11--操作来源--数据无效
    @unittest.skipIf(status=='200', "产生数据：用例11--操作来源--数据非法--未校验")
    def test_change_case11(self):
        """操作来源--数据非法"""
        self.logger.info('国内机票改签--用例11--操作来源--数据非法')
        data, header, order_id, ticket_id = self.get_change_data()
        if not order_id:
            self.assertFalse("下单失败，订单ID为空")
        if not ticket_id:
            self.assertFalse("自动出票失败，不可退票")
        data["operateSource"] = "123"
        self.response = self.api.urlHeaderData(self.url, header, data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例12--订单号--空
    def test_change_case12(self):
        """订单号--空"""
        self.logger.info('国内机票改签--用例12--订单号--空')
        self.data["orderId"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("For input string: """, str(self.response.json()))
        self.test_result = "PASS"

    # 用例13--订单号--不正确
    def test_change_case13(self):
        """订单号--不正确"""
        self.logger.info('国内机票改签--用例13--订单号--不正确')
        self.data["orderId"] = "11111111111aaaaaa"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("For input string: """, str(self.response.json()))
        self.test_result = "PASS"

    # 用例14--票号--空
    def test_change_case14(self):
        """票号--空"""
        self.logger.info('国内机票改签--用例14--票号--空')
        self.data["ticketIds"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("For input string", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例15--票号--不正确
    def test_change_case15(self):
        """票号--不正确"""
        self.logger.info('国内机票改签--用例15--票号--不正确')
        self.data["ticketIds"] = "11111111111aaaaaa"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("For input string: """, str(self.response.json()))
        self.test_result = "PASS"

    # 用例16--舱位id--空
    def test_change_case16(self):
        """舱位id--空"""
        self.logger.info('国内机票改签--用例16--舱位id--空')
        self.data["segment"]["bunkId"] = ''
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("For input string", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例17--舱位id--不正确
    def test_change_case17(self):
        """舱位id--不正确"""
        self.logger.info('国内机票改签--用例17--舱位id--不正确')
        self.data["segment"]["bunkId"] = '111111111111111111111'
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("For input string", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例18--航班id--空
    def test_change_case18(self):
        """航班id--空"""
        self.logger.info('国内机票改签--用例18--航班id--空')
        self.data["segment"]["flightId"] = ''
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("For input string", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例19--航班id--不正确
    def test_change_case19(self):
        """航班id--不正确"""
        self.logger.info('国内机票改签--用例19--航班id--不正确')
        self.data["segment"]["flightId"] = '111111111111111111'
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("For input string", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例20--航班列表id--空
    def test_change_case20(self):
        """航班列表id--空"""
        self.logger.info('国内机票改签--用例20--航班列表id--空')
        self.data["segment"]["flightsId"] = ''
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("For input string", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例21--航班列表id--空
    def test_change_case21(self):
        """航班列表id--空"""
        self.logger.info('国内机票改签--用例21--航班列表id--不正确')
        self.data["segment"]["flightsId"] = '11111111111111111'
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("For input string", str(self.response.json()["message"]))
        self.test_result = "PASS"


if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(testsuite)


