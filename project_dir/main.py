from spiders.baidu import BaiduSpider
from scrapy_plus.core.engine import Engine

if __name__ == '__main__':
    spider = BaiduSpider()
    engine = Engine(spider)
    engine.start()
