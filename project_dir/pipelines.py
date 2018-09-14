from spiders.baidu import BaiduSpider
from spiders.douban import DoubanSpider


class BaiduPipeline(object):

    def process_item(self, item, spider):
        """
        管道处理数据的函数
        :param item: 引擎传递过来的数据
        :param spider: 该数据对应的爬虫对象
        :return: item，给后面的管道使用
        """
        # 通过爬虫名称执行爬虫
        # if spider.name == BaiduSpider.name:

        # 通过爬虫类型判断
        if isinstance(spider, BaiduSpider):
            print('百度管道处理的数据：%s' % item.data)

        return item


class DoubanPipeline(object):

    def process_item(self, item, spider):
        """
        管道处理数据的函数
        :param item: 引擎传递过来的数据
        :param spider: 该数据对应的爬虫对象
        :return: item，给后面的管道使用
        """
        # 通过爬虫类型判断
        if isinstance(spider, DoubanSpider):
            print('豆瓣管道处理的数据：%s' % item.data)

        return item
