import json
import os
from Utils import JsonUtil

import requests
import urllib3
from Config import ReadConfig
from Common import Log

'''封装HTTP请求实体类'''
'''当前服务器设定仅支持Tehang_5G内网访问'''
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SendHttp:
    def  __init__(self, url):
        global httpscheme, baseurl, port, timeout
        loadRC = ReadConfig.readconfig()
        httpscheme = loadRC.get_URL('httpscheme')  # 获取请求协议
        baseurl = loadRC.get_URL(url)  # 获取域名
        # port =loadRC.get_URL('port')
        requests.adapters.DEFAULT_RETRIES = 5  # 最大重试次数
        s = requests.session()
        s.keep_alive = False
        self.timeout = loadRC.get_URL('timeout')
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = None
        # dirpath = os.path.split(__file__)[0]    #SSL证书配置
        # self.path = os.path.join(dirpath, 'https.pem')
        self.logger = Log.log('https').logger

    #  self.files = {}
    #   self.state = 0

    def set_url(self, urlpath):
        if 'http' in urlpath:
            self.url = urlpath
        else:
            self.url = (httpscheme + '://' + baseurl + urlpath).strip()
        self.logger.info('当前访问的地址为:' + self.url)

    def set_headers(self, header):
        # if not isinstance(header,dict):
        #     raise TypeError('header输入的类型不是dict类型')
        # else:
        self.headers = header

    def set_params(self, params):
        if not isinstance(params, dict):
            raise TypeError('params输入的类型不是dict类型')
        else:
            self.params = params

    def set_data(self, data):
        if not isinstance(data, dict):
            raise TypeError('data输入的类型不是dict类型')
        else:
            if self.headers['Content-Type'] == 'application/json':
                rrdata = json.dumps(data)
                self.data = rrdata
            else:
                self.data = data

    # '''get请求base配置,verify=False //关闭ssl校验'''
    def http_get(self):
        try:
            response = requests.get(
                self.url,
                params=self.params,
                headers=self.headers,
                timeout=float(
                    self.timeout),
                verify=False)
            print(self.url)
            self.logger.info('get请求返回数据:' + response.text)
            return response
        except TimeoutError:
            # 打印日志
            self.logger.error('GET请求失败_状态码（%d）' % response.status_code)
            return None

    # '''Post请求base配置'''
    def http_post(self):
        self.logger.info('post请求数据:{0}'.format(self.data))
        self.logger.info('post请求头:{0}'.format(self.headers))
        self.logger.info('post请求URL:{0}'.format(self.url))
        try:
            response = requests.post(
                self.url,
                data=self.data,
                headers=self.headers,
                timeout=float(
                    self.timeout),
                verify=False)
            self.logger.info('post请求返回数据:' + response.text)
            return response
        # except TimeoutError:
        except Exception as e:
            # 打印日志
            # self.logger.error('Post请求失败_状态码（%d）' % response.status_code)  #  timeout要做判断
            self.logger.error('Post请求失败，errormsg:{0}'.format(e))
            return None

    # 通过cookie请求
    def http_cookie_get(self):
        '''
        :param cookie:  登录态
        :return:
        '''
        session = requests.session()
        requests.utils.add_dict_to_cookiejar(session.cookies, self.cookie)
        response = session.get(
            self.url,
            params=self.params,
            headers=self.headers,
            timeout=float(
                self.timeout))
        return response

    def http_cookie_post(self):
        '''

        :param cookie: 登录态
        :return:
        '''
        session = requests.session()
        requests.utils.add_dict_to_cookiejar(session.cookies, self.cookie)
        response = session.post(
            self.url,
            data=self.data,
            headers=self.headers,
            timeout=float(
                self.timeout))
        return response

    def http_main(self, method, url, data=None, headers=None):
        if method == 'post':
            self.set_url(url)
            self.set_headers(headers)
            self.set_data(data)
            res = self.http_post()
        else:
            self.set_url(url)
            self.set_headers(headers)
            self.set_params(data)
            res = self.http_get()
        return res


if __name__ == '__main__':
    SendHttp().http_main("post", "url")
