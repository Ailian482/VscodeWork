import re
import random
from datetime import date, timedelta
from Common.Base import Base
from Common import Log
from Utils import JsonUtil, JsonPathUtil
from ApiData.UrlHeader import UrlHeader
from ApiData.UrlHeaderData import UrlHeaderData
from Config.ReadConfig import readconfig
from time import sleep
import time, ast


class FlightProcess:
    def __init__(self):
        self.logger = Log.log("test_login").logger
        self.jutil = JsonPathUtil.jsonpath_util()
        login_response = Base().Customer_login()
        token = self.jutil.get_values(login_response, "token")[0]
        self.header = {"Content-Type": "application/json", "Authorization": "Bearer {0}".format(token)}

    def get_staff_header(self):
        login_response = Base().Staff_login()
        token = self.jutil.get_values(login_response, "token")[0]
        header = {"Content-Type": "application/json", "Authorization": "Bearer {0}".format(token)}
        return header

    def search_flight(self):
        search_data = JsonUtil.OperetionJson("flight.json").get_data("searchFlight")
        flight_data = (date.today() + timedelta(days=+random.randint(10, 100))).strftime("%Y-%m-%d")
        search_data["flightDate"] = flight_data
        response = UrlHeaderData().urlHeaderData(readconfig().get_flight_url("search"), self.header, search_data)
        if response.json()["code"] != 0:
            return "", "", ""
        flights_id = self.jutil.get_values(response.json(), "id")[0]
        flight_id = self.jutil.get_values(response.json(), "flights")[0][0]["id"]
        bunk_id = self.jutil.get_values(response.json(), "bunks")[0][0]["id"]
        return flights_id, flight_id, bunk_id

    def get_place_data(self):
        flights_id, flight_id, bunk_id = self.search_flight()
        place_data = JsonUtil.OperetionJson("flight.json").get_data("placeFlight")
        place_data["routes"][0]["segments"][0]["bunkId"] = bunk_id
        place_data["routes"][0]["segments"][0]["flightId"] = flight_id
        place_data["routes"][0]["segments"][0]["flightsId"] = flights_id

        return place_data

    def place_flight(self):
        place_data = self.get_place_data()
        response = UrlHeaderData().urlHeaderData(readconfig().get_flight_url("place"), self.header, place_data)
        return response.json()

    def get_order_id(self):
        place_result = self.place_flight()
        assert place_result["code"] == 0, "下单失败！失败原因：{0}".format(place_result["message"])
        if re.findall(r"\d{17}", str(place_result)):
            return JsonPathUtil.jsonpath_util().get_values(place_result, "data")[0]
        else:
            return ""

    def cancel_flight(self):
        order_id = self.get_order_id()
        if not order_id:
            return {}
        url = "{0}{1}".format(readconfig().get_flight_url("cancel"), order_id)
        response = UrlHeader().urlHeader(url, self.header)
        return response.json()

    def pay_flight(self):
        order_id = self.get_order_id()
        if not order_id:
            return {}, order_id, self.header
        # 调用支付前验价
        prepay_url = "{0}{1}".format(readconfig().get_flight_url("prepayValidate"), order_id)
        UrlHeader().urlHeader(prepay_url, self.header)
        query_prepay_url = "{0}{1}".format(readconfig().get_flight_url("queryPrepayValidate"), order_id)
        t1 = time.time()
        check = False
        while 1:
            if time.time() - t1 > 60:
                break
            response = UrlHeader().urlHeader(query_prepay_url, self.header)
            if response.json()["data"].__contains__("status"):
                if response.json()["data"]["status"] == 0:
                    check = True
                    break
        if not check:
            order_id = ""
        url = "{0}{1}".format(readconfig().get_flight_url("pay"), order_id)
        response = UrlHeader().urlHeader(url, self.header)
        return response.json(), order_id, self.header

    def get_ticket_id(self):
        order_id = self.pay_flight()[1]
        ticket_id = ""
        if not order_id:
            return "", "", self.header
        url = r"{0}{1}".format(readconfig().get_flight_url("detail"), order_id)
        t1 = time.time()
        while 1:
            if time.time() - t1 > 60:
                break
            response = UrlHeader().urlHeader(url, self.header)
            operation = JsonPathUtil.jsonpath_util().get_values(response.json(), "flightOrderOperation")[0]
            result = operation["canBeChanged"]
            if result:
                ticket_id_list = JsonPathUtil.jsonpath_util().get_values(response.json(), "ticketId")
                ticket_id = ",".join(ticket_id_list)
                break
            sleep(5)
        return order_id, ticket_id, self.header

    # 获取出票请求数据
    def get_confirm_data(self):
        confirm_data = JsonUtil.OperetionJson("flight.json").get_data("ticketConfirm")
        task_id, order_id, ticket_ids, header = self.get_id()
        confirm_data["taskId"] = task_id
        self.get_tickets_inf(confirm_data, ticket_ids)
        return confirm_data

    # 获取出票接口tickets信息
    def get_tickets_inf(self, confirm_data, ticket_ids):
        dict_data = confirm_data["tickets"][0]
        dict_data["ticketId"] = ticket_ids[0]
        confirm_data["tickets"][0] = str(dict_data)
        if len(ticket_ids) > 1:
            for i in range(1, len(ticket_ids)):
                dict_data["ticketId"] = ticket_ids[i]
                confirm_data["tickets"].append(str(dict_data))
        # 将字符串转换为字典（直接添加字典，键值对会同时更新为相同的值，暂不明确原因）
        for i in range(len(confirm_data["tickets"])):
            confirm_data["tickets"][i] = ast.literal_eval(confirm_data["tickets"][i])
        return confirm_data

    # 调用任务列表，获取taskID和orderID和ticket_ids
    def get_id(self, tasktype="TicketConfirm"):
        query_tasks = readconfig().get_flight_url("queryFlightTask")
        data = JsonUtil.OperetionJson("flight.json").get_data("queryFlightTask")
        data["taskTypes"] = tasktype
        header = self.get_staff_header()
        response = UrlHeaderData("Staff_url").urlHeaderData(query_tasks, header, data)
        number = random.randint(0, 9)
        task_id = self.jutil.get_values(response, "id")[number]
        order_id = self.jutil.get_values(response, "orderId")[number]
        ticket_ids = self.jutil.get_values(response, "ticketIds")[number].split(",")
        return task_id, order_id, ticket_ids, header

     # 获取退票任务的乘客类型
    def get_passenger_type(self, task_id):
        get_return_detail = readconfig().get_flight_url("getTicketReturnTaskDetail")
        url = "{0}{1}".format(get_return_detail, task_id)
        response = UrlHeader("Staff_url").urlHeader(url, self.get_staff_header())
        passenger_types = list(set(self.jutil.get_values(response, "passengerType")))
        return passenger_types

    # 构造退票请求data
    def get_return_data(self):
        return_data = JsonUtil.OperetionJson("flight.json").get_data("returnSuccess")
        task_id, order_id, ticket_ids, header = self.get_id("ReturnConfirm")
        return_data["taskId"] = int(task_id)
        passenger_type = self.get_passenger_type(task_id )
        return_data["passengerItems"][0]["passengerType"] = passenger_type[0]
        set_data = return_data["passengerItems"][0]
        return_data["passengerItems"][0] = str(set_data)
        if len(passenger_type) > 1:
            for i in range(1, len(passenger_type)):
                set_data["passengerType"] = passenger_type[i]
                return_data["passengerItems"].append(str(set_data))
        for i in range(len(return_data["passengerItems"])):
            return_data["passengerItems"][i] = ast.literal_eval(return_data["passengerItems"][i])
        return return_data

if __name__ == '__main__':
    print(FlightProcess().get_return_data())
