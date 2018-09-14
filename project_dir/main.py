from middlewares.downloader_middlewares import DownloaderMiddleware1, DownloaderMiddleware2
from middlewares.spider_middlewares import SpiderMiddleware1, SpiderMiddleware2
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

    # 下载器中间件列表
    downloader_middlewares = [
        DownloaderMiddleware1(),
        DownloaderMiddleware2()
    ]

    # 爬虫中间件列表
    spider_middlewares = [
        SpiderMiddleware1(),
        SpiderMiddleware2()
    ]

    engine = Engine(spiders, pipelines, downloader_middlewares, spider_middlewares)
    engine.start()
