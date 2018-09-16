"""Request对象"""


class Request(object):
    """框架内置请求对象，设置请求信息"""

    def __init__(self, url, method='GET', headers=None, params=None, data=None, callback=None, meta=None,
                 dont_filter=False):
        """
        :param url: 请求的URL
        :param method: 请求的方法
        :param headers: 请求头
        :param params: GET的请求参数
        :param data: POST的请求参数
        :param callback: 用于指定该请求对应响应的解析函数
        :param meta: 用于不同解析函数间数据传递
        :param dont_filter: 判断是否去重，False表示要去重，True表示不过滤
        """
        if meta is None:
            meta = {}
        if data is None:
            data = {}
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data
        self.callback = callback
        self.meta = meta
        self.dont_filter = dont_filter
