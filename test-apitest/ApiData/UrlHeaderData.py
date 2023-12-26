from Common.Base import Base
from Common import BaseHttp, Log


class UrlHeaderData:

    def __init__(self,url="Customer_url"):
        self.logger = Log.log("Base_login").logger
        base_url = Base(url).ReturnBaseUrl()   # 获取接口域名前缀
        self.basehttp = BaseHttp.SendHttp(base_url)

    def urlHeaderData(self, url, headers, data):
        self.basehttp.set_url(url)
        self.basehttp.set_headers(headers)
        self.basehttp.set_data(data)
        response = self.basehttp.http_post()
        return response


if __name__ == '__main__':
    pass
