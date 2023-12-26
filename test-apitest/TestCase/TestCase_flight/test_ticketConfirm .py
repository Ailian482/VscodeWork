import unittest
from Common.Base import Base
from Common import operationExcel, Log
from Utils import JsonPathUtil
from ApiData.UrlHeaderData import UrlHeaderData
from TestCase.TestCase_flight.FlightProcess import FlightProcess
from Config.ReadConfig import readconfig

status = str(readconfig().get_status("status"))

'''
国内机票出票确认
'''

class TestFlightTicketConfirm(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger = Log.log("test_login").logger
        cls.operateExcel = operationExcel.operationExcel(readconfig().get_table_name("flight"), "ticketConfirm")
        cls.url = readconfig().get_flight_url("ticketConfirm")

    def setUp(self) -> None:
        self.jutil = JsonPathUtil.jsonpath_util()
        self.data = FlightProcess().get_confirm_data()
        login_response = Base().Staff_login()
        self.api = UrlHeaderData('Staff_url')
        self.token = self.jutil.get_values(login_response, "token")[0]
        self.headers = {"Content-Type": "application/json", "Authorization": "Bearer {0}".format(self.token)}
        self.test_result = "FAIL"
        self.message = ""
        self.response_code = 0

    def tearDown(self) -> None:
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

    @unittest.skipIf(status, "产生数据：用例01--正常出票")
    def test_ticketConfirm_case01(self):
        """正常出票"""
        self.logger.info('国内机票出票--用例01--正常出票')
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue("ok",self.response.json()["data"])
        self.test_result = "PASS"

    def test_ticketConfirm_case02(self):
        """是否是同舱确认--空"""
        self.logger.info('国内机票出票--用例02--是否是同舱确认--空')
        self.data["sameBunk"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定是否同舱确认", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case03(self):
        """是否是同舱确认--非bool值"""
        self.logger.info('国内机票出票--用例03--是否是同舱确认--非bool值')
        self.data["sameBunk"] = "ni"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn('only "true" or "false" recognized', str(self.message))
        self.test_result = "PASS"

    def test_ticketConfirm_case04(self):
        """任务Id--空"""
        self.logger.info('国内机票出票--用例04--任务Id--空')
        self.data["taskId"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("请传入正确的任务ID", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case05(self):
        """任务Id--不正确"""
        self.logger.info('国内机票出票--用例05--任务Id--不正确')
        self.data["taskId"] = 121243434
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("不存在", str(self.response.json()))
        self.test_result = "PASS"

    def test_ticketConfirm_case06(self):
        """机建费成本--空"""
        self.logger.info('国内机票出票--用例06--机建费成本--空')
        self.data["tickets"][0]["airportFeeCost"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn("内部数据库错误", str(self.message))
        self.test_result = "PASS"

    def test_ticketConfirm_case07(self):
        """机建费成本--非数字"""
        self.logger.info('国内机票出票--用例07--机建费成本--非数字')
        self.data["tickets"][0]["airportFeeCost"] = "er"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn("not a valid representation", str(self.message))
        self.test_result = "PASS"

    def test_ticketConfirm_case08(self):
        """燃油费成本--空"""
        self.logger.info('国内机票出票--用例08--燃油费成本--空')
        self.data["tickets"][0]["oilFeeCost"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn("内部数据库错误", str(self.message))
        self.test_result = "PASS"

    def test_ticketConfirm_case09(self):
        """燃油费成本--非数字"""
        self.logger.info('国内机票出票--用例09--燃油费成本--非数字')
        self.data["tickets"][0]["oilFeeCost"] = "er"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn("not a valid representation", str(self.message))
        self.test_result = "PASS"

    def test_ticketConfirm_case10(self):
        """供应商代码--空"""
        self.logger.info('国内机票出票--用例10--后返佣金比例--负数')
        self.data["tickets"][0]["supplier"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定机票", str(self.response.json()))
        self.test_result = "PASS"

    def test_ticketConfirm_case11(self):
        """机票费成本--空"""
        self.logger.info('国内机票出票--用例11--机票费成本--空')
        self.data["tickets"][0]["ticketFeeCost"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn("内部数据库错误", str(self.message))
        self.test_result = "PASS"

    def test_ticketConfirm_case12(self):
        """机票费成本--非数字"""
        self.logger.info('国内机票出票--用例12--机票费成本--非数字')
        self.data["tickets"][0]["ticketFeeCost"] = "qwr"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn("not a valid representation", str(self.message))
        self.test_result = "PASS"

    def test_ticketConfirm_case13(self):
        """机票id--空"""
        self.logger.info('国内机票出票--用例13--机票id--空')
        self.data["tickets"][0]["ticketId"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("传入的机票ID格式不正确", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case14(self):
        """机票id--不存在"""
        self.logger.info('国内机票出票--用例14--机票id--不存在')
        self.data["tickets"][0]["ticketId"] = "11111111111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("不存在", str(self.message))
        self.test_result = "PASS"

if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(testsuite)

