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

# 配置异步类型：thread线程，coroutine协程
ASYNC_TYPE = 'thread'

# 配置是否启用分布式，默认启用
SCHEDULER_PERSIST = True

# 配置redis
# 用于指定基于Redis的队列, 在Redis数据中的key
REDIS_QUEUE_NAME = 'scrapy_plus_request_queue_key'
# 用于指定基于Redis的set集合key: 用于存储指纹数据
REDIS_SET_NAME = 'scrapy_plus_fp_set_key'

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0

# 配置断点续爬，默认开启
FP_PERSIST = True

# 默认请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
