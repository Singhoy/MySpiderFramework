"""爬虫组件封装"""
from requests import Request

from item import Item

"""
1. 准备起始URL
2. 构建起始请求
3. 对响应数据进行解析
"""


class Spider(object):
    # 1.准备起始URL
    start_url = 'http://www.baidu.com'

    def start_request(self):
        # 2.构建起始请求
        # 返回请求数据
        return Request(self.start_url)

    @staticmethod
    def parse(response):
        # 3.对响应数据进行解析，返回数据或新请求
        return Item(response.body)
