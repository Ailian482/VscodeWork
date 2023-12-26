import unittest
from Common import Log, Base, operationExcel
from Utils import JsonPathUtil, JsonUtil
from ApiData.UrlHeaderData import UrlHeaderData
import sys
import random
from datetime import date, timedelta
from Config.ReadConfig import readconfig
sys.path.append('E:/autoInterface/AutoInterface')


status = str(readconfig().get_status("status"))


class TestSearchFlight(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.logger = Log.log("test_login").logger
        cls.jutil = JsonPathUtil.jsonpath_util()
        login_response = Base.Base().Customer_login()
        cls.token = cls.jutil.get_values(login_response, "token")[0] #获取登录
        cls.headers = {"Content-Type": "application/json", "Authorization": "Bearer {0}".format(cls.token)}
        cls.url = readconfig().get_flight_url("search")
        cls.operateExcel = operationExcel.operationExcel(readconfig().get_table_name("flight"), "search")
        cls.api = UrlHeaderData()

    def setUp(self):
        self.data = JsonUtil.OperetionJson("flight.json").get_data("searchFlight")
        flight_date = (date.today() + timedelta(days=+random.randint(10, 100))).strftime("%Y-%m-%d")
        self.data["flightDate"] = flight_date
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

    # 用例1--单程查询
    def test_search_case01(self):
        """单程查询"""
        self.logger.info('国内机票查询--用例01--单程查询')
        self.data["isOneWay"] = "true"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(self.response.json()["data"]["flights"], "查询到的航班列表为空")
        self.assertIn("西安", str(self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例2--往返查询
    def test_search_case02(self):
        """往返查询"""
        self.logger.info('国内机票查询--用例02--往返查询')
        self.data["isOneWay"] = "false"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(self.response.json()["data"]["flights"], "查询到的航班列表为空")
        self.assertIn("西安", str(self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例3--往返字段为空
    def test_search_case03(self):
        """往返字段为空"""
        self.logger.info('国内机票查询--用例03--往返字段为空')
        self.data["isOneWay"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(self.response.json()["data"]["flights"], "查询到的航班列表为空")
        self.assertIn("西安", str(self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例4--往返字段输入值不合法
    def test_search_case04(self):
        """往返字段输入值无效"""
        self.logger.info('国内机票查询--用例04--往返字段数据不合法')
        self.data["isOneWay"] = "111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(self.response.json()["data"]["flights"], "查询到的航班列表为空")
        self.assertIn("西安", str(self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例5--出发日期正常取值
    def test_search_case05(self):
        """出发日期正常取值"""
        self.logger.info('国内机票查询--用例05--出发日期正常')
        flight_data = (date.today() + timedelta(days=+random.randint(10, 100))).strftime("%Y-%m-%d")
        self.data["flightDate"] = flight_data
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(self.response.json()["data"]["flights"], "查询到的航班列表为空")
        self.assertIn(flight_data, str(self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例6--出发日期早于系统日期
    def test_search_case06(self):
        """出发日期早于系统日期"""
        self.logger.info('国内机票查询--用例06--出发日期早于当前系统日期')
        flight_data = (date.today() + timedelta(days=-random.randint(5, 15))).strftime("%Y-%m-%d")
        self.data["flightDate"] = flight_data
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 4, "返回的code不是4，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("departureDate can not be before now!", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例7--出发日期为空
    def test_search_case07(self):
        """出发日期为空"""
        self.logger.info('国内机票查询--用例07--出发日期为空')
        self.data["flightDate"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定出发日期", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例8--出发日期数据不合法
    def test_search_case08(self):
        """出发日期数据无效"""
        self.logger.info('国内机票查询--用例08--出发日期数据不合法')
        self.data["flightDate"] = "20191111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("出发日期格式不正确", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例9--出发城市正常（西安）
    def test_search_case09(self):
        """出发城市正常（西安）"""
        self.logger.info('国内机票查询--用例09--出发城市正常（西安）')
        self.data["departureCode"] = "SIA"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(self.response.json()["data"]["flights"], "查询到的航班列表为空")
        self.assertIn("西安", str(self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例10--出发城市三字码不存在
    def test_search_case10(self):
        """出发城市三字码不存在"""
        self.logger.info('国内机票查询--用例10--出发城市三字码不存在')
        self.data["departureCode"] = "AAA"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertFalse(self.response.json()["data"]["flights"], "查询的航班不为空")
        self.test_result = "PASS"

    # 用例11--出发城市为空
    def test_search_case11(self):
        """出发城市为空"""
        self.logger.info('国内机票查询--用例11--出发城市为空')
        self.data["departureCode"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定出发地代码", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例12--出发城市数据不合法
    def test_search_case12(self):
        """出发城市数据无效"""
        self.logger.info('国内机票查询--用例12--出发城市数据不合法')
        self.data["departureCode"] = "-0="
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 4, "返回的code不是4，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("请输入正确的出发机场或城市三字码", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例13--到达城市正常（深圳）
    def test_search_case13(self):
        """到达城市正常（深圳）"""
        self.logger.info('国内机票查询--用例13--到达城市正常（深圳）')
        self.data["arrivalCode"] = "SZX"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(self.response.json()["data"]["flights"], "查询到的航班列表为空")
        self.assertIn("深圳", str(self.response.json()))
        self.test_result = "PASS"

    # 用例14--到达城市三字码不存在
    def test_search_case14(self):
        """到达城市三字码不存在"""
        self.logger.info('国内机票查询--用例14--到达城市三字码不存在')
        self.data["arrivalCode"] = "YYY"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertFalse(self.response.json()["data"]["flights"], "查询的航班不为空")
        self.test_result = "PASS"

    # 用例15--到达城市为空
    def test_search_case15(self):
        """到达城市为空"""
        self.logger.info('国内机票查询--用例15--到达城市为空')
        self.data["arrivalCode"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定到达地代码", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例16--到达城市数据不合法
    def test_search_case16(self):
        """到达城市数据无效"""
        self.logger.info('国内机票查询--用例16--到达城市数据不合法')
        self.data["arrivalCode"] = "、。1"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 4, "返回的code不是4，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("请输入正确的到达机场或城市三字码", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例17--出差类型因私
    def test_search_case17(self):
        """出差类型因私"""
        self.logger.info('国内机票查询--用例17--出差类型因私')
        self.data["travelType"] = "OnPrivate"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(self.response.json()["data"]["flights"], "查询到的航班列表为空")
        self.assertIn("西安", str(self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例18--出差类型为空
    def test_search_case18(self):
        """出差类型为空"""
        self.logger.info('国内机票查询--用例18--出差类型因公')
        self.data["travelType"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(self.response.json()["data"]["flights"], "查询到的航班列表为空")
        self.assertIn("西安", str(self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例19--出差类型数据不合法--未校验
    def test_search_case19(self):
        """出差类型数据无效"""
        self.logger.info('国内机票查询--用例19--出差类型数据不合法')
        self.data["travelType"] = "`1234"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(self.response.json()["data"]["flights"], "查询到的航班列表为空")
        self.assertIn("西安", str(self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例20--出发日期超过一年
    def test_search_case20(self):
        """出发日期超过一年"""
        self.logger.info('国内机票查询--用例20--出发日期超过一年')
        flight_data = (date.today() + timedelta(days=+367)).strftime("%Y-%m-%d")
        self.data["flightDate"] = flight_data
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 4, "返回的code不是4，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("departureDate can not be after", str(self.response.json()["message"]))
        self.test_result = "PASS"


if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(testsuite)
