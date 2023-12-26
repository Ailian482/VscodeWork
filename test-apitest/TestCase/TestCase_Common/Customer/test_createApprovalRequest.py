
import unittest
from Common.Base import Base
from Common import operationExcel, Log
from Utils import JsonUtil, JsonPathUtil
from ApiData.UrlHeaderData import UrlHeaderData
from Config.ReadConfig import readconfig
import random
from datetime import date, timedelta

'''
创建出差申请
'''
status = readconfig().get_status("status")


class TestCreateApprovalRequest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger = Log.log("test_login").logger
        cls.operateExcel = operationExcel.operationExcel(readconfig().get_table_name("customer"), "createApprovalRequest")
        cls.api = UrlHeaderData()
        cls.url = readconfig().get_customer_url("createApprovalRequest")
        cls.Id = ""

    def setUp(self):
        # 获取token
        self.jutil = JsonPathUtil.jsonpath_util()
        login_response = Base().Customer_login()
        self.token = self.jutil.get_values(login_response, "token")[0]
        self.headers = {"Content-Type": "application/json", "Authorization": "Bearer {0}".format(self.token)}
        self.data = JsonUtil.OperetionJson("Common_Staff_Json.json").get_data("createApprovalRequest")
        self.data["travelDateStart"] = (date.today() + timedelta(days=+random.randint(0, 10))).strftime("%Y-%m-%d")
        self.data["travelDateEnd"] = (date.today() + timedelta(days=+random.randint(10, 30))).strftime("%Y-%m-%d")
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

    # 用例01--正常创建--单个员工
    @unittest.skipIf(status=='200', "产生数据：用例01--正常创建--单个员工")
    def test_createApprovalRequest_case01(self):
        """正常创建--单个员工"""
        self.logger.info('创建出差申请--用例01--正常创建--单个员工')
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertEqual(self.response.json()["message"], "OK", )
        self.test_result = "PASS"

    # 用例02--出差员工id--多个
    @unittest.skipIf(status=='200', "产生数据：用例02--出差员工id--多个")
    def test_createApprovalRequest_case02(self):
        """出差员工id--多个"""
        self.logger.info('创建出差申请--用例02--出差员工id--多个')
        self.data["employees"] = [{"givenNameCn": "口自动化测试", "surnameCn": "接", "id": 157849636302884864}, {"givenNameCn": "动化测试", "surnameCn": "自", "id": 239787160507650048}]
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertEqual(self.response.json()["message"], "OK", )
        self.test_result = "PASS"

    # 用例03--出差员工id--为空
    def test_createApprovalRequest_case03(self):
        """出差员工id--为空"""
        self.logger.info('创建出差申请--用例03--出差员工id--为空')
        self.data["employees"][0]["id"] = None
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.test_result = "PASS"

    # 用例04--出差员工id--不存在
    def test_createApprovalRequest_case04(self):
        """出差员工id--不存在"""
        self.logger.info('创建出差申请--用例04--出差员工id--不存在')
        self.data["employees"][0]["id"] = 1111111111111111111
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("提交的出差员工不存在", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例05--出差开始日期--早于当前日期
    @unittest.skipIf(status=='200', "产生数据：用例05--出差开始日期--早于当前日期")
    def test_createApprovalRequest_case05(self):
        """出差开始日期--早于当前日期"""
        self.logger.info('创建出差申请--用例05--出差开始日期--早于当前日期')
        self.data["travelDateStart"] = (date.today() + timedelta(days=+random.randint(-10, 0))).strftime("%Y-%m-%d")
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertEqual(self.response.json()["message"], "OK", )
        self.test_result = "PASS"

    # 用例06--出差开始日期--格式错误
    def test_createApprovalRequest_case06(self):
        """出差开始日期--格式错误"""
        self.logger.info('创建出差申请--用例06--出差开始日期--格式错误')
        self.data["travelDateStart"] = "2020/12/30"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("出差开始日期格式不正确", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例07--出差开始日期--空
    def test_createApprovalRequest_case07(self):
        """出差开始日期--空"""
        self.logger.info('创建出差申请--用例7--出差开始日期--空')
        self.data["travelDateStart"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("出差开始日期格式不正确", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例08--出差结束日期--空
    def test_createApprovalRequest_case08(self):
        """出差结束日期--空"""
        self.logger.info('创建出差申请--用例8--出差结束日期--空')
        self.data["travelDateEnd"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("出差结束日期不能为空", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例09--出差结束日期--早于当前日期
    @unittest.skipIf(status=='200', "产生数据：用例09--出差结束日期--早于当前日期")
    def test_createApprovalRequest_case09(self):
        """出差结束日期--早于当前日期"""
        self.logger.info('创建出差申请--用例9--出差结束日期--早于当前日期')
        self.data["travelDateEnd"] = (date.today() + timedelta(days=+random.randint(-10, 0))).strftime("%Y-%m-%d")
        self.data["travelDateStart"] = (date.today() + timedelta(days=+random.randint(-20, -10))).strftime("%Y-%m-%d")
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertEqual(self.response.json()["message"], "OK", )
        self.test_result = "PASS"

    # 用例10--出差结束日期--早于开始日期
    def test_createApprovalRequest_case10(self):
        """出差结束日期--早于当前日期"""
        self.logger.info('创建出差申请--用例10--出差结束日期--早于开始日期')
        self.data["travelDateEnd"] = (date.today() + timedelta(days=+random.randint(-10, 0))).strftime("%Y-%m-%d")
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("不能大于", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例11--出差结束日期--格式错误
    def test_createApprovalRequest_case11(self):
        """出差结束日期--格式错误"""
        self.logger.info('创建出差申请--用例11--出差结束日期--格式错误')
        self.data["travelDateEnd"] = "2020/12/1"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("出差截止日期格式不正确", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例12--出差是由--空
    def test_createApprovalRequest_case12(self):
        """出差是由--空"""
        self.logger.info('创建出差申请--用例12--出差是由--空')
        self.data["travelReason"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("出差事由不能为空", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例13--出差到达地--空
    def test_createApprovalRequest_case13(self):
        """出差到达地--空"""
        self.logger.info('创建出差申请--用例13--出差到达地--空')
        self.data["travelDestination"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("出差到达地不能为空", str(self.response.json()["message"]))
        self.test_result = "PASS"

if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(testsuite)


