import unittest

from ApiData.UrlHeaderData import UrlHeaderData
from Common import Log, Base, operationExcel
from Utils import JsonPathUtil, JsonUtil
from datetime import date, timedelta

'''
    运营管理--商旅事业部管理--机构客户
    --更新公司授信模式
'''


class updateCorpSettlementInfo(unittest.TestCase):


    @classmethod
    def setUpClass(cls) -> None:
        cls.logger = Log.log("test_login").logger
        cls.jutil = JsonPathUtil.jsonpath_util()
        cls.url = "/admin/v1/corp/updateCorpSettlementInfo"
        cls.data = JsonUtil.OperetionJson("Common_Staff_Json.json").get_data("updateCorpSettlementInfo")
        cls.Send = UrlHeaderData('Staff_url')

    def setUp(self):
        loginResponseData = Base.Base().Staff_login()
        self.token = self.jutil.get_values(loginResponseData, "token")[0]
        header = {'Content-Type': 'application/json', 'Authorization': ''}
        self.header = self.jutil.set_values(header, 'Authorization', "Bearer " + self.token)
        self.test_result = "Fail"

    def tearDown(self):
        # 写入
        # row_number = int(self.id()[-2:])
        # self.operateExcel = operationExcel.operationExcel("hotel_interface.xls", "search")
        # self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("id"), row_number)
        # self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("描述"), self.Test_name)
        # self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("path"), self.url)
        # self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("header"), self.header)
        # self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("请求数据"), self.data)
        # self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("预期结果"), self.expected_result)
        # self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("实际结果"), self.response)
        # self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("测试结果"), self.test_result)
        pass

    # 用例1--修改支付方式（改为授信）

    def test_search_case01(self):
        self.Test_name = '用例1--修改支付方式'
        self.logger.info(self.Test_name)
        self.jutil.set_values(self.data, "corpPayMode", "CorpCredit")
        response = self.Send.urlHeaderData(self.url, self.header, self.data)
        self.response = response.json()
        self.expected_result = "code = 0"
        # 断言
        self.assertEqual(self.response["code"], 0)
        self.assertIn("OK", str(response.json()["message"]))
        self.test_result = "Pass"


if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(testsuite)
