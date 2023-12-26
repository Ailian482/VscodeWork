import unittest
from Common import Log, operationExcel
from Utils import JsonUtil
from Common import BaseHttp
from Config.ReadConfig import readconfig

status = str(readconfig().get_status("status"))


class TestLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger = Log.log("test_login").logger
        cls.basehttp = BaseHttp.SendHttp("Customer_url")
        cls.operateExcel = operationExcel.operationExcel(readconfig().get_table_name("flight"), sheet_name="login")
        cls.url = readconfig().get_flight_url("login")
        cls.header = {'Content-Type': 'application/json', 'Connection': 'Keep-Alive'}

    def setUp(self):
        self.data = JsonUtil.OperetionJson("flight.json").get_data("login")
        self.test_result = "FAIL"

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

    # 构造请求数据
    def send_request(self, data):
        self.basehttp.set_url(self.url)
        self.basehttp.set_headers(self.header)
        self.basehttp.set_data(data)

    # 用例1--正常登陆
    def test_login_case01(self):
        """正常登陆（用户名密码均正确）"""
        self.logger.info('登录--用例01--正常登录')
        self.send_request(self.data)
        self.response = self.basehttp.http_post()
        self.assertIn("token", self.response.json()["data"])
        self.test_result = "PASS"

    # 用例2--客户端类型-Web
    def test_login_case02(self):
        """客户端类型-Web"""
        self.logger.info('登录--用例02--客户端类型-Web')
        self.data["clientType"] = "Web"
        self.send_request(self.data)
        self.response = self.basehttp.http_post()
        self.assertIn("token", self.response.json()["data"])
        self.test_result = "PASS"

    # 用例3--客户端类型-Ios
    def test_login_case03(self):
        """客户端类型-Ios"""
        self.logger.info('登录--用例03--客户端类型-Ios')
        self.data["clientType"] = "Ios"
        self.send_request(self.data)
        self.response = self.basehttp.http_post()
        self.assertIn("token", self.response.json()["data"])
        self.test_result = "PASS"

    # 用例4--客户端类型-Android
    def test_login_case04(self):
        """客户端类型-Android"""
        self.logger.info('登录--用例04--客户端类型-Android')
        self.data["clientType"] = "Android"
        self.send_request(self.data)
        self.response = self.basehttp.http_post()
        self.assertIn("token", self.response.json()["data"])
        self.test_result = "PASS"

    # 用例5--客户端类型-空
    def test_login_case05(self):
        """客户端类型-空"""
        self.logger.info('登录--用例05--客户端类型-空')
        self.data["clientType"] = ""
        self.send_request(self.data)
        self.response = self.basehttp.http_post()
        self.assertIn("登录客户端类型错误", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例6--客户端类型-不正确的数据
    def test_login_case06(self):
        """客户端类型-不正确的数据"""
        self.logger.info('登录--用例06--客户端类型-不正确的数据')
        self.data["clientType"] = "123"
        self.send_request(self.data)
        self.response = self.basehttp.http_post()
        self.assertIn("登录客户端类型错误", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例7--用户名-正确
    def test_login_case07(self):
        """用户名-正确"""
        self.logger.info('登录--用例07--用户名-正确')
        self.data["identity"] = "15950582102"
        self.send_request(self.data)
        self.response = self.basehttp.http_post()
        self.assertIn("token", self.response.json()["data"])
        self.test_result = "PASS"

    # 用例8--用户名-空
    def test_login_case08(self):
        """用户名-空"""
        self.logger.info('登录--用例08--用户名-空')
        self.data["identity"] = ""
        self.send_request(self.data)
        self.response = self.basehttp.http_post()
        self.assertIn("用户密码错误", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例9--用户名-不正确
    def test_login_case09(self):
        """用户名-不正确"""
        self.logger.info('登录--用例09--用户名-不正确')
        self.data["identity"] = "111111111"
        self.send_request(self.data)
        self.response = self.basehttp.http_post()
        self.assertIn("用户名不存在", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例10--密码-正确
    def test_login_case10(self):
        """密码-正确"""
        self.logger.info('登录--用例10--密码-正确')
        self.send_request(self.data)
        self.response = self.basehttp.http_post()
        self.assertIn("token", self.response.json()["data"])
        self.test_result = "PASS"

    # 用例11--密码-空
    def test_login_case11(self):
        """密码-空"""
        self.logger.info('登录--用例11--密码-空')
        self.data["password"] = ""
        self.send_request(self.data)
        self.response = self.basehttp.http_post()
        self.assertIn("密码错误", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例12--密码-不正确
    def test_login_case12(self):
        """密码-不正确"""
        self.logger.info('登录--用例12--密码-不正确')
        self.data["password"] = "111111"
        self.send_request(self.data)
        self.response = self.basehttp.http_post()
        self.assertIn("密码错误", str(self.response.json()["message"]))
        self.test_result = "PASS"


if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(testsuite)
