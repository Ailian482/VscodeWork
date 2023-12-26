import random
from datetime import date, timedelta
from Common.Base import Base
from Common import Log
from Utils import JsonUtil, JsonPathUtil
from ApiData.UrlHeaderData import UrlHeaderData
from ApiData.UrlHeader import UrlHeader


class Common_interface:
    def __init__(self):
        self.logger = Log.log("test_login").logger
        self.jutil = JsonPathUtil.jsonpath_util()
        login_response = Base().Staff_login()
        token = self.jutil.get_values(login_response, "token")[0]
        self.header = {"Content-Type": "application/json", "Authorization": "Bearer {0}".format(token)}

    def getMonitorRecords(self, url="/admin/v1/hotelMonitor/getMonitorRecords"):  # 获取国内酒店“自动订房/退房”监控记录
        interface_data = JsonUtil.OperetionJson("Common_Staff_Json.json").get_data("getMonitorRecords")
        response = UrlHeaderData().urlHeaderData(url, self.header, interface_data)
        response_data = response.json()
        return response_data


if __name__ == '__main__':
    print(Common_interface().getMonitorRecords())
