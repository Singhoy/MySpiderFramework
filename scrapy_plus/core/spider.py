"""爬虫组件封装"""
from _http.request import Request
from item import Item

"""
1. 准备起始URL
2. 构建起始请求
3. 对响应数据进行解析
"""


class Spider(object):
    # 1.准备起始URL
    start_urls = []

    def start_request(self):
        # 2.构建起始请求
        # 遍历起始URL列表，创建请求对象，交给引擎
        for url in self.start_urls:
            # 返回请求数据
            yield Request(url)

    @staticmethod
    def parse(response):
        # 3.对响应数据进行解析，返回数据或新请求
        item = Item(response.url)

        return item
