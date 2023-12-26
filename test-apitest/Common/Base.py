from Utils import JsonUtil
from Common import BaseHttp, Log

'''基本请求，登录登出'''


class Base:
    def __init__(self, url="Customer_url"):
        self.logger = Log.log("Base_login").logger
        self.URL = url

    def ReturnBaseUrl(self):  # 读取器，读取通用变量
        return self.URL

    def Customer_login(self, json_file='login_user.json', url='/front/v1/employee/login'):
        data = JsonUtil.OperetionJson(json_file).get_data("Customer_login")
        self.basehttp = BaseHttp.SendHttp(self.URL)
        self.basehttp.set_url(url)
        self.basehttp.set_headers({'Content-Type': 'application/json', 'Connection': 'Keep-Alive'})
        self.basehttp.set_data(data)
        response = self.basehttp.http_post()
        return response.json()

    def Staff_login(self, json_file='login_user.json', url='/v1/staff/login'):
        self.URL = "Staff_url"
        data = JsonUtil.OperetionJson(json_file).get_data("Staff_login")
        self.basehttp = BaseHttp.SendHttp(self.URL)
        self.basehttp.set_url(url)
        self.basehttp.set_headers({'Content-Type': 'application/json', 'Connection': 'Keep-Alive'})
        self.basehttp.set_data(data)
        response = self.basehttp.http_post()
        return response.json()


if __name__ == '__main__':
    print(Base().Customer_login())
    print(Base().Staff_login())
