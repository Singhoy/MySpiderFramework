"""引擎组件"""
from _http.request import Request
from .pipeline import Pipeline
from .downloader import Downloader
from .scheduler import Scheduler
from .spider import Spider


class Engine(object):
    """
    1.对其他模块进行初始化
    2.启动引擎（实现引擎调用核心逻辑）
    """

    def __init__(self):
        self.spider = Spider()
        self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.pipeline = Pipeline()

    def start(self):
        """启动引擎，对外提供接口"""
        self.__start()

    def __start(self):
        """私有启动引擎的方法，实现核心代码"""
        # 爬虫起始请求
        start_request = self.spider.start_request()

        # 把起始请求添加给调度器
        self.scheduler.add_request(start_request)

        # 从调度器获取请求对象，交给下载器发起请求，获取一个响应对象
        request = self.scheduler.get_request()

        # 利用下载器发起请求
        response = self.downloader.get_response(request)

        # 利用爬虫的解析响应方法，处理响应，得到结果
        result = self.spider.parse(response)

        # 判断结果对象
        if isinstance(result, Request):
            # 如果是请求对象，就再交给调度器
            self.scheduler.add_request(result)
        else:
            # 否则，交给管道处理
            self.pipeline.process_item(result)
