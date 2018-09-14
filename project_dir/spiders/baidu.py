from scrapy_plus.core.spider import Spider


class BaiduSpider(Spider):
    name = 'baidu'

    start_urls = ['http://www.baidu.com', 'https://www.hao123.com', 'http://www.baidu.com', 'https://www.hao123.com']
