import re
import unittest
from Common.Base import Base
from Common import operationExcel, Log
from Utils import JsonPathUtil
from ApiData.UrlHeaderData import UrlHeaderData
from TestCase.TestCase_train.TrainProcess import TrainProcess
from Config.ReadConfig import readconfig


'''
订火车票
'''

status = str(readconfig().get_status("status"))


class TestPlaceTrain(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger = Log.log("test_login").logger
        cls.url = readconfig().get_train_url("place")
        cls.operateExcel = operationExcel.operationExcel(readconfig().get_table_name("train"), "place")

    def setUp(self):
        # 获取token
        self.jutil = JsonPathUtil.jsonpath_util()
        self.placeData = TrainProcess().get_place_data()
        login_response = Base().Customer_login()
        self.api = UrlHeaderData()
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
    @unittest.skipIf(status=='200', '产生数据：用例1--正常下单')
    def test_place_case01(self):
        """正常下单"""
        self.logger.info('火车票下单--用例01--正常下单')
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例2--联系人电话--正确
    @unittest.skipIf(status=='200', '产生数据：用例2--联系人电话正确')
    def test_place_case02(self):
        """联系人电话正确"""
        self.logger.info('火车票下单--用例02--联系人电话正确')
        self.placeData["contact"]["mobile"] = 15950582102
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例3--联系人电话--空
    def test_place_case03(self):
        """联系人电话为空"""
        self.logger.info('火车票下单--用例03--联系人电话为空')
        self.placeData["contact"]["mobile"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("联系人手机不能为空", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例4--联系人电话--非法数据
    @unittest.skipIf(status=='200', '产生数据：用例4--联系人电话--非法数据--未校验')
    def test_place_case04(self):
        """联系人电话数据无效"""
        self.logger.info('火车票下单--用例04--联系人电话数据非法')
        self.placeData["contact"]["mobile"] = "aaaaaaaaaaa"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例5--联系人姓名--正确
    @unittest.skipIf(status=='200', '产生数据：用例5--联系人姓名--正确')
    def test_place_case05(self):
        """联系人姓名正确"""
        self.logger.info('火车票下单--用例05--联系人姓名正确')
        self.placeData["contact"]["name"] = "谭春节"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例6--联系人姓名--空
    def test_place_case06(self):
        """联系人姓名为空"""
        self.logger.info('火车票下单--用例06--联系人姓名为空')
        self.placeData["contact"]["name"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("联系人姓名不能为空", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例7--联系人姓名--非法数据
    @unittest.skipIf(status=='200', '产生数据：用例7--联系人姓名--非法数据--未校验')
    def test_place_case07(self):
        """联系人姓名数据无效"""
        self.logger.info('火车票下单--用例07--联系人姓名数据非法')
        self.placeData["contact"]["name"] = "+++++"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例8--联系人姓名--不存在
    @unittest.skipIf(status=='200', '产生数据：用例8--联系人姓名--不存在')
    def test_place_case08(self):
        """联系人姓名不存在"""
        self.logger.info('火车票下单--用例05--联系人姓名不存在')
        self.placeData["contact"]["name"] = "王志凯"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例9--操作来源--Web
    @unittest.skipIf(status=='200', '产生数据：用例9--操作来源--Web')
    def test_place_case09(self):
        """操作来源--Web"""
        self.logger.info('火车票下单--用例09--操作来源web')
        self.placeData["operateSource"] = "Web"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例10--操作来源--Ios
    @unittest.skipIf(status=='200', '产生数据：用例10--操作来源--Ios')
    def test_place_case10(self):
        """操作来源--Ios"""
        self.logger.info('火车票下单--用例10--操作来源iOS')
        self.placeData["operateSource"] = "Ios"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例11--操作来源--Android
    @unittest.skipIf(status=='200', '产生数据：用例11--操作来源--Android')
    def test_place_case11(self):
        """操作来源--Android"""
        self.logger.info('火车票下单--用例11--操作来源Android')
        self.placeData["operateSource"] = "Android"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例12--操作来源--Admin
    @unittest.skipIf(status=='200', '产生数据：用例12--操作来源--Admin')
    def test_place_case12(self):
        """操作来源--Admin"""
        self.logger.info('火车票下单--用例12--操作来源Admin')
        self.placeData["operateSource"] = "Admin"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例13--操作来源--空
    @unittest.skipIf(status=='200', '产生数据：用例13--操作来源为空--未校验')
    def test_place_case13(self):
        """操作来源--空"""
        self.logger.info('火车票下单--用例13--操作来源为空')
        self.placeData["operateSource"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例14--操作来源--非法数据
    @unittest.skipIf(status=='200', '产生数据：用例14--操作来源--非法数据--未校验')
    def test_place_case14(self):
        """操作来源--数据无效"""
        self.logger.info('火车票下单--用例14--操作来源数据非法')
        self.placeData["operateSource"] = "111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例15--乘客生日--正确
    @unittest.skipIf(status=='200', '产生数据：用例15--乘客生日--正确')
    def test_place_case15(self):
        """乘客生日--正确"""
        self.logger.info('火车票下单--用例15--乘客生日正确')
        self.placeData["passengers"][0]["birthday"] = "1997-04-03"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例16--乘客生日--空
    def test_place_case16(self):
        """乘客生日--为空"""
        self.logger.info('火车票下单--用例16--乘客生日为空')
        self.placeData["passengers"][0]["birthday"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("出生日期格式不正确", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例17--乘客生日--非法数据
    def test_place_case17(self):
        """乘客生日--数据无效"""
        self.logger.info('火车票下单--用例17--乘客生日数据非法')
        self.placeData["passengers"][0]["birthday"] = "aaaa-bb-cc"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("出生日期格式不正确", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例18--证件号--正确
    @unittest.skipIf(status=='200', '产生数据：用例18--证件号--正确')
    def test_place_case18(self):
        """证件号--正确"""
        self.logger.info('火车票下单--用例18--乘客证件号正确')
        self.placeData["passengers"][0]["docNo"] = "P11111111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例19--证件号--空
    def test_place_case19(self):
        """证件号--空"""
        self.logger.info('火车票下单--用例19--乘客证件号为空')
        self.placeData["passengers"][0]["docNo"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定证件号", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例20--证件号--非法数据
    def test_place_case20(self):
        """证件号--数据无效"""
        self.logger.info('火车票下单--用例20--乘客证件号数据非法')
        self.placeData["passengers"][0]["docType"] = "IdCard"
        self.placeData["passengers"][0]["docNo"] = "aaaaaaaaa"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("身份证号码位数为 18 位", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例21--证件类型--身份证
    @unittest.skipIf(status=='200', '产生数据：用例21--证件类型--身份证')
    def test_place_case21(self):
        """证件类型--身份证"""
        self.logger.info('火车票下单--用例21--乘客证件类型身份证')
        self.placeData["passengers"][0]["docNo"] = "422801199704033443"
        self.placeData["passengers"][0]["docType"] = "IdCard"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例22--证件类型--护照
    @unittest.skipIf(status=='200', '产生数据：用例22--证件类型--护照')
    def test_place_case22(self):
        """证件类型--护照"""
        self.logger.info('火车票下单--用例22--乘客证件类型护照')
        self.placeData["passengers"][0]["docNo"] = "P1111111"
        self.placeData["passengers"][0]["docType"] = "Passport"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例23--证件类型--台胞证
    @unittest.skipIf(status=='200', '产生数据：用例23--证件类型--台胞证')
    def test_place_case23(self):
        """证件类型--台胞证"""
        self.logger.info('火车票下单--用例23--乘客证件类型台胞证')
        self.placeData["passengers"][0]["docNo"] = "A123456789"
        self.placeData["passengers"][0]["docType"] = "TaiwanCard"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例24--证件类型--港澳通行证
    def test_place_case24(self):
        """证件类型--港澳通行证"""
        self.logger.info('火车票下单--用例24--乘客证件类型港澳通行证')
        self.placeData["passengers"][0]["docNo"] = "23456789"
        self.placeData["passengers"][0]["docType"] = "HKMAPassCard"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("身份证，护照，台胞证，回乡证购票", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例25--证件类型--空
    def test_place_case25(self):
        """证件类型--空"""
        self.logger.info('火车票下单--用例25--乘客证件类型为空')
        self.placeData["passengers"][0]["docType"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定证件类型", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例26--证件类型--非法数据
    def test_place_case26(self):
        """证件类型--数据无效"""
        self.logger.info('火车票下单--用例26--乘客证件类型数据非法')
        self.placeData["passengers"][0]["docType"] = "aaa"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("只能使用身份证，护照，台胞证，回乡证购票", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例27--乘客性别--Male
    @unittest.skipIf(status=='200', '产生数据：用例27--乘客性别--Male')
    def test_place_case27(self):
        """乘客性别--Male"""
        self.logger.info('火车票下单--用例27--乘客性别男')
        self.placeData["passengers"][0]["gender"] = "Male"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例28--乘客性别--Female
    @unittest.skipIf(status=='200', '产生数据：用例28--乘客性别--Female')
    def test_place_case28(self):
        """乘客性别--Female"""
        self.logger.info('火车票下单--用例28--乘客性别女')
        self.placeData["passengers"][0]["gender"] = "Female"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例29--乘客性别--空
    def test_place_case29(self):
        """乘客性别--空"""
        self.logger.info('火车票下单--用例29--乘客性别为空')
        self.placeData["passengers"][0]["gender"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("性别只能是Male/Female", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例30--乘客性别--数据非法
    def test_place_case30(self):
        """乘客性别--数据无效"""
        self.logger.info('火车票下单--用例30--乘客性别数据非法')
        self.placeData["passengers"][0]["gender"] = "123"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("性别只能是Male/Female", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例31--乘客姓名--正确
    @unittest.skipIf(status=='200', '产生数据：用例31--乘客姓名--正确')
    def test_place_case31(self):
        """乘客姓名--正确"""
        self.logger.info('火车票下单--用例31--乘客姓名正确')
        self.placeData["passengers"][0]["passengerName"] = "谭春节"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例32--乘客姓名--不存在
    @unittest.skipIf(status=='200', '产生数据：用例32--乘客姓名--不存在')
    def test_place_case32(self):
        """乘客姓名--不存在"""
        self.logger.info('火车票下单--用例32--乘客姓名不存在')
        self.placeData["passengers"][0]["passengerName"] = "安安"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例33--乘客姓名--空
    def test_place_case33(self):
        """乘客姓名--空"""
        self.logger.info('火车票下单--用例33--乘客姓名为空')
        self.placeData["passengers"][0]["passengerName"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定乘客姓名", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例34--乘客姓名--数据不合法
    def test_place_case34(self):
        """乘客姓名--数据不合法"""
        self.logger.info('火车票下单--用例34--乘客姓名数据不合法')
        self.placeData["passengers"][0]["passengerName"] = "-------"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("中国护照必须使用中文名下单", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例35--乘客类型--Adult
    @unittest.skipIf(status=='200', '产生数据：用例35--乘客类型--Adult')
    def test_place_case35(self):
        """乘客类型--Adult"""
        self.logger.info('火车票下单--用例35--乘客类型成人')
        self.placeData["passengers"][0]["passengerType"] = "Adult"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例36--乘客类型--Child
    @unittest.skipIf(status=='200', '产生数据：用例36--乘客类型--Child')
    def test_place_case36(self):
        """乘客类型--Child"""
        self.logger.info('火车票下单--用例36--乘客类型儿童')
        self.placeData["passengers"][0]["passengerType"] = "Child"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例37--乘客类型--Infant
    def test_place_case37(self):
        """乘客类型--Infant"""
        self.logger.info('火车票下单--用例37--乘客类型婴儿')
        self.placeData["passengers"][0]["passengerType"] = "Infant"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("只支持成人票和儿童票", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例38--乘客类型--空
    def test_place_case38(self):
        """乘客类型--空"""
        self.logger.info('火车票下单--用例38--乘客类型为空')
        self.placeData["passengers"][0]["passengerType"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("只支持成人票和儿童票", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例39--乘客类型--非法数据
    def test_place_case39(self):
        """乘客类型--非法数据"""
        self.logger.info('火车票下单--用例39--乘客类型数据非法')
        self.placeData["passengers"][0]["passengerType"] = "111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("只支持成人票和儿童票", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例40--乘客是否公司员工--true
    @unittest.skipIf(status=='200', '产生数据：用例40--乘客是否公司员工--true')
    def test_place_case40(self):
        """乘客是否公司员工--true"""
        self.logger.info('火车票下单--用例40--乘客是否公司员工--true')
        self.placeData["passengers"][0]["wasEmployee"] = "true"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例41--乘客是否公司员工--false
    @unittest.skipIf(status=='200', '产生数据：用例41--乘客是否公司员工--false')
    def test_place_case41(self):
        """乘客是否公司员工--false"""
        self.logger.info('火车票下单--用例41--乘客是否公司员工--false')
        self.placeData["passengers"][0]["wasEmployee"] = "false"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例42--乘客是否公司员工--空
    @unittest.skipIf(status=='200', '产生数据：用例42--乘客是否公司员工为空--未校验')
    def test_place_case42(self):
        """乘客是否公司员工--空"""
        self.logger.info('火车票下单--用例42--乘客是否公司员工为空')
        self.placeData["passengers"][0]["wasEmployee"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例43--乘客是否公司员工--非法数据
    @unittest.skipIf(status=='200', '产生数据：用例43--乘客是否公司员工数据非法--未校验')
    def test_place_case43(self):
        """乘客是否公司员工--非法数据"""
        self.logger.info('火车票下单--用例43--乘客是否公司员工数据非法')
        self.placeData["passengers"][0]["wasEmployee"] = "1111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例44--出发站--正确
    @unittest.skipIf(status=='200', '产生数据：用例44--出发站--正确')
    def test_place_case44(self):
        """出发站--正确"""
        self.logger.info('火车票下单--用例44--出发站正确')
        self.placeData["route"]["fromStation"] = "SZQ"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例45--出发站--空
    def test_place_case45(self):
        """出发站--空"""
        self.logger.info('火车票下单--用例45--出发站为空')
        self.placeData["route"]["fromStation"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("出发站不能为空", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例46--出发站--三字码不存在
    @unittest.skipIf(status=='200', '产生数据：用例46--出发站--三字码不存在--未校验')
    def test_place_case46(self):
        """出发站--三字码不存在"""
        self.logger.info('火车票下单--用例46--出发站三字码不存在')
        self.placeData["route"]["fromStation"] = "ZZZ"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例47--出发站--三字码数据非法
    @unittest.skipIf(status=='200', '产生数据：用例47--出发站--三字码数据非法--未校验')
    def test_place_case47(self):
        """出发站--三字码数据无效"""
        self.logger.info('火车票下单--用例47--出发站三字码数据非法')
        self.placeData["route"]["fromStation"] = "123"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例48--车次列表查询id--正确
    @unittest.skipIf(status=='200', '产生数据：用例48--车次列表查询id--正确')
    def test_place_case48(self):
        """车次列表查询id--正确"""
        self.logger.info('火车票下单--用例48--车次列表查询id正确')
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例49--车次列表查询id--空
    def test_place_case49(self):
        """车次列表查询id--空"""
        self.logger.info('火车票下单--用例49--车次列表查询id为空')
        self.placeData["route"]["queryId"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定车次列表id", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例50--车次列表查询id--错误数据
    def test_place_case50(self):
        """车次列表查询id--错误数据"""
        self.logger.info('火车票下单--用例50--车次列表查询id数据错误')
        self.placeData["route"]["queryId"] = "58a77558-3a3e-4e18-bca3-bf6ee1111111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 3, "返回的code不是3，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("车次信息已过期，请重新查询", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例51--坐席类型--正确
    @unittest.skipIf(status=='200', '产生数据：用例51--坐席类型--正确')
    def test_place_case51(self):
        """坐席类型--正确"""
        self.logger.info('火车票下单--用例51--坐席类型正确')
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例52--坐席类型--空
    def test_place_case52(self):
        """坐席类型--空"""
        self.logger.info('火车票下单--用例52--坐席类型为空')
        self.placeData["route"]["seatType"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定坐席类型", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例53--坐席类型--数据无效
    def test_place_case53(self):
        """坐席类型--数据无效"""
        self.logger.info('火车票下单--用例53--坐席类型数据无效')
        self.placeData["route"]["seatType"] = "seat"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("坐席不可用", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例54--到达站--正确
    @unittest.skipIf(status=='200', '产生数据：用例54--到达站--正确')
    def test_place_case54(self):
        """到达站--正确"""
        self.logger.info('火车票下单--用例54--到达站正确')
        self.placeData["route"]["toStation"] = "WHN"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例55--到达站--空
    def test_place_case55(self):
        """到达站--空"""
        self.logger.info('火车票下单--用例55--到达站为空')
        self.placeData["route"]["toStation"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("到达站不能为空", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例56--到达站--三字码不存在
    @unittest.skipIf(status=='200', '产生数据：用例56--到达站--三字码不存在--未校验')
    def test_place_case56(self):
        """到达站--三字码不存在"""
        self.logger.info('火车票下单--用例56--到达站三字码不存在')
        self.placeData["route"]["toStation"] = "ZZZ"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例57--到达站--三字码非法
    @unittest.skipIf(status=='200', '产生数据：用例57--到达站--三字码非法--未校验')
    def test_place_case57(self):
        """到达站--三字码无效"""
        self.logger.info('火车票下单--用例57--到达站三字码非法')
        self.placeData["route"]["toStation"] = "111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例58--车次号--正确
    @unittest.skipIf(status=='200', '产生数据：用例58--车次号--正确')
    def test_place_case58(self):
        """车次号--正确"""
        self.logger.info('火车票下单--用例58--车次号正确')
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例59--车次号--空
    def test_place_case59(self):
        """车次号--空"""
        self.logger.info('火车票下单--用例59--车次号为空')
        self.placeData["route"]["trainNo"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("车次号不能为空", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例60--车次号--不正确
    def test_place_case60(self):
        """车次号--不正确"""
        self.logger.info('火车票下单--用例60--车次号不正确')
        self.placeData["route"]["trainNo"] = "1314"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("车次不存在", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例61--出差类型--OnPrivate
    @unittest.skipIf(status=='200', '产生数据：用例61--出差类型--OnPrivate')
    def test_place_case61(self):
        """出差类型--OnPrivate"""
        self.logger.info('火车票下单--用例61--出差类型因私')
        self.placeData["travelType"] = "OnPrivate"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例62--出差类型--OnBusiness
    @unittest.skipIf(status=='200', '产生数据：用例62--出差类型--OnBusiness')
    def test_place_case62(self):
        """出差类型--OnBusiness"""
        self.logger.info('火车票下单--用例62--出差类型因公')
        self.placeData["travelType"] = "OnBusiness"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    # 用例63--出差类型--空
    def test_place_case63(self):
        """出差类型--空"""
        self.logger.info('火车票下单--用例63--出差类型为空')
        self.placeData["travelType"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定出差类型", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例64--出差类型--非法数据
    def test_place_case64(self):
        """出差类型--无效数据"""
        self.logger.info('火车票下单--用例64--出差类型数据非法')
        self.placeData["travelType"] = "1111111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("出差类型必须是因公或因私", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    # 用例65--证件类型与证件号不匹配（证件为身份证，证件号码是护照号）
    def test_place_case65(self):
        """证件类型与证件号不匹配（证件为身份证，证件号码是护照号）"""
        self.logger.info('火车票下单--用例65--证件为身份证，证件号码是护照号')
        self.placeData["passengers"][0]["docNo"] = "P1111111"
        self.placeData["passengers"][0]["docType"] = "IdCard"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("身份证号码位数为 18 位", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例66--身份证号码格式错误
    def test_place_case66(self):
        """份证号码格式错误"""
        self.logger.info('火车票下单--用例66--身份证号码格式错误')
        self.placeData["passengers"][0]["docNo"] = "111111111111111111"
        self.placeData["passengers"][0]["docType"] = "IdCard"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("身份证号码校验不通过", str(self.response.json()["message"]))
        self.test_result = "PASS"

    # 用例67--他人身份证号
    def test_place_case67(self):
        """他人身份证号"""
        self.logger.info('火车票下单--用例67--他人身份证号')
        self.placeData["passengers"][0]["docNo"] = "422801199001031001"
        self.placeData["passengers"][0]["docType"] = "IdCard"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.placeData)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("身份证号码校验不通过", str(self.response.json()["message"]))
        self.test_result = "PASS"


if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(testsuite)

