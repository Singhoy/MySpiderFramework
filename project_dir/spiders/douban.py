"""
豆瓣Top250爬虫

实现思路:
1. 由于页数固定, 并且URL规律很明显; 我们可以通过重写start_requests生成多个起始请求
2. 对数据进行解析
"""
from scrapy_plus.item import Item
from scrapy_plus.win_http.request import Request
from scrapy_plus.core.spider import Spider


class DoubanSpider(Spider):
    name = 'douban'

    def start_request(self):
        """重写start_request方法，返回多个请求"""
        # URL模板
        start_url_pattern = 'https://movie.douban.com/top250?start={}&filter='
        for num in range(0, 250, 25):
            start_url = start_url_pattern.format(num)
            yield Request(start_url)

    def parse(self, response):
        """对响应进行处理"""
        # 获取包含电影信息的li标签列表
        lis = response.xpath('//*[@id="content"]/div/div[1]/ol/li')
        # 遍历lis获取每个电影名
        for li in lis:
            dic = {'name': li.xpath('./div/div[2]/div[1]/a/span[1]/text()')[0]}
            # print(dic)
            item = Item(dic)
            # 请求详情页，构造详情页的请求
            # 1.准备详情的URL
            detail_url = li.xpath('./div/div[2]/div[1]/a/@href')[0]
            yield Request(detail_url, callback=self.parse_detail, meta={'item': item})

    @staticmethod
    def parse_detail(response):
        """解析详情页"""
        # 取出上一个解析函数传递过来的数据
        item = response.meta['item']
        # print(item.data)
        return item
