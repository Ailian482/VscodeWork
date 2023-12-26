import re
import unittest
import time
from Common.Base import Base
from Common import operationExcel, Log
from Utils import JsonUtil, JsonPathUtil
from TestCase.TestCase_train.TrainProcess import TrainProcess
from ApiData.UrlHeaderData import UrlHeaderData
from Config.ReadConfig import readconfig


'''
火车票改签
'''
status = str(readconfig().get_status("status"))


class TestChangeTrain(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger = Log.log("test_login").logger
        cls.operateExcel = operationExcel.operationExcel(readconfig().get_table_name("train"), "change")
        cls.url = readconfig().get_train_url("change")

    def setUp(self):
        # 获取token
        self.jutil = JsonPathUtil.jsonpath_util()
        login_response = Base().Customer_login()
        self.api = UrlHeaderData()
        self.token = self.jutil.get_values(login_response, "token")[0]
        self.headers = {"Content-Type": "application/json", "Authorization": "Bearer {0}".format(self.token)}
        self.data = JsonUtil.OperetionJson("train.json").get_data("changeTrain")
        self.fee_data = JsonUtil.OperetionJson("train.json").get_data("changeFee")
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

    # 构造改签接口的请求数据
    def get_change_data(self):
        query_id, seat_type, train_no = TrainProcess().search_train()
        order_id, passenger_id, header = TrainProcess().get_passenger_id()
        self.data["orderId"] = order_id
        self.data["passengerIds"] = passenger_id
        self.data["route"]["queryId"] = query_id
        self.data["route"]["seatType"] = seat_type
        self.data["route"]["trainNo"] = train_no
        self.fee_data["orderId"] = order_id
        self.fee_data["route"]["queryId"] = query_id
        self.fee_data["route"]["seatType"] = seat_type
        self.fee_data["route"]["trainNo"] = train_no
        return self.data, header

    def get_change_fee(self, header):
        url = readconfig().get_train_url("changefee")
        response = self.api.urlHeaderData(url, header, self.fee_data)
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

    # 用例1--正常改签
    @unittest.skipIf(status=='200', "产生数据：用例1--正常改签")
    def test_change_case01(self):
        """正常改签，所有必填参数均正确"""
        self.logger.info('火车票改签--用例01--正常改签')
        data, header = self.get_change_data()
        change_feekey = self.get_change_fee(header)
        if not change_feekey:
            self.assertFalse("获取feeKey失败！")
        data["feeKey"] = change_feekey
        time.sleep(5)
        self.response = self.api.urlHeaderData(self.url, header, data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例2--改签费用--为空
    def test_change_case02(self):
        """改签费用为空"""
        self.logger.info('火车票改签--用例02--改签费用--为空')
        self.data["feeKey"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("改签feeKey不能为空", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例3--改签费用--数据无效
    @unittest.skipIf(status=='200', "产生数据：用例3--改签费用--数据无效")
    def test_change_case03(self):
        """改签费用--数据无效"""
        self.logger.info('火车票改签--用例03--改签票补差价--数据无效')
        data, header = self.get_change_data()
        data["feeKey"] = "`da"
        time.sleep(5)
        self.response = self.api.urlHeaderData(self.url, header, data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("价格不存在或已过期", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例4--订单号--为空
    def test_change_case04(self):
        """订单号为空"""
        self.logger.info('火车票改签--用例04--订单号--为空')
        self.data["orderId"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("产品订单id不能为空", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例5--订单号--数据无效
    def test_change_case05(self):
        """正确订单号数据无效"""
        self.logger.info('火车票改签--用例05--订单号--数据无效')
        self.data["orderId"] = "aaaaaaaaaaaaaaaaa"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("产品订单id不规范", str(self.response.json()))
        self.test_result = "PASS"

    # 用例6--乘客id--空格
    def test_change_case06(self):
        """乘客id为空"""
        self.logger.info('火车票改签--用例6--乘客id--空格')
        self.data["passengerIds"] = []
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("乘客id不能为空", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例7--乘客id--数据无效
    @unittest.skipIf(status=='200', "产生数据：用例7--乘客id--数据无效")
    def test_change_case07(self):
        """乘客id数据无效"""
        self.logger.info('火车票改签--用例07--乘客id--数据无效')
        data, header = self.get_change_data()
        data["passengerIds"] = ["aaaaaaaaaaaaaaaa"]
        change_feekey = self.get_change_fee(header)
        if not change_feekey:
            self.assertFalse("获取feeKey失败！")
        data["feeKey"] = change_feekey
        time.sleep(5)
        self.response = self.api.urlHeaderData(self.url, header, data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("不存在", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例8--出发站--空
    def test_change_case08(self):
        """出发站为空"""
        self.logger.info('火车票改签--用例08--出发站--空')
        self.data["route"]["fromStation"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("出发站不能为空", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例9--出发站--三字码数据无效
    @unittest.skipIf(status=='200', "产生数据：用例9--出发站--三字码数据无效")
    def test_change_case09(self):
        """出发站三字码数据无效"""
        self.logger.info('火车票改签--用例09--出发站--三字码数据无效')
        data, header = self.get_change_data()
        self.data["route"]["fromStation"] = "111"
        change_feekey = self.get_change_fee(header)
        if not change_feekey:
            self.assertFalse("获取feeKey失败！")
        data["feeKey"] = change_feekey
        time.sleep(5)
        self.response = self.api.urlHeaderData(self.url, header, data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("出发站不能变更", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例10--车次列表查询id--空
    def test_change_case10(self):
        """车次列表查询id为空"""
        self.logger.info('火车票改签--用例10--车次列表查询id--空')
        self.data["route"]["queryId"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定车次列表id", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例11--车次列表查询id--数据无效
    def test_change_case11(self):
        """车次列表查询id数据无效"""
        self.logger.info('火车票改签--用例11--车次列表查询id--数据无效')
        self.data["route"]["queryId"] = "aaaaaaaaaaaaaaaaaaaa"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("车次信息已过期，请重新查询", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例12--坐席类型--空
    def test_change_case12(self):
        """坐席类型为空"""
        self.logger.info('火车票改签--用例12--坐席类型--空')
        self.data["route"]["seatType"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定坐席类型", str(self.response.json()))
        self.test_result = "PASS"

    # 用例13--坐席类型--数据无效
    def test_change_case13(self):
        """坐席类型数据无效"""
        self.logger.info('火车票改签--用例13--坐席类型--数据无效')
        self.data["route"]["seatType"] = "aaaaaa"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("车次信息已过期", str(self.response.json()))
        self.test_result = "PASS"

    # 用例14--到达站--空
    def test_change_case14(self):
        """到达站为空"""
        self.logger.info('火车票改签--用例14--到达站--空')
        self.data["route"]["toStation"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("到达站不能为空", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例15--到达站--数据无效
    @unittest.skipIf(status=='200', "产生数据：用例15--到达站--数据无效--未校验")
    def test_change_case15(self):
        """到达站数据无效"""
        self.logger.info('火车票改签--用例15--到达站--数据无效')
        data, header = self.get_change_data()
        data["route"]["toStation"] = "111"
        change_feekey = self.get_change_fee(header)
        if not change_feekey:
            self.assertFalse("获取feeKey失败！")
        data["feeKey"] = change_feekey
        time.sleep(5)
        self.response = self.api.urlHeaderData(self.url, header, data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例16--车次号--空
    def test_change_case16(self):
        """车次号为空"""
        self.logger.info('火车票改签--用例16--车次号--空')
        self.data["route"]["trainNo"] = ''
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("车次号不能为空", str(self.response.json()))
        self.test_result = "PASS"

    # 用例17--车次号--数据无效
    def test_change_case17(self):
        """车车次号数据无效"""
        self.logger.info('火车票改签--用例17--舱位id--不正确')
        self.data["route"]["trainNo"] = '111'
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("车次信息已过期", str(self.response.json()["message"]))
        self.test_result = "PASS"


if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    testsuite.addTest(TestChangeTrain("test_change_case09"))
    testsuite.addTest(TestChangeTrain("test_change_case10"))
    runner = unittest.TextTestRunner()
    runner.run(testsuite)

