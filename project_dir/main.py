from pipelines import BaiduPipeline, DoubanPipeline
from spiders.baidu import BaiduSpider
from scrapy_plus.core.engine import Engine
from spiders.douban import DoubanSpider

if __name__ == '__main__':
    baidu_spider = BaiduSpider()
    douban_spider = DoubanSpider()
    spiders = {
        BaiduSpider.name: baidu_spider,
        DoubanSpider.name: douban_spider
    }
    # 定义一个管道列表
    pipelines = [BaiduPipeline(), DoubanPipeline()]
    engine = Engine(spiders, pipelines)
    engine.start()
