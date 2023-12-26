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
        self.Send = UrlHeaderData('Staff_url')

    def updateCorpSettlementInfo_CorpPayMode(self, payMode,
                                             url='/admin/v1/corp/updateCorpSettlementInfo'):  # 修改企业结算信息——修改支付方式
        interface_data = JsonUtil.OperetionJson("Common_Staff_Json.json").get_data("updateCorpSettlementInfo")
        self.jutil.set_values(interface_data, "corpPayMode", payMode)
        response = self.Send.urlHeaderData(url, self.header, interface_data)
        response_data = response.json()
        return response_data["code"] == 0


if __name__ == '__main__':
    print(Common_interface().updateCorpSettlementInfo_CorpPayMode("CorpCredit"))
