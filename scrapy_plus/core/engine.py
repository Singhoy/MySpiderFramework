"""引擎组件"""
import importlib
import time
from collections import Iterable
from datetime import datetime

from scrapy_plus.core.downloader import Downloader
from scrapy_plus.core.scheduler import Scheduler
from scrapy_plus.utils.log import logger
from scrapy_plus.win_http.request import Request
from scrapy_plus.conf import settings

# 根据异步类型导入不同的池
if settings.ASYNC_TYPE.lower() == 'thread':
    # 异步类型是线程，导入线程池
    from multiprocessing.dummy import Pool
else:
    from scrapy_plus.async.coroutine import Pool
# 导入统计器类
if not settings.SCHEDULER_PERSIST:
    # 不支持分布式，导入内存版指纹容器
    from scrapy_plus.utils.stats_collector import NormalStatsCollector as StatsCollector
else:
    # 支持分布式，导入redis版指纹容器
    from scrapy_plus.utils.stats_collector import RedisStatsCollector as StatsCollector


class Engine(object):
    """
    1.对其他模块进行初始化
    2.启动引擎（实现引擎调用核心逻辑）
    """

    def __init__(self):
        self.spiders = self.__auto_import(settings.SPIDERS, is_spider=True)  # 这里传递过来的是一个字典{爬虫名：爬虫对象}
        # 创建统计器对象
        self.stats_collector = StatsCollector()
        # 把统计器对象传递给调度器
        self.scheduler = Scheduler(self.stats_collector)
        self.downloader = Downloader()
        self.pipelines = self.__auto_import(settings.PIPELINES)
        self.spider_middlewares = self.__auto_import(settings.SPIDER_MIDDLEWARES)
        self.downloader_middlewares = self.__auto_import(settings.DOWNLOADER_MIDDLEWARES)
        self.pool = Pool()  # 创建线程池对象
        # 定义变量，用于记录起始请求完成的爬虫数量
        self.start_request_finished_spider_count = 0

    @staticmethod
    def __auto_import(full_names, is_spider=False):
        """
        动态导入:根据配置信息自动创建对象,封装成需要的格式返回
        :param full_names: 配置全类名(路径)列表
        :param is_spider: 判断是不是爬虫对象
        :return: 配置类的对象列表或者字典
        """
        # 如果是爬虫就是字典,否则是列表
        instances = {} if is_spider else []
        for full_name in full_names:
            result = full_name.rsplit('.', maxsplit=1)
            # 模块名
            module_name = result[0]
            # 类名
            class_name = result[1]
            # 根据模块名,导入模块,获取模块对象
            module = importlib.import_module(module_name)
            # 根据类名,从模块对象中获取类对象
            cls = getattr(module, class_name)
            # 使用类对象,创建实例对象
            instance = cls()
            # 如果是爬虫,存储到字典中,否则存到列表里
            if is_spider:
                instances[instance.name] = instance
            else:
                instances.append(instance)

        return instances

    def start(self):
        """启动引擎，对外提供接口"""
        start = datetime.now()
        logger.info("开始运行时间：%s" % start)
        self.__start()
        stop = datetime.now()
        logger.info("运行结束时间：%s" % stop)
        logger.info("耗时：%.2f秒" % (stop - start).total_seconds())
        # 总起始请求数量
        logger.info('总起始请求数量:%s' % self.stats_collector.start_request_nums)
        # 记录总请求数量
        logger.info('总请求数量：%s' % self.stats_collector.request_nums)
        # 总过滤请求数量
        logger.info('过滤掉的请求数量:%s' % self.stats_collector.repeat_request_nums)
        # 总响应数量
        logger.info('总响应处理数量：%s' % self.stats_collector.response_nums)
        # 如果启用分布式，当前程序结束的时候，清空统计信息
        if settings.SCHEDULER_PERSIST:
            self.stats_collector.clear()
            if not settings.FP_PERSIST:
                # 如果不开启断点续爬，清空指纹和请求队列数据
                self.scheduler.clear()

    @staticmethod
    def __error_callback(e):
        """错误回调函数"""
        try:
            raise e
        except Exception as e:
            logger.exception(e)

    def __callback_execute(self, temp):
        """异步线程池回调函数"""
        self.pool.apply_async(self.__execute_request_response_item, callback=self.__callback_execute,
                              error_callback=self.__error_callback)

    def __start(self):
        """私有启动引擎的方法，实现核心代码"""
        # 添加起始请求到调度器中
        # 异步执行__add_start_requests任务
        self.pool.apply_async(self.__add_start_requests, error_callback=self.__error_callback)

        # 配置多少个异步任务，这个异步调用就执行多少次
        for i in range(settings.ASYNC_COUNT):
            # 异步执行__execute_request_response_item任务
            self.pool.apply_async(self.__execute_request_response_item, callback=self.__callback_execute,
                                  error_callback=self.__error_callback)

        # 让主线程等待一下，让上面的异步任务启动起来
        time.sleep(1)

        while True:
            # 死循环进行轮询，非常消耗cpu性能，稍睡一下，降低消耗
            time.sleep(0.1)

            # 当所有爬虫的起始请求都执行完了才结束
            if self.start_request_finished_spider_count >= len(self.spiders):
                # 当所有请求都处理完成，要结束循环
                if self.stats_collector.response_nums >= self.stats_collector.request_nums:
                    # 没有请求了，退出循环
                    break

    def __execute_request_response_item(self):
        """处理请求、响应和数据方法"""
        # 从调度器获取请求对象，交给下载器发起请求，获取一个响应对象
        request = self.scheduler.get_request()

        # 取出该请求对应爬虫对象，根据爬虫名去爬虫字典中取出爬虫对象
        spider = self.spiders[request.spider_name]

        # 遍历下载器中间件列表,获取每一个下载器中间件
        for downloader_middleware in self.downloader_middlewares:
            # 利用下载器中间件预处理请求对象
            request = downloader_middleware.process_request(request)
        # 利用下载器发起请求
        response = self.downloader.get_response(request)
        # 把请求的meta数据传递给response
        response.meta = request.meta

        # 利用下载器中间件预处理响应对象
        # 遍历下载器中间件列表,获取每个下载器中间件
        for downloader_middleware in self.downloader_middlewares:
            response = downloader_middleware.process_response(response)

        # 遍历爬虫中间件列表,获取每一个爬虫中间件
        for spider_middleware in self.spider_middlewares:
            # 调用爬虫中间件的process_response方法，处理响应
            response = spider_middleware.process_response(response)

        # 如果有该请求有对应解析函数callback，就使用callback来解析数据
        if request.callback:
            # 接收解析函数，处理结果
            results = request.callback(response)
        else:
            # 如果没有callback就使用parse函数来解析数据
            results = spider.parse(response)

        # 判断results是不是可迭代对象，如果不可迭代，变为可迭代的
        if not isinstance(results, Iterable):
            results = [results]
        for result in results:
            # 判断结果对象
            if isinstance(result, Request):
                # 如果是请求对象，就再交给调度器
                # 遍历爬虫中间件列表,获取每个爬虫中间件
                for spider_middleware in self.spider_middlewares:
                    # 利用爬虫中间件预处理请求对象
                    result = spider_middleware.process_request(result)

                # 设置请求对象对应的爬虫名
                result.spider_name = spider.name

                self.scheduler.add_request(result)
            else:
                # 否则，交给管道处理
                for pipeline in self.pipelines:
                    result = pipeline.process_item(result, spider)

        # 统计总的响应数量，每次递增1
        self.stats_collector.incr(self.stats_collector.response_nums_key)

    def __add_start_requests(self):
        # 遍历爬虫字典，取出爬虫对象
        for spider_name, spider in self.spiders.items():
            # 异步执行起始请求任务，防止有增量爬虫启动后不停止而后面的爬虫不执行的问题
            self.pool.apply_async(self.__add_one_spider_start_requests, args=(spider, spider_name),
                                  error_callback=self.__error_callback,
                                  callback=self.__add_one_spider_start_requests_callback)

    def __add_one_spider_start_requests_callback(self, temp):
        """每调用一次，起始请求完成数+1"""
        self.start_request_finished_spider_count += 1

    def __add_one_spider_start_requests(self, spider, spider_name):
        # 调用爬虫start_request方法，获取请求对象
        for request in spider.start_request():
            # 设置该请求对应的爬虫名
            request.spider_name = spider_name

            # 统计起始请求数量
            self.stats_collector.incr(self.stats_collector.start_request_nums_key)

            # 利用爬虫中间件预处理请求对象
            # 遍历爬虫中间件列表,获取每个爬虫中间件
            for spider_middleware in self.spider_middlewares:
                request = spider_middleware.process_request(request)
            # 调用调度器的add_request把请求添加到调度器中
            self.scheduler.add_request(request)
