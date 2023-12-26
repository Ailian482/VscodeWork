from Common.Base import Base
from Common import BaseHttp, Log


class UrlHeader:

    def __init__(self,url="Customer_url"):
        self.logger = Log.log("Base_login").logger
        base_url = Base(url).ReturnBaseUrl()   # 获取接口域名前缀
        self.basehttp = BaseHttp.SendHttp(base_url)

    def urlHeader(self, url, headers):
        self.basehttp.set_url(url)
        self.basehttp.set_headers(headers)
        response = self.basehttp.http_post()
        return response


if __name__ == '__main__':
    pass
