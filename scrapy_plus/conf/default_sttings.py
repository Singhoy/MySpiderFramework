import logging

# 默认的配置
DEFAULT_LOG_LEVEL = logging.INFO  # 默认等级
DEFAULT_LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'  # 默认日志格式
DEFAULT_LOG_DATE_FMT = '%Y-%m-%d %H:%M:%S'  # 默认时间格式
DEFAULT_LOG_FILENAME = 'log.log'  # 默认日志文件名称

# 配置爬虫
SPIDERS = []

# 配置管道
PIPELINES = []

# 配置下载器中间件
DOWNLOADER_MIDDLEWARES = []

# 配置爬虫中间件
SPIDER_MIDDLEWARES = []

# 配置异步任务数量
ASYNC_COUNT = 5
