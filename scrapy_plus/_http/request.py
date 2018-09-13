"""Request对象"""


class Request(object):
    """框架内置请求对象，设置请求信息"""

    def __init__(self, url, method='GET', headers=None, params=None, data=None):
        """
        :param url: 请求的URL
        :param method: 请求的方法
        :param headers: 请求头
        :param params: GET的请求参数
        :param data: POST的请求参数
        """
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data
