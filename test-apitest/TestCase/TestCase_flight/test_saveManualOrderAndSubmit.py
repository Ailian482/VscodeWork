import unittest, random, datetime, time
from Common.Base import Base
from Common import operationExcel, Log
from Utils import JsonPathUtil, JsonUtil
from ApiData.UrlHeaderData import UrlHeaderData
from Config.ReadConfig import readconfig

status = str(readconfig().get_status("status"))


class TestSaveManualOrderAndSubmit(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger = Log.log("test_login").logger
        cls.operateExcel = operationExcel.operationExcel(readconfig().get_table_name("flight"), "saveManualOrderAndSubmit")
        cls.url = readconfig().get_flight_url("saveManualOrderAndSubmit")

    def setUp(self) -> None:
        self.jutil = JsonPathUtil.jsonpath_util()
        self.data = self.get_build_data()
        login_response = Base().Staff_login()
        self.api = UrlHeaderData('Staff_url')
        self.token = self.jutil.get_values(login_response, "token")[0]
        self.headers = {"Content-Type": "application/json", "Authorization": "Bearer {0}".format(self.token)}
        self.test_result = "FAIL"
        self.message = ""
        self.response_code = 0

    def tearDown(self) -> None:
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

    def get_build_data(self):
        build_data = JsonUtil.OperetionJson("flight.json").get_data("saveManualOrderAndSubmit")
        cur_time = datetime.datetime.utcfromtimestamp(time.time())
        build_data["bookingInfo"]["bookingTime"] = str(cur_time)
        dep_time = (datetime.datetime.now() + datetime.timedelta(days=+random.randint(0, 365), hours=random.randint(0, 24),
                                                        minutes=random.randint(0, 60))).strftime("%Y-%m-%d %H:%M")
        stu = datetime.datetime.strptime(dep_time, "%Y-%m-%d %H:%M")
        arr_time = (stu + datetime.timedelta(days=+random.randint(0, 1), hours=random.randint(0, 24),
                                    minutes=random.randint(0, 60))).strftime("%Y-%m-%d %H:%M")
        build_data["segment"]["arrivalDateTime"] = arr_time
        build_data["segment"]["departureDateTime"] = dep_time
        return build_data

    def test_saveManualOrderAndSubmit_case01(self):
        """正常保存"""
        self.logger.info('国内机票编单--用例01--正常保存')
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue("ok",self.response.json()["data"])
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case02(self):
        """预订人员工id--空"""
        self.logger.info('国内机票编单--用例02--预订人员工id--空')
        self.data["bookingInfo"]["bookingEmployeeId"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定预定人员工id", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case03(self):
        """预订人员工id--不存在"""
        self.logger.info('国内机票编单--用例03--预订人员工id--不存在')
        self.data["bookingInfo"]["bookingEmployeeId"] = "111111111106718976"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 6, "返回的code不是6，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("员工不存在", str(self.response.json()["message"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case04(self):
        """预订人姓名--空"""
        self.logger.info('国内机票编单--用例04--预订人姓名--空')
        self.data["bookingInfo"]["bookingEmployeeName"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定预订人员工姓名", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case05(self):
        """代订人id--空"""
        self.logger.info('国内机票编单--用例05--代订人id--空')
        self.data["bookingInfo"]["bookingStaffId"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定代订人id", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case06(self):
        """代订人id--不存在"""
        self.logger.info('国内机票编单--用例06--代订人id--不存在')
        self.data["bookingInfo"]["bookingStaffId"] = "00000"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 5, "返回的code不是5，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("后台员工不存在", str(self.response.json()["message"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case07(self):
        """联系人手机--空"""
        self.logger.info('国内机票编单--用例07--联系人手机--空')
        self.data["contactInfo"]["contactMobile"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定联系人手机", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case08(self):
        """联系人姓名--空"""
        self.logger.info('国内机票编单--用例08--联系人姓名--空')
        self.data["contactInfo"]["contactName"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定联系人姓名", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case09(self):
        """公司id--空"""
        self.logger.info('国内机票编单--用例09--公司id--空')
        self.data["corpId"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定公司id", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case10(self):
        """公司id--不存在"""
        self.logger.info('国内机票编单--用例10--公司id--不存在')
        self.data["corpId"] = "111111111111111111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 7, "返回的code不是7，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("公司不存在", str(self.response.json()["message"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case11(self):
        """证件号码--空"""
        self.logger.info('国内机票编单--用例11--证件号码--空')
        self.data["passengers"][0]["docNo"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("证件号码不为空", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case12(self):
        """证件号码--身份证号格式不对"""
        self.logger.info('国内机票编单--用例12--证件号码--身份证号格式不对')
        self.data["passengers"][0]["docNo"] = "12312312222222"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("length", str(self.response.json()["message"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case13(self):
        """证件类型--空"""
        self.logger.info('国内机票编单--用例13--证件类型--空')
        self.data["passengers"][0]["docType"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("证件类型不为空", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case14(self):
        """乘机人姓名--空"""
        self.logger.info('国内机票编单--用例14--乘机人姓名--空')
        self.data["passengers"][0]["passengerName"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("乘机人不为空", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case15(self):
        """乘机人类型--空"""
        self.logger.info('国内机票编单--用例15--乘机人类型--空')
        self.data["passengers"][0]["passengerType"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定乘机人类型", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case16(self):
        """乘机人类型--不存在"""
        self.logger.info('国内机票编单--用例16--乘机人类型--不存在')
        self.data["passengers"][0]["passengerType"] = "123"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("乘机人类型无效", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case17(self):
        """票号--空"""
        self.logger.info('国内机票编单--用例17--票号--空')
        self.data["passengers"][0]["ticketNo"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("票号不为空", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case18(self):
        """票号--格式不正确"""
        self.logger.info('国内机票编单--用例18--票号--格式不正确')
        self.data["passengers"][0]["ticketNo"] = "123"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("请输入正确的票号", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case19(self):
        """航空公司二字码--空"""
        self.logger.info('国内机票编单--用例19--航空公司二字码--空')
        self.data["segment"]["airline"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("请输入正确的航司二字码", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case20(self):
        """航空公司短名称--空"""
        self.logger.info('国内机票编单--用例20--航空公司短名称--空')
        self.data["segment"]["airlineName"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定航司短名称", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case21(self):
        """机建费--空"""
        self.logger.info('国内机票编单--用例21--机建费--空')
        self.data["segment"]["airportFee"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未填写机建费", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case22(self):
        """机建费--非数字"""
        self.logger.info('国内机票编单--用例21--机建费--非数字')
        self.data["segment"]["airportFee"] = "AA"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn("not a valid representation", str(self.message))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case23(self):
        """到达机场代码--空"""
        self.logger.info('国内机票编单--用例23--到达机场代码--空')
        self.data["segment"]["arrivalAirportCode"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定到达机场代码", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case24(self):
        """到达机场代码--空"""
        self.logger.info('国内机票编单--用例24--到达机场代码--空')
        self.data["segment"]["arrivalAirportName"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定到达机场短名称", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case25(self):
        """到达城市三字码--空"""
        self.logger.info('国内机票编单--用例25--到达城市三字码--空')
        self.data["segment"]["arrivalCityCode"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定到达城市三字码", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case26(self):
        """到达城市名称--空"""
        self.logger.info('国内机票编单--用例26--到达城市名称--空')
        self.data["segment"]["arrivalCityName"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定到达城市", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case27(self):
        """到达日期--空"""
        self.logger.info('国内机票编单--用例27--到达日期--空')
        self.data["segment"]["arrivalDateTime"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定到达日期", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case28(self):
        """舱位类型--空"""
        self.logger.info('国内机票编单--用例28--舱位类型--空')
        self.data["segment"]["bunkType"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定舱位类型", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case29(self):
        """是否允许改签--空"""
        self.logger.info('国内机票编单--用例29--是否允许改签--空')
        self.data["segment"]["changeAllowed"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未说明是否允许改签", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case30(self):
        """是否允许改签--非bool值"""
        self.logger.info('国内机票编单--用例30--是否允许改签--非bool值')
        self.data["segment"]["changeAllowed"] = "1"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn('only "true" or "false" recognized', str(self.message))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case31(self):
        """复核通过后是否自动发送出票通知--空"""
        self.logger.info('国内机票编单--用例31--复核通过后是否自动发送出票通知--空')
        self.data["contactInfo"]["receiveTicketingNotify"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定是否再复核通过后发送出票通知", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case32(self):
        """复核通过后是否自动发送出票通知--非bool值"""
        self.logger.info('国内机票编单--用例32--复核通过后是否自动发送出票通知--非bool值')
        self.data["contactInfo"]["receiveTicketingNotify"] = "1"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn('only "true" or "false" recognized', str(self.message))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case33(self):
        """出发机场代码--空"""
        self.logger.info('国内机票编单--用例33--出发机场代码--空')
        self.data["segment"]["departureAirportCode"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("请输入正确的机场三字码", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case34(self):
        """出发机场短名称--空"""
        self.logger.info('国内机票编单--用例34--出发机场短名称--空')
        self.data["segment"]["departureAirportName"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定出发机场短名称", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case35(self):
        """出发城市三字码--空"""
        self.logger.info('国内机票编单--用例35--出发城市三字码--空')
        self.data["segment"]["departureCityCode"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("请输入正确的城市三字码", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case36(self):
        """出发城市名称--空"""
        self.logger.info('国内机票编单--用例36--出发城市名称--空')
        self.data["segment"]["departureCityName"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定出发城市", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case37(self):
        """出发日期--空"""
        self.logger.info('国内机票编单--用例37--出发日期--空')
        self.data["segment"]["departureDateTime"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定出发日期时间", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case38(self):
        """折扣--空"""
        self.logger.info('国内机票编单--用例38--折扣--空')
        self.data["segment"]["discount"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定折扣", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case39(self):
        """折扣--大于10"""
        self.logger.info('国内机票编单--用例39--折扣--大于10')
        self.data["segment"]["discount"] = "11"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("折扣不能超过10", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case40(self):
        """折扣--小于0"""
        self.logger.info('国内机票编单--用例40--折扣--小于0')
        self.data["segment"]["discount"] = "-1"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("折扣不能小于0", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case41(self):
        """折扣--非数字"""
        self.logger.info('国内机票编单--用例41--折扣--非数字')
        self.data["segment"]["discount"] = "A"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn("not a valid representation", str(self.message))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case42(self):
        """航班号--空"""
        self.logger.info('国内机票编单--用例42--航班号--空')
        self.data["segment"]["flightNo"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("航班号不能为空", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case43(self):
        """航班号--格式错误"""
        self.logger.info('国内机票编单--用例43--航班号--格式错误')
        self.data["segment"]["flightNo"] = "123"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("请传入正确航班号", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case44(self):
        """燃油费--空"""
        self.logger.info('国内机票编单--用例44--燃油费--空')
        self.data["segment"]["oilFee"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未填写燃油费", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case45(self):
        """燃油费--非数字"""
        self.logger.info('国内机票编单--用例45--燃油费--非数字')
        self.data["segment"]["oilFee"] = "A"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn("not a valid representation", str(self.message))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case46(self):
        """票面价--空"""
        self.logger.info('国内机票编单--用例46--燃油费--空')
        self.data["segment"]["ticketPrice"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未填写票面价", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case47(self):
        """票面价--非数字"""
        self.logger.info('国内机票编单--用例47--燃油费--非数字')
        self.data["segment"]["ticketPrice"] = "A"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn("not a valid representation", str(self.message))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case48(self):
        """经停次数--空"""
        self.logger.info('国内机票编单--用例48--燃油费--空')
        self.data["segment"]["stops"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("经停次数必填", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case49(self):
        """经停次数--非数字"""
        self.logger.info('国内机票编单--用例49--经停次数--非数字')
        self.data["segment"]["stops"] = "A"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn("not a valid Integer value", str(self.message))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case50(self):
        """经停次数--小数"""
        self.logger.info('国内机票编单--用例50--经停次数--小数')
        self.data["segment"]["stops"] = "1.4"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.logger.info("错误内容：{0}".format(self.message))
        self.assertIn("not a valid Integer value", str(self.message))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case51(self):
        """机票供应商--空"""
        self.logger.info('国内机票编单--用例51--机票供应商--空')
        self.data["supplier"]["supplier"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定供应商", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case52(self):
        """供应商支付方式--空"""
        self.logger.info('国内机票编单--用例52--供应商支付方式--空')
        self.data["supplier"]["supplierPaymentMode"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定供应商支付方式", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_saveManualOrderAndSubmit_case53(self):
        """出差类型--不存在的类型"""
        self.logger.info('国内机票编单--用例53--出差类型--不存在的类型')
        self.data["travelType"] = "AAA"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("出差类型必须是OnBusiness或OnPrivate", str(self.response.json()["errors"]))
        self.test_result = "PASS"

if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(testsuite)

