import random, ast
import datetime
from datetime import timedelta
from Common import Log
from Common.Base import Base
from Utils import JsonUtil, JsonPathUtil
from ApiData.UrlHeaderData import UrlHeaderData
from ApiData.UrlHeader import UrlHeader
from Config.ReadConfig import readconfig

class IntflightProcess:

    def __init__(self):
        self.logger = Log.log("test_login").logger
        self.jutil = JsonPathUtil.jsonpath_util()
        login_response = Base().Staff_login()
        token = self.jutil.get_values(login_response, "token")[0]
        self.header = {"Content-Type": "application/json", "Authorization": "Bearer {0}".format(token)}

    def get_build_data(self):
        build_data = JsonUtil.OperetionJson("intflight.json").get_data("build")
        build_data["bookingInfo"]["bookingTime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        build_data["priceInfo"]["addPrice"] = random.randint(0, 500)
        build_data["priceInfo"]["customerReservedAmount"] = random.randint(0, 400)
        build_data["priceInfo"]["serviceFee"] = random.randint(0, 100)
        build_data["priceInfo"]["tax"] = random.randint(200, 400)
        build_data["priceInfo"]["ticketFee"] = random.randint(500, 1000)
        dep_time = (datetime.datetime.now() + timedelta(days=+random.randint(0, 365), hours=random.randint(0, 24),
                                                        minutes=random.randint(0, 60))).strftime("%Y-%m-%d %H:%M")
        stu = datetime.datetime.strptime(dep_time, "%Y-%m-%d %H:%M")
        arr_time = (stu + timedelta(days=+random.randint(0, 1), hours=random.randint(0, 24),
                                    minutes=random.randint(0, 60))).strftime("%Y-%m-%d %H:%M")
        build_data["routes"][0]["segments"][0]["arrival"]["dateTime"] = arr_time
        build_data["routes"][0]["segments"][0]["departure"]["dateTime"] = dep_time
        return build_data

    def get_confirm_data(self):
        confirm_data = JsonUtil.OperetionJson("intflight.json").get_data("ticketConfirm")
        task_id, order_id, header = self.get_id()
        passenger_ids, segment_ids = self.get_order_detail(order_id)
        confirm_data["taskId"] = task_id
        confirm_data["priceItems"][0]["segmentIds"] = segment_ids
        self.get_price_inf(confirm_data, passenger_ids)
        return confirm_data

    # 获取出票接口priceItems信息
    def get_price_inf(self, confirm_data, passenger_ids):
        dict_data = confirm_data["priceItems"][0]
        dict_data["passengerId"] = passenger_ids[0]
        confirm_data["priceItems"][0] = str(dict_data)
        if len(passenger_ids) > 1:
            for i in range(1, len(passenger_ids)):
                dict_data["passengerId"] = passenger_ids[i]
                confirm_data["priceItems"].append(str(dict_data))
        # 将字符串转换为字典（直接添加字典，键值对会同时更新为相同的值，暂不明确原因）
        for i in range(len(confirm_data["priceItems"])):
            confirm_data["priceItems"][i] = ast.literal_eval(confirm_data["priceItems"][i])
        return confirm_data

    # 调用后台任务列表，获取taskID和orderID
    def get_id(self, tasktype="TicketConfirm"):
        query_tasks = readconfig().get_intflight_url("queryTasks")
        data = JsonUtil.OperetionJson("intflight.json").get_data("queryTasks")
        data["taskTypes"] = tasktype
        response = UrlHeaderData("Staff_url").urlHeaderData(query_tasks, self.header, data)
        number = random.randint(0, 19)
        task_id = self.jutil.get_values(response, "id")[number]
        order_id = self.jutil.get_values(response, "orderId")[number]
        return task_id, order_id, self.header

    # 获取订单详情
    def get_order_detail(self, order_id):
        url = "{0}{1}".format(readconfig().get_intflight_url("detail"), order_id)
        response = UrlHeader("Staff_url").urlHeader(url, self.header)
        passenger_id = self.jutil.get_values(response, "passengerId")
        segment_id = self.jutil.get_values(response, "segmentId")
        return passenger_id, segment_id

    # 调用前台任务列表，获取taskID和orderID和ticket_ids
    def get_task_detail(self, tasktype="CancelPnr"):
        query_tasks = readconfig().get_intflight_url("queryRequirementTasks")
        data = JsonUtil.OperetionJson("intflight.json").get_data("queryTasks")
        data["taskTypes"] = tasktype
        response = UrlHeaderData("Staff_url").urlHeaderData(query_tasks, self.header, data)
        number = random.randint(0, 9)
        task_id = self.jutil.get_values(response, "id")[number]
        order_id = self.jutil.get_values(response, "orderId")[number]
        return task_id, order_id, self.header

if __name__ == "__main__":
    print(IntflightProcess().get_id())


