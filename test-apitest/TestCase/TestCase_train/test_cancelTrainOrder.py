from Common.Base import Base
from Common import operationExcel, Log
from Utils import JsonPathUtil
from ApiData.UrlHeader import UrlHeader
from TestCase.TestCase_train.TrainProcess import TrainProcess
import unittest
from Config.ReadConfig import readconfig


'''
取消火车票订单
'''
status = str(readconfig().get_status("status"))


class TestCancelTrainOrder(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger = Log.log("test_login").logger
        cls.operateExcel = operationExcel.operationExcel(readconfig().get_table_name("train"), "cancel")
        cls.url = readconfig().get_train_url("cancel")

    def setUp(self):
        # 获取token
        self.jutil = JsonPathUtil.jsonpath_util()
        login_response = Base().Customer_login()
        self.token = self.jutil.get_values(login_response, "token")[0]
        self.headers = {"Content-Type": "application/json", "Authorization": "Bearer {0}".format(self.token)}
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

    # 用例1--正常取消
    @unittest.skipIf(status=='200', "产生数据：用例1--正常取消")
    def test_cancel_case01(self):
        """订单号正确"""
        self.logger.info('火车票订单取消--用例01--正常取消')
        self.response = TrainProcess().cancel_train()
        if not self.response:
            self.assertFalse("下单失败，订单ID为空")
        if isinstance(self.response, str):
            self.assertFalse("订座失败，预订状态：{0}".format(self.response))
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("OK", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例2--订单号-空
    def test_cancel_case02(self):
        """订单号为空"""
        self.logger.info('火车票订单取消--用例02--订单号为空')
        self.response = UrlHeader().urlHeader(self.url, self.headers)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("请输入正确的国内火车票订单 ID", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例3--订单号-不存在
    def test_cancel_case03(self):
        """订单号不存在"""
        self.logger.info('火车票订单取消--用例03--订单号不存在')
        order_id = "235325462314335"
        self.url = "{0}{1}".format(self.url, order_id)
        self.response = UrlHeader().urlHeader(self.url, self.headers)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("checkOrderOwner", str(self.response.json()["debugMsg"]))
        self.test_result = "PASS"

    # 用例4--订单号--非数字
    def test_cancel_case04(self):
        """订单号非数字"""
        self.logger.info('火车票订单取消--用例04--订单号非数字')
        order_id = "aaaa"
        self.url = "{0}{1}".format(self.url, order_id)
        self.response = UrlHeader().urlHeader(self.url, self.headers)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("请输入正确的国内火车票订单 ID", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例5--订单号-不可取消（无权限）
    def test_cancel_case05(self):
        """订单号状态不可取消"""
        self.logger.info('火车票订单取消--用例05--订单号不可取消')
        order_id = "119754251143614464"
        self.url = "{0}{1}".format(self.url, order_id)
        self.response = UrlHeader().urlHeader(self.url, self.headers)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 2, "返回的code不是2，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("当前员工没有权限操作此订单", str(self.response.json()["message"]))
        self.test_result = "PASS"


if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(testsuite)


