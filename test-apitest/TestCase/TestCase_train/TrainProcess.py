import re
import random
from Common.Base import Base
from Common import Log
from Utils import JsonUtil, JsonPathUtil
from ApiData.UrlHeader import UrlHeader
from datetime import date, timedelta
from ApiData.UrlHeaderData import UrlHeaderData
from Config.ReadConfig import readconfig
from time import sleep
import time


class TrainProcess:

    def __init__(self):
        self.logger = Log.log("test_login").logger
        self.jutil = JsonPathUtil.jsonpath_util()
        login_response = Base().Customer_login()
        token = self.jutil.get_values(login_response, "token")[0]
        self.header = {"Content-Type": "application/json", "Authorization": "Bearer {0}".format(token)}

    def search_train(self):
        search_data = JsonUtil.OperetionJson("train.json").get_data("searchTrain")
        train_date = (date.today() + timedelta(days=+random.randint(15, 30))).strftime("%Y-%m-%d")
        search_data["trainDate"] = train_date
        response = UrlHeaderData().urlHeaderData(readconfig().get_train_url("search"), self.header, search_data)
        if response.json()["code"] != 0:
            return "", "", ""
        query_id = self.jutil.get_values(response.json(), "queryId")[0]
        seat_type = self.jutil.get_values(response.json(), "seatType")[0]
        train_no = self.jutil.get_values(response.json(), "trainNo")[0]
        return query_id, seat_type, train_no

    def get_place_data(self):
        query_id, seat_type, train_no = self.search_train()
        place_data = JsonUtil.OperetionJson("train.json").get_data("placeTrain")
        self.jutil.set_values(place_data, "queryId", query_id)
        self.jutil.set_values(place_data, "seatType", seat_type)
        self.jutil.set_values(place_data, "trainNo", train_no)
        return place_data

    def place_train(self):
        place_data = self.get_place_data()
        response = UrlHeaderData().urlHeaderData(readconfig().get_train_url("place"), self.header, place_data)
        return response.json()

    def get_order_id(self):
        """用正则表达式匹配订单id"""
        place_result = self.place_train()
        assert place_result["code"] == 0, "下单失败！失败原因：{0}".format(place_result["message"])
        if re.findall(r"\d{18}", str(place_result)):
            return JsonPathUtil.jsonpath_util().get_values(place_result, "data")[0]
        else:
            return ""

    def get_booking_status(self, order_id):
        """查询订单订座状态"""
        status_url = r"{0}{1}".format(readconfig().get_train_url("bookingstatus"), order_id)
        t1 = time.time()
        while True:
            response = UrlHeader().urlHeader(status_url, self.header)
            status = JsonPathUtil.jsonpath_util().get_values(response.json(), "bookingStatus")[0]
            if time.time() - t1 > 60:
                return status
            if status == "Booking":
                sleep(5)
                continue
            else:
                return status

    def cancel_train(self):
        order_id = self.get_order_id()
        if not order_id:
            return {}
        booking_status = self.get_booking_status(order_id)
        if booking_status == "Success":
            url = r"{0}{1}".format(readconfig().get_train_url("cancel"), order_id)
            response = UrlHeader().urlHeader(url, self.header)
            return response
        else:
            return booking_status

    def pay_train(self):
        order_id = self.get_order_id()
        if not order_id:
            return "", "", self.header
        booking_status = self.get_booking_status(order_id)
        if booking_status == "Success":
            url = r"{0}{1}".format(readconfig().get_train_url("pay"), order_id)
            response = UrlHeader().urlHeader(url, self.header)
            return response, order_id, self.header
        else:
            return "", "", self.header

    def get_passenger_id(self):
        order_id = self.pay_train()[1]
        if not order_id:
            return "", "", self.header
        url = r"{0}{1}".format(readconfig().get_train_url("detail"), order_id)
        response = UrlHeader().urlHeader(url, self.header)
        id_list = JsonPathUtil.jsonpath_util().get_values(response.json(), "id")
        passenger_id = id_list[1:-1]
        return order_id, passenger_id, self.header


if __name__ == '__main__':
    TrainProcess().get_passenger_id()


