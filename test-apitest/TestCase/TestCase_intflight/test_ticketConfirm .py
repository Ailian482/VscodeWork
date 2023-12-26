import re
import unittest
from Common.Base import Base
from Common import operationExcel, Log
from Utils import JsonPathUtil, JsonUtil
from ApiData.UrlHeaderData import UrlHeaderData
from TestCase.TestCase_intflight.IntflightProcess import IntflightProcess
from Config.ReadConfig import readconfig

'''
国际机票出票确认
'''

status = str(readconfig().get_status("status"))

class TestIntflightTicketConfirm(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger = Log.log("test_login").logger
        cls.operateExcel = operationExcel.operationExcel(readconfig().get_table_name("intflight"), "ticketConfirm")
        cls.url = readconfig().get_intflight_url("ticketConfirm")

    def setUp(self) -> None:
        self.jutil = JsonPathUtil.jsonpath_util()
        self.data = IntflightProcess().get_confirm_data()
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

    def test_ticketConfirm_case01(self):
        """正常出票"""
        self.logger.info('国际机票出票--用例01--正常出票')
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue("ok",self.response.json()["data"])
        self.test_result = "PASS"

    def test_ticketConfirm_case02(self):
        """前返佣金比例--空"""
        self.logger.info('国际机票出票--用例02--前返佣金比例--空')
        self.data["priceItems"][0]["commissionPercent"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定前返佣金比例", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case03(self):
        """前返佣金比例--非数字"""
        self.logger.info('国际机票出票--用例03--前返佣金比例--非数字')
        self.data["priceItems"][0]["commissionPercent"] = "nihao"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn("not a valid representation", str(self.message))
        self.test_result = "PASS"

    def test_ticketConfirm_case04(self):
        """前返佣金比例--负数"""
        self.logger.info('国际机票出票--用例04--前返佣金比例--负数')
        self.data["priceItems"][0]["commissionPercent"] = "-0.1"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("前返佣金比例无效", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case05(self):
        """其他费用--空"""
        self.logger.info('国际机票出票--用例05--其他费用--空')
        self.data["priceItems"][0]["others"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定其他费用", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case06(self):
        """其他费用--非数字"""
        self.logger.info('国际机票出票--用例06--其他费用--非数字')
        self.data["priceItems"][0]["others"] = "aa"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn("not a valid representation", str(self.message))
        self.test_result = "PASS"

    def test_ticketConfirm_case07(self):
        """票号对应乘机人id--空"""
        self.logger.info('国际机票出票--用例07--票号对应乘机人id--空')
        self.data["priceItems"][0]["passengerId"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("乘机人id不能为空", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case08(self):
        """后返佣金比例--空"""
        self.logger.info('国际机票出票--用例08--后返佣金比例--空')
        self.data["priceItems"][0]["returnCommissionPercent"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定后返佣金比例", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case09(self):
        """后返佣金比例--非数字"""
        self.logger.info('国际机票出票--用例09--后返佣金比例--非数字')
        self.data["priceItems"][0]["returnCommissionPercent"] = "nihao"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn("not a valid representation", str(self.message))
        self.test_result = "PASS"

    def test_ticketConfirm_case10(self):
        """后返佣金比例--负数"""
        self.logger.info('国际机票出票--用例10--后返佣金比例--负数')
        self.data["priceItems"][0]["returnCommissionPercent"] = "-0.1"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("后返佣金比例无效", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case11(self):
        """票号对应的航段id--空"""
        self.logger.info('国际机票出票--用例11--票号对应的航段id--空')
        self.data["priceItems"][0]["segmentIds"] = []
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定航段id列表", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case12(self):
        """税费--空"""
        self.logger.info('国际机票出票--用例12--税费--空')
        self.data["priceItems"][0]["tax"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定税费", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case13(self):
        """税费--非数字"""
        self.logger.info('国际机票出票--用例13--税费--非数字')
        self.data["priceItems"][0]["tax"] = "nihao"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn("not a valid representation", str(self.message))
        self.test_result = "PASS"

    def test_ticketConfirm_case14(self):
        """税费--负数"""
        self.logger.info('国际机票出票--用例14--税费--负数')
        self.data["priceItems"][0]["tax"] = "-20"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("税费无效", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case15(self):
        """到达城市代码--空"""
        self.logger.info('国际机票出票--用例15--票面价--空')
        self.data["priceItems"][0]["ticketFee"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定票面价", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case16(self):
        """票面价--非数字"""
        self.logger.info('国际机票出票--用例16--票面价--非数字')
        self.data["priceItems"][0]["ticketFee"] = "nihao"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn("not a valid representation", str(self.message))
        self.test_result = "PASS"

    def test_ticketConfirm_case17(self):
        """票面价--负数"""
        self.logger.info('国际机票出票--用例17--票面价--负数')
        self.data["priceItems"][0]["ticketFee"] = "-100"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("票面价无效", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case18(self):
        """无奖励票价--空"""
        self.logger.info('国际机票出票--用例18--无奖励票价--空')
        self.data["priceItems"][0]["ticketFeeWithoutReward"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定无奖励票价", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case19(self):
        """无奖励票价--非数字"""
        self.logger.info('国际机票出票--用例19--无奖励票价--非数字')
        self.data["priceItems"][0]["ticketFeeWithoutReward"] = "nihao"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn("not a valid representation", str(self.message))
        self.test_result = "PASS"

    def test_ticketConfirm_case20(self):
        """无奖励票价--负数"""
        self.logger.info('国际机票出票--用例20--无奖励票价--负数')
        self.data["priceItems"][0]["ticketFeeWithoutReward"] = "-100"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("无奖励票价无效", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case21(self):
        """票号--空"""
        self.logger.info('国际机票出票--用例21--票号--空')
        self.data["priceItems"][0]["ticketNo"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("票号不能为空", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case22(self):
        """供应商代码--空"""
        self.logger.info('国际机票出票--用例22--供应商代码--空')
        self.data["supplier"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("供应商不能为空", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case23(self):
        """供应商支付方式--空"""
        self.logger.info('国际机票出票--用例23--供应商代码--不正确')
        self.data["supplierPaymentMode"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("供应商支付方式不能为空", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case24(self):
        """任务id--空"""
        self.logger.info('国际机票出票--用例24--任务id--空')
        self.data["taskId"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("请传入正确的任务id", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_ticketConfirm_case25(self):
        """任务id--不正确"""
        self.logger.info('国际机票出票--用例25--任务id--不正确')
        self.data["taskId"] = "1111111111111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("不存在", str(self.response.json()))
        self.test_result = "PASS"

    def test_ticketConfirm_case26(self):
        """票号对应的航段id列表--不正确"""
        self.logger.info('国际机票出票--用例26--票号对应的航段id列表--不正确')
        self.data["priceItems"][0]["segmentIds"] = ["13245346468"]
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("无效", str(self.response.json()))
        self.test_result = "PASS"

    def test_ticketConfirm_case27(self):
        """票号对应的乘机人id--不正确"""
        self.logger.info('国际机票出票--用例27--票号对应的乘机人id--不正确')
        self.data["priceItems"][0]["passengerId"] = "13245346468"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未分配票号信息", str(self.response.json()))
        self.test_result = "PASS"

    # 未校验票号格式
    def test_ticketConfirm_case28(self):
        """票号--格式不对"""
        self.logger.info('国际机票出票--用例28--票号--格式不对')
        self.data["priceItems"][0]["ticketNo"] = "1326468"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue("ok",self.response.json()["data"])
        self.test_result = "PASS"

    # 不存在的供应商也可出票
    def test_ticketConfirm_case29(self):
        """供应商代码--不正确"""
        self.logger.info('国际机票出票--用例29--出发机空场代码--空')
        self.data["supplier"] = "aaa"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue("ok",self.response.json()["data"])
        self.test_result = "PASS"

    # 不存在的支付方式也可出票
    def test_ticketConfirm_case30(self):
        """供应商支付方式--不存在"""
        self.logger.info('国际机票出票--用例30--供应商支付方式--不存在')
        self.data["supplierPaymentMode"] = "111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue("ok",self.response.json()["data"])
        self.test_result = "PASS"


if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(testsuite)

