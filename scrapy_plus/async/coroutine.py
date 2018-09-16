"""
实现一个自己的协程池
目的：该协程池的接口和线程池接口一致，在引擎中实现无缝切换
"""
from gevent import monkey

monkey.patch_all()
from gevent.pool import Pool as BasicPool


class Pool(BasicPool):

    def apply_async(self, func, args=(), kwds=None, callback=None, error_callback=None):
        # 调用父类apply_async实现协程池的异步任务
        if kwds is None:
            kwds = {}
        super().apply_async(func, args=args, kwds=kwds, callback=callback)

    def close(self):
        """线程池有close方法，但是协程池默认没有"""
        pass
