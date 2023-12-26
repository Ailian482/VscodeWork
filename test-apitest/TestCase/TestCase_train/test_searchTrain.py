import unittest
import sys
import random
from Common import Log, Base, operationExcel
from Utils import JsonPathUtil, JsonUtil
from ApiData.UrlHeaderData import UrlHeaderData
from datetime import date, timedelta
from Config.ReadConfig import readconfig


sys.path.append('E:/autoInterface/AutoInterface')

status = str(readconfig().get_status("status"))


class TestSearchTrain(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger = Log.log("test_login").logger
        cls.jutil = JsonPathUtil.jsonpath_util()
        cls.url = readconfig().get_train_url("search")
        cls.operateExcel = operationExcel.operationExcel(readconfig().get_table_name("train"), "search")
        cls.api = UrlHeaderData()

    def setUp(self):
        login_response = Base.Base().Customer_login()
        self.token = self.jutil.get_values(login_response, "token")[0]
        self.headers = {"Content-Type": "application/json", "Authorization": "Bearer {0}".format(self.token)}
        self.search_data = JsonUtil.OperetionJson("train.json").get_data("searchTrain")
        train_date = (date.today() + timedelta(days=+random.randint(0, 60))).strftime("%Y-%m-%d")
        self.search_data["trainDate"] = train_date
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

    # 用例1--正常查询
    def test_search_case01(self):
        """正常查询"""
        self.logger.info('火车票查询--用例01--正常查询')
        self.response = self.api.urlHeaderData(self.url, self.headers, self.search_data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("深圳", str(self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例2--出发站--正常(北京)
    def test_search_case02(self):
        """出发站--正常(北京)"""
        self.logger.info('火车票查询--用例02--出发站正确（北京）')
        self.search_data["fromStation"] = "BJP"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.search_data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("北京", str(self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例3--出发站--空
    def test_search_case03(self):
        """出发站--空"""
        self.logger.info('火车票查询--用例03--出发站为空')
        self.search_data["fromStation"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.search_data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("出发站不能为空", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例4--出发站--三字码不存在
    def test_search_case04(self):
        """出发站--三字码不存在"""
        self.logger.info('火车票查询--用例04--出发站三字码不存在')
        self.search_data["fromStation"] = "ZZZ"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.search_data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 1, "返回的code不是1，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("暂无数据", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例5--出发站--三字码不合法
    def test_search_case05(self):
        """出发站--三字码不合法"""
        self.logger.info('火车票查询--用例05--出发站三字码不合法')
        self.search_data["fromStation"] = "111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.search_data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("请输入正确的出发站简码", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例6--乘车日期--正常
    def test_search_case06(self):
        """乘车日期--正常"""
        self.logger.info('火车票查询--用例06--乘车日期正确')
        train_date = (date.today() + timedelta(days=+random.randint(0, 30))).strftime("%Y-%m-%d")
        self.search_data["trainDate"] = train_date
        self.response = self.api.urlHeaderData(self.url, self.headers, self.search_data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn(train_date, str(self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例7--乘车日期--早于当前日期
    def test_search_case07(self):
        """乘车日期--早于当前日期"""
        self.logger.info('火车票查询--用例07--乘车日期早于当前日期')
        train_date = (date.today() + timedelta(days=-15)).strftime("%Y-%m-%d")
        self.search_data["trainDate"] = train_date
        self.response = self.api.urlHeaderData(self.url, self.headers, self.search_data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("不能查询今日之前的余票信息", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例8--乘车日期--空
    def test_search_case08(self):
        """乘车日期--空"""
        self.logger.info('火车票查询--用例08--乘车日期为空')
        self.search_data["trainDate"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.search_data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("出发日期不能为空", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例9--乘车日期--非法数据
    def test_search_case09(self):
        """车日期--非法数据"""
        self.logger.info('火车票查询--用例09--乘车日期数据非法')
        self.search_data["trainDate"] = "aaaa-bb-cc"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.search_data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("请输入正确的乘车日期", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例10--乘车日期--超过60天
    def test_search_case10(self):
        """乘车日期--超过60天"""
        self.logger.info('火车票查询--用例10--乘车日期超过60天')
        train_date = (date.today() + timedelta(days=+61)).strftime("%Y-%m-%d")
        self.search_data["trainDate"] = train_date
        self.response = self.api.urlHeaderData(self.url, self.headers, self.search_data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("不能查询 60 天之后的余票信息", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例11--到达站--正常（广州）
    def test_search_case11(self):
        """到达站--正常（广州）"""
        self.logger.info('火车票查询--用例11--到达站正常（广州）')
        self.search_data["toStation"] = "GZQ"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.search_data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("广州", str(self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例12--到达站--三字码不存在
    def test_search_case12(self):
        """到达站--三字码不存在"""
        self.logger.info('火车票查询--用例12--到达站三字码不存在')
        self.search_data["toStation"] = "TTT"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.search_data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 1, "返回的code不是1，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("暂无数据", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例13--到达站--三字码空
    def test_search_case13(self):
        """到达站--三字码空"""
        self.logger.info('火车票查询--用例13--到达站三字码为空')
        self.search_data["toStation"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.search_data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("请输入正确的到达站简码", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例14--到达站--三字码不合法
    def test_search_case14(self):
        """到达站--三字码不合法"""
        self.logger.info('火车票查询--用例14--到达站三字码不合法')
        self.search_data["toStation"] = "555"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.search_data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("请输入正确的到达站简码", str(self.response.json()["errors"]))
        self.test_result = "PASS"


if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(testsuite)
