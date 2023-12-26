import re
import unittest
from Common.Base import Base
from Common import operationExcel, Log
from Utils import JsonPathUtil
from ApiData.UrlHeaderData import UrlHeaderData
from TestCase.TestCase_intflight.IntflightProcess import IntflightProcess
from Config.ReadConfig import readconfig

status = str(readconfig().get_status("status"))


class TestIntflightBuild(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger = Log.log("test_login").logger
        cls.operateExcel = operationExcel.operationExcel(readconfig().get_table_name("intflight"), "build")
        cls.url = readconfig().get_intflight_url("build")

    def setUp(self) -> None:
        self.jutil = JsonPathUtil.jsonpath_util()
        self.data = IntflightProcess().get_build_data()
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
        row_number = int(self.id()[-3:])

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

    @unittest.skipIf(status=='200', "产生数据：用例001--正常编单")
    def test_build_case001(self):
        """正常编单"""
        self.logger.info('国际机票编单--用例001--正常编单')
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}",self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例002--编单方式--ByPnr")
    def test_build_case002(self):
        """编单方式--ByPnr"""
        self.logger.info('国际机票编单--用例002--编单方式--ByPnr')
        self.data["buildType"] = "ByPnr"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}",self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例003--编单方式--Manual")
    def test_build_case003(self):
        """编单方式--Manual"""
        self.logger.info('国际机票编单--用例003--编单方式--Manual')
        self.data["buildType"] = "Manual"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}",self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用用例004--行程类型--OneWay")
    def test_build_case004(self):
        """行程类型--OneWay"""
        self.logger.info('国际机票编单--用例004--行程类型--OneWay')
        self.data["routeType"] = "OneWay"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}",self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例005--行程类型--RoundTrip")
    def test_build_case005(self):
        """行程类型--RoundTrip"""
        self.logger.info('国际机票编单--用例005--行程类型--RoundTrip')
        self.data["routeType"] = "RoundTrip"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}",self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例006--行程类型--MultiCity")
    def test_build_case006(self):
        """行程类型--MultiCity"""
        self.logger.info('国际机票编单--用例006--行程类型--MultiCity')
        self.data["routeType"] = "MultiCity"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}",self.response.json()["data"]))
        self.test_result = "PASS"

    def test_build_case007(self):
        """航司代码--空"""
        self.logger.info('国际机票编单--用例007--航司代码--空')
        self.data["routes"][0]["segments"][0]["airline"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定航司代码", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例008--航司代码--数据无效--未校验")
    def test_build_case008(self):
        """航司代码--数据无效"""
        self.logger.info('国际机票编单--用例008--航司代码--数据无效')
        self.data["routes"][0]["segments"][0]["airline"] = "11·1"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    def test_build_case009(self):
        """航司名称--空"""
        self.logger.info('国际机票编单--用例009--航司名称--空')
        self.data["routes"][0]["segments"][0]["airlineName"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定航司名称", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例010--航司名称--数据无效--未校验")
    def test_build_case010(self):
        """航司名称--数据无效"""
        self.logger.info('国际机票编单--用例010--航司名称--数据无效')
        self.data["routes"][0]["segments"][0]["airlineName"] = "1111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例011--到达机空场代码--空--未校验")
    def test_build_case011(self):
        """到达机空场代码--空"""
        self.logger.info('国际机票编单--用例011--到达机空场代码--空')
        self.data["routes"][0]["segments"][0]["arrival"]["airportCode"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例012--到达机空场代码--数据无效--未校验")
    def test_build_case012(self):
        """到达机空场代码--数据无效"""
        self.logger.info('国际机票编单--用例012--到达机空场代码--数据无效')
        self.data["routes"][0]["segments"][0]["arrival"]["airportCode"] = "111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例013--到达机空场名称--空--未校验")
    def test_build_case013(self):
        """到达机空场名称--空"""
        self.logger.info('国际机票编单--用例013--到达机空场名称--空')
        self.data["routes"][0]["segments"][0]["arrival"]["airportName"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例014--到达机空场名称--数据无效--未校验")
    def test_build_case014(self):
        """到达机空场名称--数据无效"""
        self.logger.info('国际机票编单--用例014--到达机空场名称--数据无效')
        self.data["routes"][0]["segments"][0]["arrival"]["airportName"] = "111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例015--到达城市代码--空--未校验")
    def test_build_case015(self):
        """到达城市代码--空"""
        self.logger.info('国际机票编单--用例015--到达城市代码--空')
        self.data["routes"][0]["segments"][0]["arrival"]["cityCode"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例016--到达城市代码--无效值--未校验")
    def test_build_case016(self):
        """到达城市代码--无效值"""
        self.logger.info('国际机票编单--用例016--到达城市代码--无效值')
        self.data["routes"][0]["segments"][0]["arrival"]["cityCode"] = "111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例017--到达城市名称--空--未校验")
    def test_build_case017(self):
        """到达城市名称--空"""
        self.logger.info('国际机票编单--用例017--到达城市名称--空')
        self.data["routes"][0]["segments"][0]["arrival"]["cityName"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例018--到达城市名称--无效值--未校验")
    def test_build_case018(self):
        """到达城市名称--无效值"""
        self.logger.info('国际机票编单--用例018--到达城市名称--无效值')
        self.data["routes"][0]["segments"][0]["arrival"]["cityName"] = "111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例019--到达时间--空--未校验")
    def test_build_case019(self):
        """到达时间--空"""
        self.logger.info('国际机票编单--用例019--到达时间--空')
        self.data["routes"][0]["segments"][0]["arrival"]["dateTime"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例020--到达时间--无效值--未校验")
    def test_build_case020(self):
        """到达时间--无效值"""
        self.logger.info('国际机票编单--用例020--到达时间--无效值')
        self.data["routes"][0]["segments"][0]["arrival"]["dateTime"] = "131314"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例021--舱位名称--空-未校验")
    def test_build_case021(self):
        """舱位名称--空"""
        self.logger.info('国际机票编单--用例021--舱位名称--空')
        self.data["routes"][0]["segments"][0]["bunkName"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例022--舱位名称--无效值--未校验")
    def test_build_case022(self):
        """舱位名称--无效值"""
        self.logger.info('国际机票编单--用例022--舱位名称--无效值')
        self.data["routes"][0]["segments"][0]["bunkName"] = "`````"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    def test_build_case023(self):
        """舱位类型--空"""
        self.logger.info('国际机票编单--用例023--舱位类型--空')
        self.data["routes"][0]["segments"][0]["bunkType"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定舱位类型", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例024--舱位类型--无效值--未校验")
    def test_build_case024(self):
        """舱位类型--无效值"""
        self.logger.info('国际机票编单--用例024--舱位类型--无效值')
        self.data["routes"][0]["segments"][0]["bunkName"] = "`````"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例025--是否共享航班--true")
    def test_build_case025(self):
        """是否共享航班--true"""
        self.logger.info('国际机票编单--用例025--是否共享航班--true')
        self.data["routes"][0]["segments"][0]["codeShare"] = "true"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例026--是否共享航班--false")
    def test_build_case026(self):
        """是否共享航班--false"""
        self.logger.info('国际机票编单--用例026--是否共享航班--false')
        self.data["routes"][0]["segments"][0]["codeShare"] = "false"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例027--是否共享航班--空--未校验")
    def test_build_case027(self):
        """是否共享航班--空"""
        self.logger.info('国际机票编单--用例027--是否共享航班--空')
        self.data["routes"][0]["segments"][0]["codeShare"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定是否共享航班", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_build_case028(self):
        """是否共享航班--数据无效"""
        self.logger.info('国际机票编单--用例028--是否共享航班--数据无效')
        self.data["routes"][0]["segments"][0]["codeShare"] = "`122"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.assertIn('only "true" or "false"', str(self.response.json()))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例029--出发机空场代码--空--未校验")
    def test_build_case029(self):
        """出发机空场代码--空"""
        self.logger.info('国际机票编单--用例029--出发机空场代码--空')
        self.data["routes"][0]["segments"][0]["departure"]["airportCode"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例030--出发机空场代码--数据无效--未校验")
    def test_build_case030(self):
        """出发机空场代码--数据无效"""
        self.logger.info('国际机票编单--用例030--出发机空场代码--数据无效')
        self.data["routes"][0]["segments"][0]["departure"]["airportCode"] = "111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例031--出发机空场名称--空--未校验")
    def test_build_case031(self):
        """出发机空场名称--空"""
        self.logger.info('国际机票编单--用例031--出发机空场名称--空')
        self.data["routes"][0]["segments"][0]["departure"]["airportName"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例032--出发机空场名称--数据无效--未校验")
    def test_build_case032(self):
        """出发机空场名称--数据无效"""
        self.logger.info('国际机票编单--用例032--出发机空场名称--数据无效')
        self.data["routes"][0]["segments"][0]["departure"]["airportName"] = "111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例033--出发城市代码--空--未校验")
    def test_build_case033(self):
        """出发城市代码--空"""
        self.logger.info('国际机票编单--用例033--出发城市代码--空')
        self.data["routes"][0]["segments"][0]["departure"]["cityCode"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例034--出发城市代码--无效值--未校验")
    def test_build_case034(self):
        """出发城市代码--无效值"""
        self.logger.info('国际机票编单--用例034--出发城市代码--无效值')
        self.data["routes"][0]["segments"][0]["departure"]["cityCode"] = "111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例1--正常取用例035--出发城市名称--空--未校验")
    def test_build_case035(self):
        """出发城市名称--空"""
        self.logger.info('国际机票编单--用例035--出发城市名称--空')
        self.data["routes"][0]["segments"][0]["departure"]["cityName"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例036--出发城市名称--无效值--未校验")
    def test_build_case036(self):
        """出发城市名称--无效值"""
        self.logger.info('国际机票编单--用例036--出发城市名称--无效值')
        self.data["routes"][0]["segments"][0]["departure"]["cityName"] = "111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例037--出发时间--空--未校验")
    def test_build_case037(self):
        """出发时间--空"""
        self.logger.info('国际机票编单--用例037--出发时间--空')
        self.data["routes"][0]["segments"][0]["departure"]["dateTime"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例038--出发时间--无效值--未校验")
    def test_build_case038(self):
        """出发时间--无效值"""
        self.logger.info('国际机票编单--用例038--出发时间--无效值')
        self.data["routes"][0]["segments"][0]["departure"]["dateTime"] = "131314"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    def test_build_case039(self):
        """航班号--空"""
        self.logger.info('国际机票编单--用例039--航班号--空')
        self.data["routes"][0]["segments"][0]["flightNo"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.assertIn('未指定航班号', str(self.response.json()["errors"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例040--航班号--数据无效--未校验")
    def test_build_case040(self):
        """航班号--数据无效"""
        self.logger.info('国际机票编单--用例040--航班号--数据无效')
        self.data["routes"][0]["segments"][0]["flightNo"] = ",./.,/,/,"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例041--是否有经停--false")
    def test_build_case041(self):
        """是否有经停--false"""
        self.logger.info('国际机票编单--用例041--是否有经停--false')
        self.data["routes"][0]["segments"][0]["hasStops"] = "false"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例042--是否有经停--true")
    def test_build_case042(self):
        """是否有经停--true"""
        self.logger.info('国际机票编单--用例042--是否有经停--true')
        self.data["routes"][0]["segments"][0]["hasStops"] = "true"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    def test_build_case043(self):
        """是否有经停--空"""
        self.logger.info('国际机票编单--用例043--是否有经停--空')
        self.data["routes"][0]["segments"][0]["hasStops"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定是否有经停", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_build_case044(self):
        """是否有经停--数据无效"""
        self.logger.info('国际机票编单--用例044--是否有经停--数据无效')
        self.data["routes"][0]["segments"][0]["hasStops"] = "·12"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.assertIn('only "true" or "false"', str(self.response.json()))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例045--经停机场三字码--空--有经停时未校验")
    def test_build_case045(self):
        """经停机场三字码--空"""
        self.logger.info('国际机票编单--用例045--经停机场三字码--空')
        self.data["routes"][0]["segments"][0]["hasStops"] = "true"
        self.data["routes"][0]["segments"][0]["stops"][0]["airportCode"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例046--经停机场三字码--数据无效--有经停时未校验")
    def test_build_case046(self):
        """经停机场三字码--数据无效"""
        self.logger.info('国际机票编单--用例046--经停机场三字码--数据无效')
        self.data["routes"][0]["segments"][0]["hasStops"] = "true"
        self.data["routes"][0]["segments"][0]["stops"][0]["airportCode"] = "···"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例047--经停到达时间--空--有经停时未校验")
    def test_build_case047(self):
        """经停到达时间--空"""
        self.logger.info('国际机票编单--用例047--经停到达时间--空')
        self.data["routes"][0]["segments"][0]["hasStops"] = "true"
        self.data["routes"][0]["segments"][0]["stops"][0]["arrivalDateTime"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例048--经停到达时间--数据无效--有经停时未校验")
    def test_build_case048(self):
        """经停到达时间--数据无效"""
        self.logger.info('国际机票编单--用例048--经停到达时间--数据无效')
        self.data["routes"][0]["segments"][0]["hasStops"] = "true"
        self.data["routes"][0]["segments"][0]["stops"][0]["arrivalDateTime"] = "aaaaaa"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例049--经停到达时间--空--未校验")
    def test_build_case049(self):
        """经停到达时间--空"""
        self.logger.info('国际机票编单--用例049--经停到达时间--空')
        self.data["routes"][0]["segments"][0]["hasStops"] = "true"
        self.data["routes"][0]["segments"][0]["stops"][0]["departureDateTime"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例050--经停出发时间--数据无效--未校验")
    def test_build_case050(self):
        """经停出发时间--数据无效"""
        self.logger.info('国际机票编单--用例050--经停出发时间--数据无效')
        self.data["routes"][0]["segments"][0]["hasStops"] = "true"
        self.data["routes"][0]["segments"][0]["stops"][0]["departureDateTime"] = "aaaaaa"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    def test_build_case051(self):
        """预定人员id--空"""
        self.logger.info('国际机票编单--用例051--预定人员id--空')
        self.data["bookingInfo"]["bookingEmployeeId"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定预订员人id", str(self.response.json()["message"]))
        self.test_result = "PASS"

    def test_build_case052(self):
        """预定人员id--不存在"""
        self.logger.info('国际机票编单--用例052--预定人员id--不存在')
        self.data["bookingInfo"]["bookingEmployeeId"] = "111111111111111111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("不存在", str(self.response.json()["message"]))
        self.test_result = "PASS"

    def test_build_case053(self):
        """预定人员id--不存在"""
        self.logger.info('国际机票编单--用例053--预定人员id--不存在')
        self.data["bookingInfo"]["bookingEmployeeId"] = "aaaaaaaaaaaaaaaaaa"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("For input string", str(self.response.json()["message"]))
        self.test_result = "PASS"

    def test_build_case054(self):
        """代订人id--空"""
        self.logger.info('国际机票编单--用例054--代订人id--空')
        self.data["bookingInfo"]["bookingStaffId"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定代订人id", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_build_case055(self):
        """代订人id--不存在"""
        self.logger.info('国际机票编单--用例055--代订人id--不存在')
        self.data["bookingInfo"]["bookingStaffId"] = "111111111111111111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("tmc后台员工不存在", str(self.response.json()["message"]))
        self.test_result = "PASS"

    def test_build_case056(self):
        """代订人id--数据无效"""
        self.logger.info('国际机票编单--用例056--代订人id--数据无效')
        self.data["bookingInfo"]["bookingStaffId"] = "qwerasdfghzxcvbn"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("For input string", str(self.response.json()["message"]))
        self.test_result = "PASS"

    def test_build_case057(self):
        """预定时间--空"""
        self.logger.info('国际机票编单--用例057--预定时间--空')
        self.data["bookingInfo"]["bookingTime"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定预订时间", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_build_case058(self):
        """预定时间--数据无效"""
        self.logger.info('国际机票编单--用例058--预定时间--数据无效')
        self.data["bookingInfo"]["bookingTime"] = "aaaa"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 99, "返回的code不是99，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("Invalid format", str(self.response.json()["message"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例059--是否发送出票通知--true")
    def test_build_case059(self):
        """是否发送出票通知--true"""
        self.logger.info('国际机票编单--用例059--是否发送出票通知--true')
        self.data["bookingInfo"]["sendTicketingNotify"] = "true"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例060--是否发送出票通知--false")
    def test_build_case060(self):
        """是否发送出票通知--false"""
        self.logger.info('国际机票编单--用例060--是否发送出票通知--false')
        self.data["bookingInfo"]["sendTicketingNotify"] = "false"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    def test_build_case061(self):
        """是否发送出票通知--空"""
        self.logger.info('国际机票编单--用例061--是否发送出票通知--空')
        self.data["bookingInfo"]["sendTicketingNotify"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定是否发送出票通知", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_build_case062(self):
        """是否发送出票通知--空"""
        self.logger.info('国际机票编单--用例062--是否发送出票通知--空')
        self.data["bookingInfo"]["sendTicketingNotify"] = "aaa"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.assertIn('only "true" or "false"', str(self.response.json()))
        self.test_result = "PASS"

    def test_build_case063(self):
        """联系人电话--空"""
        self.logger.info('国际机票编单--用例063--联系人电话--空')
        self.data["contact"]["mobile"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定联系人手机", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例064--联系人电话--数据无效--未校验")
    def test_build_case064(self):
        """联系人电话--数据无效"""
        self.logger.info('国际机票编单--用例064--联系人电话--数据无效')
        self.data["contact"]["mobile"] = "aaaaaaaaaaaa"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    def test_build_case065(self):
        """联系人姓名--空"""
        self.logger.info('国际机票编单--用例065--联系人姓名--空')
        self.data["contact"]["name"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定联系人姓名", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例066--联系人姓名--数据无效--未校验")
    def test_build_case066(self):
        """联系人姓名--数据无效"""
        self.logger.info('国际机票编单--用例066--联系人姓名--数据无效')
        self.data["contact"]["name"] = "····"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    def test_build_case067(self):
        """乘机人出生日期--空"""
        self.logger.info('国际机票编单--用例067--乘机人出生日期--空')
        self.data["passengers"][0]["doc"]["birthday"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定出生日期", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_build_case068(self):
        """乘机人出生日期--数据无效"""
        self.logger.info('国际机票编单--用例068--乘机人出生日期--数据无效')
        self.data["passengers"][0]["doc"]["birthday"] = "aaaa--aa--aa"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("出生日期格式不正确", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_build_case069(self):
        """乘机人国家二字码--空"""
        self.logger.info('国际机票编单--用例069--乘机人国家二字码--空')
        self.data["passengers"][0]["doc"]["countryCode"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定国家代码", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例070--乘机人国家二字码--数据无效--未校验")
    def test_build_case070(self):
        """乘机人国家二字码--数据无效"""
        self.logger.info('国际机票编单--用例070--乘机人国家二字码--数据无效')
        self.data["passengers"][0]["doc"]["countryCode"] = "·1"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    def test_build_case071(self):
        """证件号--空"""
        self.logger.info('国际机票编单--用例071--证件号--空')
        self.data["passengers"][0]["doc"]["docNo"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定证件号", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例072--证件号--数据无效--未校验")
    def test_build_case072(self):
        """证件号--数据无效"""
        self.logger.info('国际机票编单--用例072--证件号--数据无效')
        self.data["passengers"][0]["doc"]["docNo"] = "~!@#^%$#$^&$^%"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    def test_build_case073(self):
        """证件号--空"""
        self.logger.info('国际机票编单--用例073--证件号--空')
        self.data["passengers"][0]["doc"]["docType"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定证件类型", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例074--证件类型--数据无效--未校验")
    def test_build_case074(self):
        """证件类型--数据无效"""
        self.logger.info('国际机票编单--用例074--证件类型--数据无效')
        self.data["passengers"][0]["doc"]["docType"] = "1111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例075--乘客性别--Female")
    def test_build_case075(self):
        """乘客性别--Female"""
        self.logger.info('国际机票编单--用例075--乘客性别--Female')
        self.data["passengers"][0]["doc"]["gender"] = "Female"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例076--乘客性别--Male")
    def test_build_case076(self):
        """乘客性别--Male"""
        self.logger.info('国际机票编单--用例076--乘客性别--Male')
        self.data["passengers"][0]["doc"]["gender"] = "Male"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    def test_build_case077(self):
        """乘客性别--空"""
        self.logger.info('国际机票编单--用例077--乘客性别--空')
        self.data["passengers"][0]["doc"]["gender"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定性别", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例078--乘客性别--无效值--未校验")
    def test_build_case078(self):
        """乘客性别--无效值"""
        self.logger.info('国际机票编单--用例078--乘客性别--无效值')
        self.data["passengers"][0]["doc"]["gender"] = "1111"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    def test_build_case079(self):
        """乘机人中文姓名--空"""
        self.logger.info('国际机票编单--用例079--乘机人中文姓名--空')
        self.data["passengers"][0]["passengerName"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定乘机人中文姓名", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_build_case080(self):
        """乘机人中文姓名--数据无效"""
        self.logger.info('国际机票编单--用例080--乘机人中文姓名--数据无效')
        self.data["passengers"][0]["passengerName"] = "~！@#4"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("乘客对应员工姓名已变更", str(self.response.json()["message"]))
        self.test_result = "PASS"

    def test_build_case081(self):
        """乘机人英文名--空"""
        self.logger.info('国际机票编单--用例081--乘机人英文姓名--空')
        self.data["passengers"][0]["givenNameEn"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定乘机人英文名", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_build_case082(self):
        """乘机人英文名--数据无效"""
        self.logger.info('国际机票编单--用例082--乘机人英文姓名--数据无效')
        self.data["passengers"][0]["givenNameEn"] = "中文"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("员工姓名不满足格式要求", str(self.response.json()["message"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例083--乘客类型--Adult")
    def test_build_case083(self):
        """乘客类型--Adult"""
        self.logger.info('国际机票编单--用例083--乘客类型--Adult')
        self.data["passengers"][0]["passengerType"] = "Adult"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例084--乘客类型--Child")
    def test_build_case084(self):
        """乘客类型--Child"""
        self.logger.info('国际机票编单--用例084--乘客类型--Child')
        self.data["passengers"][0]["passengerType"] = "Child"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue("当前系统仅支持成人", str(self.response.json()["message"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例085--乘客类型--Infant")
    def test_build_case085(self):
        """乘客类型--Infant"""
        self.logger.info('国际机票编单--用例085--乘客类型--Infant')
        self.data["passengers"][0]["passengerType"] = "Infant"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue("当前系统仅支持成人", str(self.response.json()["message"]))
        self.test_result = "PASS"

    def test_build_case086(self):
        """乘机人英文姓--空"""
        self.logger.info('国际机票编单--用例086--乘机人英文姓--空')
        self.data["passengers"][0]["surnameEn"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定乘机人英文姓", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_build_case087(self):
        """乘机人英文姓--数据无效"""
        self.logger.info('国际机票编单--用例087--乘机人英文姓--数据无效')
        self.data["passengers"][0]["surnameEn"] = "谭"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("员工姓名不满足格式要求", str(self.response.json()["message"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例088--是否公司员工--true")
    def test_build_case088(self):
        """是否公司员工--true"""
        self.logger.info('国际机票编单--用例088--是否公司员工--true')
        self.data["passengers"][0]["wasEmployee"] = "true"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例089--是否公司员工--false")
    def test_build_case089(self):
        """是否公司员工--false"""
        self.logger.info('国际机票编单--用例089--是否公司员工--false')
        self.data["passengers"][0]["wasEmployee"] = "false"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    def test_build_case090(self):
        """是否公司员工--空"""
        self.logger.info('国际机票编单--用例090--是否公司员工--空')
        self.data["passengers"][0]["wasEmployee"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定乘机人是否为公司员工", str(self.response.json()["errors"]))
        self.test_result = "PASS"

    def test_build_case091(self):
        """是否公司员工--数据无效"""
        self.logger.info('国际机票编单--用例091--是否公司员工--数据无效')
        self.data["passengers"][0]["wasEmployee"] = "123"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.assertIn('only "true" or "false"', str(self.response.json()))
        self.test_result = "PASS"

    def test_build_case092(self):
        """改签政策--空"""
        self.logger.info('国际机票编单--用例092--改签政策--空')
        self.data["policy"]["changePolicyDesc"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定改签政策描述", str(self.response.json()["message"]))
        self.test_result = "PASS"

    def test_build_case093(self):
        """退票政策--空"""
        self.logger.info('国际机票编单--用例093--退票政策--空')
        self.data["policy"]["returnPolicyDesc"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定退票政策描述", str(self.response.json()["message"]))
        self.test_result = "PASS"

    def test_build_case094(self):
        """加价让利--空"""
        self.logger.info('国际机票编单--用例094--加价让利--空')
        self.data["priceInfo"]["addPrice"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定加价让利", str(self.response.json()["message"]))
        self.test_result = "PASS"

    def test_build_case095(self):
        """加价让利--数据无效"""
        self.logger.info('国际机票编单--用例095--加价让利--数据无效')
        self.data["priceInfo"]["addPrice"] = "AAA"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.assertIn("not a valid representation", str(self.response.json()))
        self.test_result = "PASS"

    def test_build_case096(self):
        """客户留款--空"""
        self.logger.info('国际机票编单--用例096--客户留款--空')
        self.data["priceInfo"]["customerReservedAmount"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定客户留款", str(self.response.json()["message"]))
        self.test_result = "PASS"

    def test_build_case097(self):
        """客户留款--数据无效"""
        self.logger.info('国际机票编单--用例097--客户留款--数据无效')
        self.data["priceInfo"]["customerReservedAmount"] = "AAA"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.assertIn("not a valid representation", str(self.response.json()))
        self.test_result = "PASS"

    def test_build_case098(self):
        """价格来源--空"""
        self.logger.info('国际机票编单--用例098--价格来源--空')
        self.data["priceInfo"]["priceSource"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定价格来源", str(self.response.json()["message"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例099--价格来源--数据无效--未校验")
    def test_build_case099(self):
        """价格来源--数据无效"""
        self.logger.info('国际机票编单--用例099--价格来源--数据无效')
        self.data["priceInfo"]["priceSource"] = "！@￥"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    def test_build_case100(self):
        """系统使用费--空"""
        self.logger.info('国际机票编单--用例100--系统使用费--空')
        self.data["priceInfo"]["serviceFee"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定系统使用费", str(self.response.json()["message"]))
        self.test_result = "PASS"

    def test_build_case101(self):
        """客户留款--数据无效"""
        self.logger.info('国际机票编单--用例101--客户留款--数据无效')
        self.data["priceInfo"]["serviceFee"] = "AAA"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.assertIn("not a valid representation", str(self.response.json()))
        self.test_result = "PASS"

    def test_build_case102(self):
        """税费--空"""
        self.logger.info('国际机票编单--用例102--税费--空')
        self.data["priceInfo"]["tax"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定税费", str(self.response.json()["message"]))
        self.test_result = "PASS"

    def test_build_case103(self):
        """客户留款--数据无效"""
        self.logger.info('国际机票编单--用例103--客户留款--数据无效')
        self.data["priceInfo"]["serviceFee"] = "AAA"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.assertIn("not a valid representation", str(self.response.json()))
        self.test_result = "PASS"

    def test_build_case104(self):
        """票面价--空"""
        self.logger.info('国际机票编单--用例104--票面价--空')
        self.data["priceInfo"]["ticketFee"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 98, "返回的code不是98，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertIn("未指定票面价", str(self.response.json()["message"]))
        self.test_result = "PASS"

    def test_build_case105(self):
        """票面价--数据无效"""
        self.logger.info('国际机票编单--用例105--票面价--数据无效')
        self.data["priceInfo"]["ticketFee"] = "AAA"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.assertIn("not a valid representation", str(self.response.json()))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例106--是否发起预记账--true")
    def test_build_case106(self):
        """是否发起预记账--true"""
        self.logger.info('国际机票编单--用例106--是否发起预记账--true')
        self.data["priceInfo"]["wasPrebilling"] = "true"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例107--是否发起预记账--false")
    def test_build_case107(self):
        """是否发起预记账--false"""
        self.logger.info('国际机票编单--用例107--是否发起预记账--false')
        self.data["priceInfo"]["wasPrebilling"] = "false"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例108--是否发起预记账--空--未校验")
    def test_build_case108(self):
        """是否发起预记账--空"""
        self.logger.info('国际机票编单--用例108--是否发起预记账--空')
        self.data["priceInfo"]["wasPrebilling"] = ""
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"

    @unittest.skipIf(status=='200', "产生数据：用例109--是否发起预记账--数据无效--未校验")
    def test_build_case109(self):
        """是否发起预记账--数据无效"""
        self.logger.info('国际机票编单--用例109--是否发起预记账--数据无效')
        self.data["priceInfo"]["wasPrebilling"] = "·13"
        self.response = self.api.urlHeaderData(self.url, self.headers, self.data)
        self.get_error(self.response)
        self.assertEqual(self.response_code, 0, "返回的code不是0，是{0}，错误内容：{1}".format(self.response_code, self.message))
        self.assertTrue(re.findall(r"\d{18}", self.response.json()["data"]))
        self.test_result = "PASS"


if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(testsuite)

