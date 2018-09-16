import pickle
import time

import redis
from six.moves import queue as base_queue

from scrapy_plus.conf.settings import REDIS_QUEUE_NAME, REDIS_HOST, REDIS_PORT, REDIS_DB


class Queue(object):
    """利用redis实现Queue，使接口跟python内置的队列接口一致，实现无缝转换"""
    Empty = base_queue.Empty
    Full = base_queue.Full
    max_timeout = 0.3

    def __init__(self, maxsize=0, name=REDIS_QUEUE_NAME, host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, lazy_limit=True,
                 password=None):
        """
        重构redis队列
        :param maxsize: 设置队列上限
        :param lazy_limit:  惰性限制redis共享队列大小
        """
        self.name = name
        self.redis = redis.StrictRedis(host=host, port=port, db=db, password=password)
        self.maxsize = maxsize
        self.lazy_limit = lazy_limit
        self.last_qsize = 0

    def qsize(self):
        self.last_qsize = self.redis.llen(self.name)
        return self.last_qsize

    def empty(self):
        if self.qsize() == 0:
            return True
        else:
            return False

    def full(self):
        if self.maxsize and self.qsize() >= self.maxsize:
            return True
        else:
            return False

    def put_nowait(self, obj):
        if self.lazy_limit and self.last_qsize < self.maxsize:
            pass
        elif self.full():
            raise self.Full
        self.last_qsize = self.redis.rpush(self.name, pickle.dumps(obj))  # pickle.dumps(obj) 把对象转化为二进制
        return True

    def put(self, obj, block=True, timeout=None):
        if not block:
            return self.put_nowait(obj)
        start = time.time()
        while True:
            try:
                return self.put_nowait(obj)
            except self.Full:
                if timeout:
                    lasted = time.time() - start
                    if timeout > lasted:
                        time.sleep(min(self.max_timeout, timeout - lasted))
                    else:
                        raise
                else:
                    time.sleep(self.max_timeout)

    def get_nowait(self):
        ret = self.redis.lpop(self.name)
        if ret is None:
            raise self.Empty

        return pickle.loads(ret)  # pickle.loads(ret)把二进制字符串转化为对象，反序列化

    def get(self, block=True, timeout=None):
        if not block:
            return self.get_nowait()
        start = time.time()
        while True:
            try:
                return self.get_nowait()
            except self.Empty:
                if timeout:
                    lasted = time.time() - start
                    if timeout > lasted:
                        time.sleep(min(self.max_timeout, timeout - lasted))
                    else:
                        raise
                else:
                    time.sleep(self.max_timeout)

    def clear(self):
        """清空队列"""
        self.redis.delete(self.name)
