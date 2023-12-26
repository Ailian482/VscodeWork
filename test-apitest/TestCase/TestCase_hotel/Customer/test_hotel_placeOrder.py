import unittest
from ApiData.UrlHeaderData import UrlHeaderData
from Common import Log, Base, operationExcel
from Config.ReadConfig import readconfig
from TestCase.TestCase_hotel.hotel_Customer import HotelProcess

from Utils import JsonPathUtil, JsonUtil
from datetime import date, timedelta

'''
    酒店下单接口
'''
status = str(readconfig().get_status("status"))


class HotelPlaceOrder(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger = Log.log("test_login").logger
        cls.jutil = JsonPathUtil.jsonpath_util()

        # 获取数据依赖的接口数据
        cls.dependData = HotelProcess().getHotelDetail()

        # 请求url
        cls.url = "/front/v1/hotel/placeOrder"

        # 发送实例化
        cls.Send = UrlHeaderData('Customer_url')

    def setUp(self):
        # 获取接口请求参数Json
        self.data = JsonUtil.OperetionJson("Hotel_Customer_Json.json").get_data("placeOrder_OnBusiness")
        self.privateData = JsonUtil.OperetionJson("Hotel_Customer_Json.json").get_data("placeOrder_OnPrivate")

        # 因公(OnBusiness)Json请求参数改写
        self.jutil.set_values_list(self.data,
                                   ["hotelCode", "cityCode", "roomCode", "planCode", "checkInDate", "checkOutDate"],
                                   [self.jutil.get_values(self.dependData, "data")[0]["hotelCode"],
                                    self.jutil.get_values(self.dependData, "data")[0]["cityCode"],
                                    self.jutil.get_values(self.dependData, "rooms")[0][0]["roomCode"],
                                    self.jutil.get_values(self.dependData, "rooms")[0][0]["planCode"],
                                    (date.today()).strftime("%Y-%m-%d"),
                                    (date.today() + timedelta(days=+3)).strftime("%Y-%m-%d")])
        # 因私（OnPrivate)Json请求参数改写
        self.jutil.set_values_list(self.privateData,
                                   ["hotelCode", "cityCode", "roomCode", "planCode", "checkInDate", "checkOutDate"],
                                   [self.jutil.get_values(self.dependData, "data")[0]["hotelCode"],
                                    self.jutil.get_values(self.dependData, "data")[0]["cityCode"],
                                    self.jutil.get_values(self.dependData, "rooms")[0][0]["roomCode"],
                                    self.jutil.get_values(self.dependData, "rooms")[0][0]["planCode"],
                                    (date.today()).strftime("%Y-%m-%d"),
                                    (date.today() + timedelta(days=+3)).strftime("%Y-%m-%d")])

        # 请求头header登录态处理
        loginResponseData = Base.Base().Customer_login()
        self.token = self.jutil.get_values(loginResponseData, "token")[0]
        header = {'Content-Type': 'application/json', 'Authorization': ''}
        self.header = self.jutil.set_values(header, 'Authorization', "Bearer " + self.token)
        # 测试结果的初始化
        self.test_result = "Fail"

    def tearDown(self):
        # 写入
        row_number = int(self.id()[-2:])
        self.operateExcel = operationExcel.operationExcel("hotel_interface.xls", "placeOrder")
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("id"), row_number)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("描述"), self.Test_name)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("path"), self.url)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("header"), self.header)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("请求数据"), self.data)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("预期结果"), self.expected_result)
        self.operateExcel.write_value(row_number, self.operateExcel.get_col_name_num("实际结果"), self.response)
        pass

    # 用例1--因公--普通正常下单(已添加审批单）
    # @unittest.skipIf(status=='200', "产生数据：用例1--正常下单")
    def test_search_case01(self):
        """酒店下单 --普通正常下单"""
        self.Test_name = '用例1 --酒店下单 --普通正常下单'
        self.logger.info(self.Test_name)
        # 预期结果
        self.expected_result = "code = 0 / OrderId"
        # 实际结果
        response = self.Send.urlHeaderData(self.url, self.header, self.data)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 0)
        self.assertEqual(response.json()["message"], "OK")
        self.test_result = "Pass"

    # 用例2 --因公--登录态校验
    def test_search_case02(self):
        """酒店下单 --登录态校验"""
        self.Test_name = '用例2 --酒店下单 --登录态校验'
        self.logger.info(self.Test_name)
        header = {'Content-Type': 'application/json'}
        # 预期结果
        self.expected_result = "code = 401 / Data：尚未登陆"
        # 实际结果
        response = self.Send.urlHeaderData(self.url, header, self.data)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 401)
        self.assertIn("您尚未登录", str(response.json()["message"]))
        self.test_result = "Pass"

    # 用例3--因公-- 联系人姓名为空
    def test_search_case03(self):
        """酒店下单 --入住人姓名为空"""
        self.Test_name = '用例3 --酒店下单 --入住人姓名为空'
        self.logger.info(self.Test_name)
        self.jutil.set_values(self.data, "name", "")
        # 预期结果
        self.expected_result = "code = 98 / 联系人姓名不能为空"
        # 实际结果
        response = self.Send.urlHeaderData(self.url, self.header, self.data)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 98)
        self.assertIn("联系人姓名不能为空", response.json()["message"])
        self.test_result = "Pass"

    # 用例4--因公-- 联系人手机号为空
    # @unittest.skipIf(status=='200', "产生数据：用例4--联系人手机号为空")
    def test_search_case04(self):
        """酒店下单 --联系人手机号为空"""
        self.Test_name = '用例4 --酒店下单 --联系人手机号为空'
        self.logger.info(self.Test_name)
        self.jutil.set_values(self.data, "mobile", "")
        # 预期结果
        self.expected_result = "code = 98 / 联系人手机号不能为空"
        # 实际结果
        response = self.Send.urlHeaderData(self.url, self.header, self.data)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 98)
        self.assertEqual(response.json()["message"], "请指定联系人手机")
        self.test_result = "Pass"

    # 用例5--因公-- 联系人邮箱为空
    # @unittest.skipIf(status=='200', "产生数据：用例5--联系人邮箱为空")
    def test_search_case05(self):
        """酒店下单 --联系人邮箱为空"""
        self.Test_name = '用例5 --酒店下单 --联系人邮箱为空 '
        self.logger.info(self.Test_name)
        self.jutil.set_values(self.data, "email", "")
        # 预期结果
        self.expected_result = "code = 0 / OrderId"
        # 实际结果
        response = self.Send.urlHeaderData(self.url, self.header, self.data)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 0)
        self.assertEqual(response.json()["message"], "OK")
        self.test_result = "Pass"

    # 用例6--因公-- 入住人姓名为空
    def test_search_case06(self):
        """酒店下单 --入住人姓名为空 """
        self.Test_name = '用例6 --酒店下单 --入住人姓名为空 '
        self.logger.info(self.Test_name)
        self.jutil.set_values(self.data["travelers"][0], "name", "")
        # 预期结果
        self.expected_result = "code = 98 / 未指定入住人姓名"
        # 实际结果
        response = self.Send.urlHeaderData(self.url, self.header, self.data)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 98)
        self.assertEqual(response.json()["message"], "未指定入住人姓名")
        self.test_result = "Pass"

    # 用例7--因公-- 费用部门（belongedDeptId）为空
    """BUG未修复"""
    @unittest.skipIf(status == '200', "BUG未修复——没有response")
    def test_search_case07(self):
        """酒店下单 --费用部门（belongedDeptId）为空"""
        self.Test_name = '用例7 --酒店下单 --费用部门（belongedDeptId）为空 '
        self.logger.info(self.Test_name)
        self.jutil.set_values(self.data["travelers"][0], "belongedDeptId", "")
        # 预期结果
        self.expected_result = "code = 99 / 未选择部门"
        # 实际结果
        response = self.Send.urlHeaderData(self.url, self.header, self.data)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 99)
        self.assertIn("部门", response.json()["message"])
        self.test_result = "Pass"

    # 用例8--因公-- 入住人手机号为空
    # @unittest.skipIf(status=='200', "产生数据：用例8--入住人手机号为空")
    def test_search_case08(self):
        """酒店下单 --入住人手机号为空"""
        self.Test_name = '用例8 --酒店下单 --入住人手机号为空 '
        self.logger.info(self.Test_name)
        self.jutil.set_values(self.data["travelers"][0], "mobile", "")
        # 预期结果
        self.expected_result = "code = 0 / OrderId"
        # 实际结果
        response = self.Send.urlHeaderData(self.url, self.header, self.data)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 0)
        self.assertIn("OK", response.json()["message"])
        self.test_result = "Pass"

    # 用例9--因公-- 入住人邮箱为空
    # @unittest.skipIf(status=='200', "产生数据：用例9--入住人邮箱为空")
    def test_search_case09(self):
        """酒店下单 --入住人邮箱为空"""
        self.Test_name = '用例9 --酒店下单 --入住人邮箱为空 '
        self.logger.info(self.Test_name)
        self.jutil.set_values(self.data["travelers"][0], "email", "")
        # 预期结果
        self.expected_result = "code = 0 / OrderId"
        # 实际结果
        response = self.Send.urlHeaderData(self.url, self.header, self.data)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 0)
        self.assertIn("OK", response.json()["message"])
        self.test_result = "Pass"

    # 用例10--因公-- 审批单号为空
    '''BUG
    未修复'''

    @unittest.skipIf(status == '200', "BUG未修复——没有response")
    def test_search_case10(self):
        """因公-- 审批单号为空 """
        self.Test_name = '用例10--因公-- 审批单号为空 '
        self.logger.info(self.Test_name)
        self.jutil.set_values(self.data["travelers"][0], "approvalNo", "")
        self.jutil.set_values(self.data["travelers"][0], "approvalId", "")
        # 预期结果
        self.expected_result = "code = 0 / OrderId"
        # 实际结果
        response = self.Send.urlHeaderData(self.url, self.header, self.data)
        self.response = response.json()
        # 结果格式校验
        self.assertEqual(response.json()["code"], 0)
        self.assertIn("OK", response.json()["message"])
        self.test_result = "Pass"

    # 用例11--因公-- 非本人审批单号
    '''BUG
    未修复'''

    @unittest.skipIf(status == '200', "BUG未修复——使用他人审批单号仍可通过")
    def test_search_case11(self):
        """因公-- 非本人审批单号"""
        self.Test_name = '# 用例11--因公-- 非本人审批单号'
        self.logger.info(self.Test_name)
        self.jutil.set_values_list(self.data["travelers"][0], ["approvalNo", "approvalId"],
                                   ["S202003030002", "203548167231377408"])
        # 预期结果
        self.expected_result = "code = 99 / 审批单号不存在"
        # 实际结果
        response = self.Send.urlHeaderData(self.url, self.header, self.data)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 99)
        self.assertIn("审批单号不存在", response.json()["message"])
        self.test_result = "Pass"

    # 用例12--因公-- 审批单号不存在
    def test_search_case12(self):
        """因公-- 审批单号不存在"""
        self.Test_name = '# 用例12--因公-- 审批单号不存在'
        self.logger.info(self.Test_name)
        self.jutil.set_values_list(self.data["travelers"][0], ["approvalNo", "approvalId"],
                                   ["1234", "4321"])
        # 预期结果
        self.expected_result = "code = 99 / 审批单号不存在"
        # 实际结果
        response = self.Send.urlHeaderData(self.url, self.header, self.data)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 99)
        self.assertIn("不存在", response.json()["message"])
        self.test_result = "Pass"

    # 用例13--因公—— 审批单号已过期
    '''BUG
    未修复'''

    @unittest.skipIf(status == '200', "BUG未修复")
    def test_search_case13(self):
        """因公—— 审批单号已过期"""
        self.Test_name = '用例13--因公—— 审批单号已过期'
        self.logger.info(self.Test_name)
        self.jutil.set_values_list(self.data["travelers"][0], ["approvalNo", "approvalId"],
                                   ["S202003050002", "204247494140497920"])
        # 预期结果
        self.expected_result = "code = 99 / 审批单号不存在"
        # 实际结果
        response = self.Send.urlHeaderData(self.url, self.header, self.data)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 99)
        self.assertIn("不存在", response.json()["message"])
        self.test_result = "Pass"

    # 用例14--因公—— 审批单号未通过审批
    '''BUG
    未修复'''

    @unittest.skipIf(status == '200', "BUG未修复")
    def test_search_case14(self):
        """因公—— 审批单号未通过审批'"""
        self.Test_name = '用例14--因公—— 审批单号未通过审批'
        self.logger.info(self.Test_name)
        self.jutil.set_values_list(self.data["travelers"][0], ["approvalNo", "approvalId"],
                                   ["S202003030002", "203548167231377408"])
        # 预期结果
        self.expected_result = "code = 99 / 审批单号不存在"
        # 实际结果
        response = self.Send.urlHeaderData(self.url, self.header, self.data)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 99)
        self.assertIn("不存在", response.json()["message"])
        self.test_result = "Pass"

    # 用例15--因私-- 正常下单（带发票）
    def test_search_case15(self):
        """因私-- 正常下单（带发票）"""
        self.Test_name = '用例15--因私-- 正常下单（带发票）'
        self.logger.info(self.Test_name)
        # 预期结果
        self.expected_result = "code = 0 / OrderId"
        # 实际结果
        response = self.Send.urlHeaderData(self.url, self.header, self.data)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 0)
        self.assertEqual(response.json()["message"], "OK")
        self.test_result = "Pass"

    # 用例16--因私-- 正常下单（不带发票）
    def test_search_case16(self):
        """因私-- 正常下单（不带发票）"""
        self.Test_name = '用例16--因私-- 正常下单（不带发票）'
        self.logger.info(self.Test_name)
        self.jutil.set_values(self.privateData, "needInvoice", "false")
        # 预期结果
        self.expected_result = "code = 0 / OrderId"
        # 实际结果
        response = self.Send.urlHeaderData(self.url, self.header, self.data)
        self.response = response.json()
        # 断言
        self.assertEqual(response.json()["code"], 0)
        self.assertEqual(response.json()["message"], "OK")
        self.test_result = "Pass"


# # 用例12--通用-- 城市信息为空
# def test_search_case12(self):
#     self.Test_name = '用例10 --酒店下单 --城市信息为空 '
#     self.logger.info(self.Test_name)
#     data = self.data
#     self.jutil.set_values(data, "cityCode", "")
#     response = common_book.Common().common(data, self.header, self.url)
#     self.response = response.json()
#     self.expected_result = "code = 0 / OrderId"
#     # 断言
#     self.assertEqual(response.json()["code"], 0)
#     self.assertIn("OK", response.json()["message"])
#     self.test_result = "Pass"
#
# # 用例13--通用-- 酒店信息为空
# def test_search_case13(self):
#     self.Test_name = '用例11 --酒店下单 --酒店信息为空 '
#     self.logger.info(self.Test_name)
#     data = self.data
#     self.jutil.set_values(data, "hotelCode", "")
#     response = common_book.Common().common(self.data, self.header, self.url)
#     self.response = response.json()
#     self.expected_result = "code = 98 / 酒店code不能为空"
#     # 断言
#     self.assertEqual(response.json()["code"], 98)
#     self.assertIn("不能为空", response.json()["message"])
#     self.test_result = "Pass"
#     # 用例11-- 酒店信息为空
#
# # 用例14--通用-- 房型信息为空
# def test_search_case14(self):
#     self.Test_name = '用例11 --酒店下单 --酒店信息为空 '
#     self.logger.info(self.Test_name)
#     data = self.data
#     self.jutil.set_values(data, "hotelCode", "")
#     response = common_book.Common().common(self.data, self.header, self.url)
#     self.response = response.json()
#     self.expected_result = "code = 98 / 酒店code不能为空"
#     # 断言
#     self.assertEqual(response.json()["code"], 98)
#     self.assertIn("不能为空", response.json()["message"])
#     self.test_result = "Pass"


# TODO:审批单，授权，项目关联，代订权限


if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(testsuite)
