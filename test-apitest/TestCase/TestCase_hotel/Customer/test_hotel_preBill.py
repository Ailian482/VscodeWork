import unittest

from ApiData.UrlHeader import UrlHeader
from Common import Log, Base, operationExcel
from TestCase.TestCase_Common.Common_Staff import Common_interface
from TestCase.TestCase_hotel.hotel_Customer import HotelProcess

from Utils import JsonPathUtil

'''
    订单支付
'''
status = True


class HotelPreBill(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        Result = Common_interface().updateCorpSettlementInfo_CorpPayMode("CorpCredit")  # 支付方式修改为授信
        if Result is False:  # 判断是否修改成功
            exit("支付方式修改失败")

        cls.logger = Log.log("test_login").logger
        cls.jutil = JsonPathUtil.jsonpath_util()
        cls.url = "/front/v1/hotel/preBill" + "?" + "orderId="
        cls.Send = UrlHeader("Customer_url")

    def setUp(self):
        loginResponseData = Base.Base().Customer_login()
        self.token = self.jutil.get_values(loginResponseData, "token")[0]
        header = {'Content-Type': 'application/json', 'Authorization': ''}
        self.header = self.jutil.set_values(header, 'Authorization', "Bearer " + self.token)
        self.test_result = "Fail"

    def tearDown(self):
        # 写入
        row_number = int(self.id()[-2:])
        self.operateExcel = operationExcel.operationExcel("hotel_interface.xls", "preBill")
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("id"), row_number)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("描述"), self.Test_name)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("path"), self.url)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("header"), self.header)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("请求数据"), "该接口无请求数据")
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("预期结果"), self.expected_result)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("实际结果"), self.response)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("测试结果"), self.test_result)
        pass

    # 用例1-- 订单支付（正常）
    # @unittest.skipIf(status=='200', "产生数据：用例1--正常支付")
    def test_search_case01(self):
        """订单支付 --订单支付（正常）"""
        self.Test_name = '用例1 --订单支付 --订单支付（正常）'
        self.logger.info(self.Test_name)
        DependData, header = HotelProcess().placeOrder()
        url = self.url + str(DependData["data"])
        # 预期结果
        self.expected_result = "code = 0 / OrderId"
        # 实际结果
        response = self.Send.urlHeader(url, header)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 0)
        self.test_result = "Pass"

    # 用例2 -- 登录态校验
    def test_search_case02(self):
        """订单支付 --登录态校验'"""
        self.Test_name = '用例2 --订单支付 --登录态校验'
        self.logger.info(self.Test_name)
        DependData, header = HotelProcess().placeOrder()
        url = self.url + DependData["data"]
        header = {'Content-Type': 'application/json'}
        # 预期结果
        self.expected_result = "code = 401 / Data：尚未登陆"
        # 实际结果
        response = self.Send.urlHeader(url, header)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 401)
        self.assertIn("您尚未登录", str(response.json()["message"]))
        self.test_result = "Pass"

    # 用例3 -- 订单号为空
    def test_search_case03(self):
        """订单支付 --订单号为空"""
        self.Test_name = '用例3 --订单支付 --订单号为空'
        self.logger.info(self.Test_name)
        url = self.url + ""
        # 预期结果
        self.expected_result = "code = 98 / Data：请输入正确订单号"
        # 实际结果
        response = self.Send.urlHeader(url, self.header)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 98)
        self.assertIn("请输入正确的", str(response.json()["message"]))
        self.test_result = "Pass"

    # 用例4 -- 订单号不存在
    def test_search_case04(self):
        """订单支付 --订单号不存在"""
        self.Test_name = '用例4 --订单支付 --订单号不存在'
        self.logger.info(self.Test_name)
        url = self.url + ("111111111111111111")
        # 预期结果
        self.expected_result = "code = 99 / id 不存在"
        # 实际结果
        response = self.Send.urlHeader(url, self.header)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 99)
        self.assertIn("不存在", str(response.json()["message"]))
        self.test_result = "Pass"

    # # 用例5 -- 订单号存在，但是不属于该登录账号（涉及另一个账号实时订单号问题，比较复杂，暂时忽略）
    # def test_search_case05(self):
    #     self.Test_name = '用例5 --订单支付 --订单号存在，但是不属于该登录账号'
    #     self.logger.info(self.Test_name)
    #     url = self.url + "151001672817184768"
    #     response = payAndCancel.payAndCancel().payAndCancelOrder(self.header, url)
    #     self.response = response.json()
    #     self.expected_result = "code = 2 / 没有权限访问"
    #     # 断言
    #     self.assertEqual(response.json()["code"], 2)
    #     self.assertIn("没有权限", str(response.json()["message"]))
    #     self.test_result = "Pass"


if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(testsuite)
