"""调度器模块封装"""
from six.moves.queue import Queue


class Scheduler(object):
    """调度器
    1. 缓存请求
    2. 请求去重
    """

    def __init__(self):
        # 创建队列对象，用于缓存请求
        self.queue = Queue()
        # 定义变量，用于统计总请求数量
        self.total_request_count = 0

    def add_request(self, request):
        # 添加请求到请求对列中
        self.queue.put(request)
        # 每添加一次请求，就让总请求数量加1
        self.total_request_count += 1

    def get_request(self):
        # 从队列中获取请求，并返回请求
        return self.queue.get()

    def _filter_request(self):
        """请求去重，暂不实现"""
        pass
