"""指纹容器，用于存储指纹信息"""
import redis

from scrapy_plus.conf.settings import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_SET_NAME


class BasicFilterContainer(object):
    """指纹容器基类，用于定义指纹容器接口"""

    def add_fp(self, fp):
        """添加指纹"""
        pass

    def exists(self, fp):
        """判断指纹是否重复"""
        pass


class NormalFilterContainer(BasicFilterContainer):
    """基于set的内存版指纹容器"""

    def __init__(self):
        self.__container = set()

    def add_fp(self, fp):
        """添加指纹到set中"""
        self.__container.add(fp)

    def exists(self, fp):
        """判断指纹是否重复"""
        if fp in self.__container:
            return True
        else:
            return False


class RedisFilterContainer(BasicFilterContainer):
    """基于redis的set的指纹容器"""

    def __init__(self):
        """连接redis数据库"""
        self.redis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        # 记录在redis中的key
        self.name = REDIS_SET_NAME

    def add_fp(self, fp):
        """添加指纹"""
        self.redis.sadd(self.name, fp)

    def exists(self, fp):
        """判断指纹是否重复，重复返回True，否则返回False"""
        return self.redis.sismember(self.name, fp)

    def clear(self):
        """清空指纹"""
        self.redis.delete(self.name)
