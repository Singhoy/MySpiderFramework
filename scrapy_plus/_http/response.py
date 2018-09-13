"""Response对象"""


class Response(object):
    """框架内置Response对象"""

    def __init__(self, url, status_code, headers, body):
        """
        :param url: 响应的URL
        :param status_code: 状态码
        :param headers: 响应头
        :param body: 响应的数据（二进制的）
        """
        self.url = url
        self.status_code = status_code
        self.headers = headers
        self.body = body
