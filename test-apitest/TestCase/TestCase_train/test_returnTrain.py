from Common.Base import Base
from Common import operationExcel, Log
from Utils import JsonUtil, JsonPathUtil
from TestCase.TestCase_train.TrainProcess import TrainProcess
import unittest
import time
from ApiData.UrlHeaderData import UrlHeaderData
from Config.ReadConfig import readconfig
from ApiData.UrlHeader import UrlHeader

'''
火车票订单退票
'''

status = str(readconfig().get_status("status"))


class TestReturnTrain(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger = Log.log("test_login").logger
        cls.operateExcel = operationExcel.operationExcel(readconfig().get_table_name("train"), "return")
        cls.data = JsonUtil.OperetionJson("train.json").get_data("returnTrain")
        cls.url = readconfig().get_train_url("return")

    def setUp(self):
        # 获取token
        self.jutil = JsonPathUtil.jsonpath_util()
        login_response = Base().Customer_login()
        self.api = UrlHeaderData()
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

    def get_feekey(self, header, order_id):
        url = "{0}{1}".format(readconfig().get_train_url("returnfee"), order_id)
        response = UrlHeader().urlHeader(url, header)
        if response.json()["code"] != 0:
            return ""
        return self.jutil.get_values(response, "feeKey")[0]

    def get_error(self, response):
        if self.response.json().__contains__("code"):
            self.response_code = self.response.json()["code"]
        if self.response.json().__contains__("message"):
            self.message = response.json()["message"]
        else:
            self.message = response.json()

    # 用例1--正常退票
    @unittest.skipIf(status=='200', '正常退票--产生数据')
    def test_return_case01(self):
        """正常退票"""
        self.logger.info('火车票退票--用例01--正常退票（订单号和乘客id均正确）')
        order_id, passenger_id, header = TrainProcess().get_passenger_id()
        if not order_id:
            self.assertFalse("下单失败，订单ID为空")
        return_fee = self.get_feekey(header, order_id)
        if not return_fee:
            self.assertFalse("获取feeKey失败！")
        self.data["feeKey"] = return_fee
        self.data['orderId'] = order_id
        self.data['passengerIds'] = passenger_id
        time.sleep(10)
        self.response = self.api.urlHeaderData(self.url, header, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertEqual(self.response.json()["message"], "OK", )
        self.test_result = "PASS"
        
    # 用例2--订单号-空
    def test_return_case02(self):
        """订单号-空"""
        self.logger.info('火车票退票--用例02--订单号为空')
        self.data['orderId'] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("产品订单id不", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例3--订单号-不存在
    def test_return_case03(self):
        """订单号-不存在"""
        self.logger.info('火车票退票--用例03--订单号不存在')
        self.data['orderId'] = "235325462314335"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("checkOrderOwner", str(self.response.json()["debugMsg"]))
        self.test_result = "PASS"

    # 用例4--乘客id-为空
    @unittest.skipIf(status=='200', '用例4--乘客id-为空--产生数据')
    def test_return_case04(self):
        """乘客id-为空"""
        self.logger.info('火车票退票--用例04--乘客id为空')
        self.data['passengerIds'] = [""]
        response, order_id, header = TrainProcess().pay_train()
        if not response:
            self.assertFalse("下单失败，订单ID为空")
        self.data['orderId'] = order_id
        self.response = self.api.urlHeaderData(self.url, header, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("在订单中不存在", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例5--乘客id-不存在
    @unittest.skipIf(status=='200', '用例5--乘客id-不存在--产生数据')
    def test_return_case05(self):
        """乘客id-不存在"""
        self.logger.info('火车票退票--用例05--乘客id不存在')
        self.data['passengerIds'] = ["132869405225914368"]
        response, order_id, header = TrainProcess().pay_train()
        if not response:
            self.assertFalse("下单失败，订单ID为空")
        self.data['orderId'] = order_id
        self.response = self.api.urlHeaderData(self.url, header, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("在订单中不存在", str(self.response.json()["message"]))
        self.test_result = "PASS"


if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(testsuite)


