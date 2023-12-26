import unittest
import re
from Common.Base import Base
from Common import operationExcel, Log
from Utils import JsonPathUtil
from ApiData.UrlHeaderData import UrlHeaderData
from TestCase.TestCase_flight.FlightProcess import FlightProcess
from Config.ReadConfig import readconfig

'''
下单
'''
status = str(readconfig().get_status("status"))


class TestPlaceFlight(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.logger = Log.log("test_login").logger
        cls.operateExcel = operationExcel.operationExcel(readconfig().get_table_name("flight"), "place")
        cls.url = readconfig().get_flight_url("place")
        Base().Customer_login()
        cls.api = UrlHeaderData()

    def setUp(self):
        # 获取token
        self.placeData = FlightProcess().get_place_data()
        login_response = Base().Customer_login()
        self.token = JsonPathUtil.jsonpath_util().get_values(login_response, "token")[0]
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

    # 用例1--正常下单
    @unittest.skipIf(status=='200', "产生数据：用例1--正常下单")
    def test_place_case01(self):
        """正常下单"""
        self.logger.info('国内机票下单--用例01--正常下单')
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}",self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例2--联系人电话正确
    @unittest.skipIf(status=='200', "产生数据：用例2--联系人电话正确")
    def test_place_case02(self):
        """联系人电话正确"""
        self.logger.info('国内机票下单--用例02--联系人电话正确')
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例3--联系人电话为空
    def test_place_case03(self):
        """联系人电话为空"""
        self.logger.info('国内机票下单--用例03--联系人电话为空')
        self.placeData["contact"]["mobile"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("联系人手机", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例4--联系人电话数据无效
    @unittest.skipIf(status=='200', "产生数据：用例4--联系人电话数据无效--未校验")
    def test_place_case04(self):
        """联系人电话数据无效"""
        self.logger.info('国内机票下单--用例04--联系人电话无效')
        self.placeData["contact"]["mobile"] = "gaeg124"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("联系人手机", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例5--联系人姓名正确
    @unittest.skipIf(status=='200', "产生数据：用例5--联系人姓名正确")
    def test_place_case05(self):
        """联系人姓名正确"""
        self.logger.info('国内机票下单--用例05--联系人姓名正确')
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例6--联系人姓名为空
    def test_place_case06(self):
        """联系人姓名为空"""
        self.logger.info('国内机票下单--用例06--联系人姓名为空')
        self.placeData["contact"]["name"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("联系人姓名不能为空", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例7--联系人姓名数据无效
    @unittest.skipIf(status=='200', "产生数据：用例7--联系人姓名数据无效--未校验")
    def test_place_case07(self):
        """联系人姓名数据无效"""
        self.logger.info('国内机票下单--用例07--联系人姓名数据无效')
        self.placeData["contact"]["name"] = "124.、，"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例8--联系人姓名在系统不存在
    @unittest.skipIf(status=='200', "产生数据：用例8--联系人姓名在系统不存在")
    def test_place_case08(self):
        """联系人姓名在系统不存在"""
        self.logger.info('国内机票下单--用例08--联系人姓名不存在')
        self.placeData["contact"]["name"] = "哈哈哈"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例9--配送方式代码post
    @unittest.skipIf(status=='200', "产生数据：用例9--配送方式代码post")
    def test_place_case09(self):
        """配送方式代码post"""
        self.logger.info('国内机票下单--用例09--配送方式代码post')
        self.placeData["distribution"]["distributionMode"] = "Post"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例10--配送方式代码为空
    @unittest.skipIf(status=='200', "产生数据：用例10--配送方式代码为空")
    def test_place_case10(self):
        """配送方式代码为空"""
        self.logger.info('国内机票下单--用例10--配送方式代码为空')
        self.placeData["distribution"]["distributionMode"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例11--配送方式代码无效
    @unittest.skipIf(status=='200', "产生数据：用例11--配送方式代码无效")
    def test_place_case11(self):
        """配送方式代码无效"""
        self.logger.info('国内机票下单--用例11--配送方式代码数据无效')
        self.placeData["distribution"]["distributionMode"] = "123"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例12--操作来源-web
    @unittest.skipIf(status=='200', "产生数据：用例12--操作来源-web")
    def test_place_case12(self):
        """操作来源-web"""
        self.logger.info('国内机票下单--用例12--操作来源web')
        self.placeData["operateSource"] = "Web"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例13--操作来源-ios
    @unittest.skipIf(status=='200', "产生数据：用例13--操作来源-ios")
    def test_place_case13(self):
        """操作来源-ios"""
        self.logger.info('国内机票下单--用例13--操作来源iOS')
        self.placeData["operateSource"] = "Ios"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例14--操作来源-Android
    @unittest.skipIf(status=='200', "产生数据：用例14--操作来源-Android")
    def test_place_case14(self):
        """操作来源-Android"""
        self.logger.info('国内机票下单--用例14--操作来源Android')
        self.placeData["operateSource"] = "Android"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例15--操作来源-Admin
    @unittest.skipIf(status=='200', "产生数据：用例15--操作来源-Admin")
    def test_place_case15(self):
        """操作来源-Admin"""
        self.logger.info('国内机票下单--用例15--操作来源admin')
        self.placeData["operateSource"] = "Admin"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例16--操作来源-空
    def test_place_case16(self):
        """操作来源-空"""
        self.logger.info('国内机票下单--用例16--操作来源为空')
        self.placeData["operateSource"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定操作来源", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例17--操作来源数据无效
    @unittest.skipIf(status=='200', "产生数据：用例17--操作来源数据无效--未校验")
    def test_place_case17(self):
        """操作来源数据无效"""
        self.logger.info('国内机票下单--用例17--操作来源数据无效')
        self.placeData["operateSource"] = "124"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例18--乘机人生日正确
    @unittest.skipIf(status=='200', "产生数据：用例18--乘机人生日正确")
    def test_place_case18(self):
        """乘机人生日正确"""
        self.logger.info('国内机票下单--用例18--乘机人生日正确')
        self.placeData["passengers"][0]["birthday"] = "1997-04-03"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例19--乘机人生日为空
    @unittest.skipIf(status=='200', "产生数据：用例19--乘机人生日为空--未校验")
    def test_place_case19(self):
        """乘机人生日为空"""
        self.logger.info('国内机票下单--用例19--乘机人生日为空')
        self.placeData["passengers"][0]["birthday"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例20--乘机人生日数据无效
    def test_place_case20(self):
        """乘机人生日数据无效"""
        self.logger.info('国内机票下单--用例20--乘机人生日数据无效')
        self.placeData["passengers"][0]["birthday"] = "123555"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("出生日期格式不正确", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例21--乘机人证件号正确
    @unittest.skipIf(status=='200', "产生数据：用例21--乘机人证件号正确")
    def test_place_case21(self):
        """乘机人证件号正确"""
        self.logger.info('国内机票下单--用例21--乘机人证件号正确')
        self.placeData["passengers"][0]["docNo"] = "422801199704033443"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例22--乘机人证件号为空
    def test_place_case22(self):
        """乘机人证件号为空"""
        self.logger.info('国内机票下单--用例22--乘机人证件号为空')
        self.placeData["passengers"][0]["docNo"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定证件号", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例23--乘机人证件号数据无效
    def test_place_case23(self):
        """乘机人证件号数据无效"""
        self.logger.info('国内机票下单--用例23--乘机人证件号数据无效')
        self.placeData["passengers"][0]["docType"] = "IdCard"
        self.placeData["passengers"][0]["docNo"] = "`1234`"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 6, "返回的code不是6，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("身份证号码位数为 18 位", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例24--乘机人证件类型正确
    @unittest.skipIf(status=='200', "产生数据：用例24--乘机人证件类型正确")
    def test_place_case24(self):
        """乘机人证件类型正确"""
        self.logger.info('国内机票下单--用例24--乘机人证件类型正确')
        self.placeData["passengers"][0]["docType"] = "IdCard"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例25--乘机人证件类型为空
    def test_place_case25(self):
        """乘机人证件类型为空"""
        self.logger.info('国内机票下单--用例25--乘机人证件类型为空')
        self.placeData["passengers"][0]["docType"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定证件类型", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例26--乘机人证件类型数据无效
    @unittest.skipIf(status=='200', "产生数据：用例26--乘机人证件类型数据无效")
    def test_place_case26(self):
        """乘机人证件类型数据无效"""
        self.logger.info('国内机票下单--用例26--乘机人证件类型数据无效')
        self.placeData["passengers"][0]["docType"] = "、，。"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例27--乘机人性别-Male
    @unittest.skipIf(status=='200', "产生数据：用例27--乘机人性别-Male")
    def test_place_case27(self):
        """乘机人性别-Male"""
        self.logger.info('国内机票下单--用例27--乘机人证性别为男')
        self.placeData["passengers"][0]["gender"] = "Male"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例28--乘机人性别-Female
    @unittest.skipIf(status=='200', "产生数据：用例28--乘机人性别-Female")
    def test_place_case28(self):
        """乘机人性别-Female"""
        self.logger.info('国内机票下单--用例28--乘机人证性别为女')
        self.placeData["passengers"][0]["gender"] = "Female"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例29--乘机人性别为空
    def test_place_case29(self):
        """乘机人性别为空"""
        self.logger.info('国内机票下单--用例29--乘机人证性别为空')
        self.placeData["passengers"][0]["gender"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定性别", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例30-乘机人性别数据无效
    @unittest.skipIf(status=='200', "产生数据：用例30-乘机人性别数据无效--未校验")
    def test_place_case30(self):
        """乘机人性别数据无效"""
        self.logger.info('国内机票下单--用例30--乘机人证性别数据无效')
        self.placeData["passengers"][0]["gender"] = "123"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例31-乘机人类型-空
    def test_place_case31(self):
        """乘机人类型-空"""
        self.logger.info('国内机票下单--用例31--乘机人类型为空')
        self.placeData["passengers"][0]["passengerType"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("乘机人类型无效", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例32-乘机人类型-Adult
    @unittest.skipIf(status=='200', "产生数据：用例32-乘机人类型-Adult")
    def test_place_case32(self):
        """乘机人类型-Adult"""
        self.logger.info('国内机票下单--用例32--乘机人类型成人')
        self.placeData["passengers"][0]["passengerType"] = "Adult"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例33-乘机人类型-Child
    @unittest.skipIf(status=='200', "产生数据：用例33-乘机人类型-Child")
    def test_place_case33(self):
        """乘机人类型-Child"""
        self.logger.info('国内机票下单--用例33--乘机人类型儿童')
        self.placeData["passengers"][0]["passengerType"] = "Child"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        try:
            self.assertEqual(self.response_code, 6, "返回的code不是6，是{0}，错误内容：{1}".format(self.response_code, self.message))
            self.assertIn("成人", self.response.json()["message"])
        except:
            self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
            self.assertIn("未查询到儿童价格", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例34-乘机人类型-Infant
    @unittest.skipIf(status=='200', "产生数据：用例34-乘机人类型-Infant")
    def test_place_case34(self):
        """乘机人类型-Infant"""
        self.logger.info('国内机票下单--用例34--乘机人类型婴儿')
        self.placeData["passengers"][0]["passengerType"] = "Infant"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        try:
            self.assertEqual(self.response_code, 6, "返回的code不是6，是{0}，错误内容：{1}".format(self.response_code, self.message))
            self.assertIn("成人", self.response.json()["message"])
        except:
            self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
            self.assertIn("未查询到婴儿价格", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例35-乘机人类型数据无效
    def test_place_case35(self):
        """乘机人类型数据无效"""
        self.logger.info('国内机票下单--用例35--乘机人类型数据无效')
        self.placeData["passengers"][0]["passengerType"] = "123"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("乘机人类型无效", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例36-乘机人是否公司员工-true
    @unittest.skipIf(status=='200', "产生数据：用例36-乘机人是否公司员工-true")
    def test_place_case36(self):
        """乘机人是否公司员工-true"""
        self.logger.info('国内机票下单--用例36--乘机人是否公司员工-true')
        self.placeData["passengers"][0]["wasEmployee"] = "true"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例37-乘机人是否公司员工-false
    @unittest.skipIf(status=='200', "产生数据：用例37-乘机人是否公司员工-false")
    def test_place_case37(self):
        """乘机人是否公司员工-false"""
        self.logger.info('国内机票下单--用例37--乘机人是否公司员工-false')
        self.placeData["passengers"][0]["wasEmployee"] = "false"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例38-乘机人是否公司员工-空
    def test_place_case38(self):
        """乘机人是否公司员工-空"""
        self.logger.info('国内机票下单--用例38--乘机人是否公司员工数据为空')
        self.placeData["passengers"][0]["wasEmployee"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定乘机人是否为公司员工", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例39-乘机人是否公司员工-数据无效---预期结果待完善
    def test_place_case39(self):
        """乘机人是否公司员工-数据无效"""
        self.logger.info('国内机票下单--用例39--乘机人是否公司员工数据无效')
        self.placeData["passengers"][0]["wasEmployee"] = "abv"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.assertIn('only "true" or "false"', str(self.response.json()))
        self.test_result = "PASS"

    # 用例40-舱位id-空
    def test_place_case40(self):
        """舱位id-空"""
        self.logger.info('国内机票下单--用例40--舱位id为空')
        self.placeData["routes"][0]["segments"][0]["bunkId"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 1, "返回的code不是1，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("航班价格已过期", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例41-舱位id-不正确
    def test_place_case41(self):
        """舱位id-不正确"""
        self.logger.info('国内机票下单--用例41--舱位id不正确')
        self.placeData["routes"][0]["segments"][0]["bunkId"] = "11111111111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 1, "返回的code不是1，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("航班价格已过期", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例42-航班id-空
    def test_place_case42(self):
        """航班id-空"""
        self.logger.info('国内机票下单--用例42--航班id为空')
        self.placeData["routes"][0]["segments"][0]["flightId"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 1, "返回的code不是1，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("航班价格已过期", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例43-航班id-不正确
    def test_place_case43(self):
        """航班id-不正确"""
        self.logger.info('国内机票下单--用例43--航班id不正确')
        self.placeData["routes"][0]["segments"][0]["flightId"] = "352135313515"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 1, "返回的code不是1，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("航班价格已过期", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例44-航班列表id-空
    def test_place_case44(self):
        """航班列表id-空"""
        self.logger.info('国内机票下单--用例44--航班列表id为空')
        self.placeData["routes"][0]["segments"][0]["flightsId"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 1, "返回的code不是1，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("航班价格已过期", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例45-航班列表id-不正确
    def test_place_case45(self):
        """航班列表id-不正确"""
        self.logger.info('国内机票下单--用例45--航班列表id不正确')
        self.placeData["routes"][0]["segments"][0]["flightsId"] = "352135313515"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 1, "返回的code不是1，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("航班价格已过期", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例46-乘机人姓名-正确
    @unittest.skipIf(status=='200', "产生数据：用例46-乘机人姓名-正确")
    def test_place_case46(self):
        """乘机人姓名-正确"""
        self.logger.info('国内机票下单--用例46--乘机人姓名正确')
        self.placeData["passengers"][0]["passengerName"] = "谭春节"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例47-乘机人姓名-不存在
    @unittest.skipIf(status=='200', "产生数据：用例47-乘机人姓名-不存在")
    def test_place_case47(self):
        """乘机人姓名-不存在"""
        self.logger.info('国内机票下单--用例47--乘机人姓名不存在')
        self.placeData["passengers"][0]["passengerName"] = "哈哈哈"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例48-乘机人姓名-空
    def test_place_case48(self):
        """乘机人姓名-空"""
        self.logger.info('国内机票下单--用例48--乘机人姓名为空')
        self.placeData["passengers"][0]["passengerName"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定乘机人姓名", self.response.json()["message"])
        self.test_result = "PASS"

    # 用例49--乘机人姓名-无效数据
    def test_place_case49(self):
        """乘机人姓名-无效数据"""
        self.logger.info('国内机票下单--用例49--乘机人姓名数据无效')
        self.placeData["passengers"][0]["passengerName"] = "·1·、。"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 6, "返回的code不是6，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("新增员工姓名格式有误", self.response.json()["message"])
        self.test_result = "PASS"


if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(testsuite)


