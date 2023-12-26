import unittest
from Common.Base import Base
from Common import operationExcel, Log
from Utils import JsonPathUtil
from TestCase.TestCase_intflight.IntflightProcess import IntflightProcess
from ApiData.UrlHeader import UrlHeader
from Config.ReadConfig import readconfig


'''
国际机票取消pnr
'''
status = readconfig().get_status("status")


class TestReturnFlight(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.logger = Log.log("test_login").logger
        cls.url = readconfig().get_intflight_url("cancelPnr")
        cls.operateExcel = operationExcel.operationExcel(readconfig().get_table_name("intflight"), "cancelPnr")

    def setUp(self):
        # 获取token
        self.jutil = JsonPathUtil.jsonpath_util()
        login_response = Base().Staff_login()
        self.api = UrlHeader("Staff_url")
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
    @unittest.skipIf(status, "产生数据：用例1--正常取消")
    def test_return_case01(self):
        """正常取消"""
        self.logger.info('国际机票取消pnr--用例01--正常取消')
        task_id, order_id, header = IntflightProcess().get_task_detail("cancelPnr")
        if not task_id:
            self.assertFalse("获取taskId失败")
        url = "{0}{1}".format(self.url, task_id)
        self.response = self.api.urlHeader(url, header)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertEqual(self.response.json()["message"], "OK", )
        self.test_result = "PASS"

    # 用例2--任务id-空
    def test_return_case02(self):
        """任务id-空"""
        self.logger.info('国际机票取消pnr--用例02--任务id-空')
        task_id = ""
        url = "{0}{1}".format(self.url, task_id)
        self.response = self.api.urlHeader(url, self.headers)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("任务id不能为空", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例3--任务id--不存在
    def test_return_case03(self):
        """任务id--不存在"""
        self.logger.info('国际机票取消pnr--用例03--任务id--不存在')
        task_id = 121212121212121212
        url = "{0}{1}".format(self.url, task_id)
        self.response = self.api.urlHeader(url, self.headers)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("不存在", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例4--任务id--已取消
    def test_return_case04(self):
        """任务id--已取消"""
        self.logger.info('国际机票取消pnr--用例04--任务id--已取消')
        task_id = 229996845613584384
        url = "{0}{1}".format(self.url, task_id)
        self.response = self.api.urlHeader(url, self.headers)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 96, "返回的code不是96，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("当前任务状态[Completed]不可操作", str(self.response.json()["message"]))
        self.test_result = "PASS"

if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(testsuite)


