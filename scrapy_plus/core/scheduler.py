"""调度器模块封装"""
from hashlib import sha1

import six
from w3lib.url import canonicalize_url

from scrapy_plus.utils.log import logger
from scrapy_plus.conf import settings

if not settings.SCHEDULER_PERSIST:
    # 不启用分布式，导入内存版指纹容器
    from six.moves.queue import Queue
    from scrapy_plus.utils.set import NormalFilterContainer as FilterContainer
else:
    # 启用分布式，导入redis版指纹容器
    from scrapy_plus.utils.queue import Queue
    from scrapy_plus.utils.set import RedisFilterContainer as FilterContainer


class Scheduler(object):
    """调度器
    1. 缓存请求
    2. 请求去重
    """

    def __init__(self, stats_collector):
        # 接收传递过来的统计器对象
        self.stats_collector = stats_collector
        # 创建队列对象，用于缓存请求
        self.queue = Queue()
        # 创建指纹容器,用于存储指纹数据
        self.__filter_container = FilterContainer()

    def add_request(self, request):
        """添加请求到请求对列中"""
        # 如果需要过滤，并且是重复请求才过滤
        if not request.dont_filter and self.__filter_request(request):
            # 如果请求需要过滤,记录日志,直接返回
            logger.info('过滤掉了重复的请求:%s' % request.url)
            self.stats_collector.incr(self.stats_collector.repeat_request_nums_key)
            return

        self.queue.put(request)
        # 每添加一次请求，就让总请求数量加1
        self.stats_collector.incr(self.stats_collector.request_nums_key)

    def get_request(self):
        # 从队列中获取请求，并返回请求
        return self.queue.get()

    def __filter_request(self, request):
        """
        请求去重
        :return: 如果是True,说明这个请求重复了,需要过滤,否则不用过滤
        """
        # 1.获取请求对应指纹
        fp = self.__get_fp(request)
        # 如果指纹在容器里,说明这个请求已经重复了
        if self.__filter_container.exists(fp):
            return True

        # 能来到这里,说明这个请求是全新的,把指纹添加到指纹容器中
        self.__filter_container.add_fp(fp)
        return False

    def __get_fp(self, request):
        """
        生成请求对应指纹
        :param request: 请求对象
        :return: 指纹
        """
        # 创建sha1算法对象
        s = sha1()
        # 添加请求方法名到sha1算法中
        s.update(self.__to_bytes(request.method.upper()))
        # 添加请求URL名,到sha1算法中
        s.update(self.__to_bytes(canonicalize_url(request.url)))
        # 添加请求参数名到sha1算法中
        # 对请求参数进行排序
        params = sorted(request.params.items(), key=lambda x: x[0])
        s.update(self.__to_bytes(str(params)))
        # 添加请求体名导sha1算法中
        data = sorted(request.data.items(), key=lambda x: x[0])
        s.update(self.__to_bytes(str(data)))

        return s.hexdigest()

    @staticmethod
    def __to_bytes(i):
        """无论是py2还是py3,都把字符串转换为二进制"""
        if six.PY2:
            # py2中,str类型是二进制数据,unicode类型是字符串,默认使用ASCII编码
            return i if isinstance(i, str) else i.encode('utf8')
        else:
            # py3中,str类型是字符串,bytes是二进制类型
            return i.encode('utf8') if isinstance(i, str) else i
