import unittest
from Common.Base import Base
from Common import operationExcel, Log
from Utils import JsonPathUtil
from ApiData.UrlHeaderData import UrlHeaderData
from TestCase.TestCase_flight.FlightProcess import FlightProcess
from Config.ReadConfig import readconfig

status = str(readconfig().get_status("status"))

'''
国内机票退票任务处理成功
'''

class TestFlightTicketConfirm(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger = Log.log("test_login").logger
        cls.operateExcel = operationExcel.operationExcel(readconfig().get_table_name("flight"), "returnSuccess")
        cls.url = readconfig().get_flight_url("returnSuccess")

    def setUp(self) -> None:
        self.jutil = JsonPathUtil.jsonpath_util()
        self.data = FlightProcess().get_return_data()
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

    @unittest.skipIf(status, "产生数据：用例01--正常退票")
    def test_ticketConfirm_case01(self):
        """正常退票"""
        self.logger.info('国内机票退票成功--用例01--正常退票')
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue("ok",self.response.json()["data"])
        self.test_result = "PASS"

    def test_ticketConfirm_case02(self):
        """退票原因--空"""
        self.logger.info('国内机票退票成功--用例02--是否是同舱确认--空')
        self.data["actualReturnReason"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("请指定实际退票原因", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case03(self):
        """供应商退还的机建费--空"""
        self.logger.info('国内机票退票成功--用例03--供应商退还的机建费--空')
        self.data["passengerItems"][0]["airportFeeCost"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("请指定供应商退还的机建费", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case04(self):
        """供应商退还的机建费--非数字"""
        self.logger.info('国内机票退票成功--用例04--供应商退还的机建费--非数字')
        self.data["passengerItems"][0]["airportFeeCost"] = "AAA"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn('not a valid representation', str(self.message))
        self.test_result = "PASS"

    def test_ticketConfirm_case05(self):
        """供应商退还的机建费--负数"""
        self.logger.info('国内机票退票成功--用例05--供应商退还的机建费--负数')
        self.data["passengerItems"][0]["airportFeeCost"] = "-50"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("供应商退还的机建费不能为负数", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case06(self):
        """供应商退还的燃油费--空"""
        self.logger.info('国内机票退票成功--用例06--供应商退还的燃油费--空')
        self.data["passengerItems"][0]["oilFeeCost"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("请指定供应商退还的燃油费", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case07(self):
        """供应商退还的燃油费--非数字"""
        self.logger.info('国内机票退票成功--用例07--供应商退还的燃油费--非数字')
        self.data["passengerItems"][0]["oilFeeCost"] = "AAA"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn('not a valid representation', str(self.message))
        self.test_result = "PASS"

    def test_ticketConfirm_case08(self):
        """供应商退还的燃油费--负数"""
        self.logger.info('国内机票退票成功--用例08--供应商退还的燃油费--负数')
        self.data["passengerItems"][0]["oilFeeCost"] = "-10"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("供应商退还的燃油费不能为负数", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case09(self):
        """乘机人类型--空"""
        self.logger.info('国内机票退票成功--用例09--乘机人类型--空')
        self.data["passengerItems"][0]["passengerType"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("请指定乘机人类型", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case10(self):
        """乘机人类型--非字典数据"""
        self.logger.info('国内机票退票成功--用例10--乘机人类型--非字典数据')
        self.data["passengerItems"][0]["passengerType"] = "AAA"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn('value not one of declared Enum instance names: [Adult, Child, Infant]', str(self.message))
        self.test_result = "PASS"

    def test_ticketConfirm_case11(self):
        """退票手续费--空"""
        self.logger.info('国内机票退票成功--用例11--退票手续费--空')
        self.data["passengerItems"][0]["returnTicketFee"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("请指定退票手续费", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case12(self):
        """退票手续费--非数字"""
        self.logger.info('国内机票退票成功--用例12--退票手续费--非数字')
        self.data["passengerItems"][0]["returnTicketFee"] = "AAA"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn('not a valid representation', str(self.message))
        self.test_result = "PASS"

    def test_ticketConfirm_case13(self):
        """退票手续费--负数"""
        self.logger.info('国内机票退票成功--用例13--退票手续费--负数')
        self.data["passengerItems"][0]["returnTicketFee"] = "-20"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("退票手续费不能小于0", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case14(self):
        """退票手续费成本--空"""
        self.logger.info('国内机票退票成功--用例14--退票手续费成本--空')
        self.data["passengerItems"][0]["returnTicketFeeCost"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("请指定退票手续费成本", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case15(self):
        """退票手续费成本--非数字"""
        self.logger.info('国内机票退票成功--用例15--退票手续费成本--非数字')
        self.data["passengerItems"][0]["returnTicketFeeCost"] = "AAA"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn('not a valid representation', str(self.message))
        self.test_result = "PASS"

    def test_ticketConfirm_case16(self):
        """退票手续费成本--负数"""
        self.logger.info('国内机票退票成功--用例16--退票手续费成本--负数')
        self.data["passengerItems"][0]["returnTicketFeeCost"] = "-10"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("退票手续费成本不能小于0", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case17(self):
        """机票价格成本--空"""
        self.logger.info('国内机票退票成功--用例17--机票价格成本--空')
        self.data["passengerItems"][0]["ticketFeeCost"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("请指定供应商退机票费", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case18(self):
        """机票价格成本--非数字"""
        self.logger.info('国内机票退票成功--用例18--机票价格成本--非数字')
        self.data["passengerItems"][0]["ticketFeeCost"] = "AAA"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn('not a valid representation', str(self.message))
        self.test_result = "PASS"

    def test_ticketConfirm_case19(self):
        """机票价格成本--负数"""
        self.logger.info('国内机票退票成功--用例19--机票价格成本--负数')
        self.data["passengerItems"][0]["ticketFeeCost"] = "-100"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("供应商退机票费不能为负数", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case20(self):
        """退票系统使用费--非数字"""
        self.logger.info('国内机票退票成功--用例20--退票系统使用费--非数字')
        self.data["returnServiceFee"] = "AA"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn('not a valid representation', str(self.message))
        self.test_result = "PASS"

    def test_ticketConfirm_case21(self):
        """退票系统使用费--负数"""
        self.logger.info('国内机票退票成功--用例21--退票系统使用费--负数')
        self.data["returnServiceFee"] = "-20"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("退票系统使用费不能小于0", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case22(self):
        """任务id--空"""
        self.logger.info('国内机票退票成功--用例22--任务id--空')
        self.data["taskId"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("请传入正确的退票任务ID", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case23(self):
        """任务id--不存在"""
        self.logger.info('国内机票退票成功--用例23--任务id--不存在')
        self.data["taskId"] = "1111111111111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("不存在", str(self.response.json()["message"]))
        self.test_result = "PASS"


if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(testsuite)

