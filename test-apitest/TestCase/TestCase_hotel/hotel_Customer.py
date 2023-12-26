import random
from datetime import date, timedelta
from Common.Base import Base
from Common import Log
from Utils import JsonUtil, JsonPathUtil
from ApiData.UrlHeaderData import UrlHeaderData
from ApiData.UrlHeader import UrlHeader


class HotelProcess:
    def __init__(self):
        self.logger = Log.log("test_login").logger
        self.jutil = JsonPathUtil.jsonpath_util()
        login_response = Base().Customer_login()
        token = self.jutil.get_values(login_response, "token")[0]
        self.header = {"Content-Type": "application/json", "Authorization": "Bearer {0}".format(token)}
        self.Send_UHD = UrlHeaderData("Customer_url")
        self.Send_UH = UrlHeader("Customer_url")

    def search_Hotel(self):  # 酒店查询
        search_data = JsonUtil.OperetionJson("Hotel_Customer_Json.json").get_data("Hotel_search")
        search_data["checkInDate"] = (date.today()).strftime("%Y-%m-%d")
        search_data["checkOutDate"] = (date.today() + timedelta(days=+3)).strftime("%Y-%m-%d")
        response = self.Send_UHD.urlHeaderData("/front/v1/hotel/search", self.header, search_data)
        response_data = response.json()
        if response_data["code"] != 0:
            return ""
        return response_data

    def getHotelDetail(self):  # 酒店详情，依赖于查询citycode
        getHotelDetail_data = JsonUtil.OperetionJson("Hotel_Customer_Json.json").get_data("getHotelDetail")
        getHotelDetail_data["hotelCode"] = \
            self.jutil.get_values(self.search_Hotel(), "hotels")[0][random.randint(1, 9)]["hotelCode"]
        getHotelDetail_data["checkInDate"] = (date.today()).strftime("%Y-%m-%d")
        getHotelDetail_data["checkOutDate"] = (date.today() + timedelta(days=+3)).strftime("%Y-%m-%d")
        response = self.Send_UHD.urlHeaderData("/front/v1/hotel/getHotelDetail", self.header, getHotelDetail_data)
        response_data = response.json()
        if response_data["code"] != 0:
            return ""
        return response_data

    def placeOrder(self):  # 下单接口，依赖于getHotelDetail.
        dependData = self.getHotelDetail()
        placeOrder_data = JsonUtil.OperetionJson("Hotel_Customer_Json.json").get_data("placeOrder_OnBusiness")
        self.jutil.set_values(placeOrder_data, "hotelCode", self.jutil.get_values(dependData, "data")[0]["hotelCode"])
        self.jutil.set_values(placeOrder_data, "cityCode", self.jutil.get_values(dependData, "data")[0]["cityCode"])
        self.jutil.set_values(placeOrder_data, "roomCode", self.jutil.get_values(dependData, "rooms")[0][0]["roomCode"])
        self.jutil.set_values(placeOrder_data, "planCode", self.jutil.get_values(dependData, "rooms")[0][0]["planCode"])
        self.jutil.set_values(placeOrder_data, "checkInDate", (date.today()).strftime("%Y-%m-%d"))
        self.jutil.set_values(placeOrder_data, "checkOutDate", (date.today() + timedelta(days=+3)).strftime("%Y-%m-%d"))
        response = self.Send_UHD.urlHeaderData("/front/v1/hotel/placeOrder", self.header, placeOrder_data)
        response_data = response.json()
        if response_data["code"] != 0:
            return "", ""
        return response_data, self.header

    def getOrderDetail(self, OrderId):  # 获取订单详情
        url = "/front/v1/hotel/getOrderDetail" + "?" + "orderId=" + OrderId
        response = self.Send_UH.urlHeader(url, self.header)
        response_data = response.json()
        if response_data['code'] != 0:
            return ""
        else:
            return response_data, self.header

    def preBill(self):
        DependData = self.placeOrder()
        url = "/front/v1/hotel/preBill" + "?" + "orderId=" + DependData[0]['data']
        response = self.Send_UH.urlHeader(url, self.header)
        response_data = response.json()
        if response_data['code'] != 0:
            return "", ""
        else:
            return DependData[0], self.header


if __name__ == '__main__':
    print(HotelProcess().getHotelDetail())
