"""调度器模块封装"""
from hashlib import sha1

import six
from six.moves.queue import Queue
from w3lib.url import canonicalize_url

from scrapy_plus.utils.log import logger


class Scheduler(object):
    """调度器
    1. 缓存请求
    2. 请求去重
    """

    def __init__(self):
        # 创建队列对象，用于缓存请求
        self.queue = Queue()
        # 定义变量,用于统计总请求数量
        self.total_request_count = 0
        # 创建set集合,用于存储指纹数据
        self.__filter_container = set()
        # 定义变量,用于统计过滤掉的请求数量
        self.filtered_request_count = 0

    def add_request(self, request):
        """添加请求到请求对列中"""
        if self.__filter_request(request):
            # 如果请求需要过滤,记录日志,直接返回
            logger.info('过滤掉了重复的请求:%s' % request.url)
            self.filtered_request_count += 1
            return

        self.queue.put(request)
        # 每添加一次请求，就让总请求数量加1
        self.total_request_count += 1

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
        if fp in self.__filter_container:
            return True

        # 能来到这里,说明这个请求是全新的,把指纹添加到指纹容器中
        self.__filter_container.add(fp)
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
