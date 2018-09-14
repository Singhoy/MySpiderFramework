from spiders.baidu import BaiduSpider
from scrapy_plus.core.engine import Engine
from spiders.douban import DoubanSpider

if __name__ == '__main__':
    # spider = BaiduSpider()
    spider = DoubanSpider()
    engine = Engine(spider)
    engine.start()
