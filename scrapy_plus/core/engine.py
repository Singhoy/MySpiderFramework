"""引擎组件"""
from collections import Iterable
from datetime import datetime

from scrapy_plus.core.downloader import Downloader
from scrapy_plus.core.pipeline import Pipeline
from scrapy_plus.core.scheduler import Scheduler
from scrapy_plus.middlewares.downloader_middlewares import DownloaderMiddleware
from scrapy_plus.middlewares.spider_middlewares import SpiderMiddleware
from scrapy_plus.utils.log import logger
from scrapy_plus.win_http.request import Request


class Engine(object):
    """
    1.对其他模块进行初始化
    2.启动引擎（实现引擎调用核心逻辑）
    """

    def __init__(self, spiders, pipelines, downloader_middlewares, spider_middlewares):
        self.spiders = spiders  # 这里传递过来的是一个字典{爬虫名：爬虫对象}
        self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.pipelines = pipelines
        self.spider_middlewares = spider_middlewares
        self.downloader_middlewares = downloader_middlewares

        # 定义变量，用于统计总的响应处理数量
        self.total_response_count = 0

    def start(self):
        """启动引擎，对外提供接口"""
        start = datetime.now()
        logger.info("开始运行时间：%s" % start)
        self.__start()
        stop = datetime.now()
        logger.info("运行结束时间：%s" % stop)
        logger.info("耗时：%.2f秒" % (stop - start).total_seconds())
        # 记录总请求数量
        logger.info('总请求数量：%s' % self.scheduler.total_request_count)
        # 总响应数量
        logger.info('总响应处理数量：%s' % self.total_response_count)

    def __start(self):
        """私有启动引擎的方法，实现核心代码"""
        # 添加起始请求到调度器中
        self.__add_start_requests()

        while True:
            # 从调度器中，获取请求进行处理
            self.__execute_request_response_item()
            # 当所有请求都处理完成，要结束循环
            if self.total_response_count >= self.scheduler.total_request_count:
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
        self.total_response_count += 1

    def __add_start_requests(self):
        # 遍历爬虫字典，取出爬虫对象
        for spider_name, spider in self.spiders.items():
            # 调用爬虫start_request方法，获取请求对象
            for request in spider.start_request():
                # 设置该请求对应的爬虫名
                request.spider_name = spider_name

                # 利用爬虫中间件预处理请求对象
                # 遍历爬虫中间件列表,获取每个爬虫中间件
                for spider_middleware in self.spider_middlewares:
                    request = spider_middleware.process_request(request)
                # 调用调度器的add_request把请求添加到调度器中
                self.scheduler.add_request(request)
