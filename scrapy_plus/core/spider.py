"""爬虫组件封装"""
from scrapy_plus.conf.default_sttings import HEADERS

from scrapy_plus.item import Item
from scrapy_plus.win_http.request import Request

"""
1. 准备起始URL
2. 构建起始请求
3. 对响应数据进行解析
"""


class Spider(object):
    # 爬虫名
    name = 'spider'

    # 1.准备起始URL列表
    start_urls = []

    def start_request(self):
        # 2.构建起始请求
        # 遍历起始URL列表，创建请求对象，交给引擎
        for url in self.start_urls:
            # 返回请求数据
            yield Request(url, headers=HEADERS)

    def parse(self, response):
        # 3.对响应数据进行解析，返回数据或新请求
        item = Item(response.body)

        return item
