"""项目中的配置信息"""
DEFAULT_LOG_FILENAME = '日志.log'

# 配置爬虫
SPIDERS = [
    'spiders.baidu.BaiduSpider',
    # 'spiders.douban.DoubanSpider',
]

# 配置管道
PIPELINES = [
    'pipelines.BaiduPipeline',
    # 'pipelines.DoubanPipeline',
]

# 配置下载器中间件
DOWNLOADER_MIDDLEWARES = [
    'middlewares.downloader_middlewares.DownloaderMiddleware1',
    'middlewares.downloader_middlewares.DownloaderMiddleware2',
]

# 配置爬虫中间件
SPIDER_MIDDLEWARES = [
    'middlewares.spider_middlewares.SpiderMiddleware1',
    'middlewares.spider_middlewares.SpiderMiddleware2',
]
