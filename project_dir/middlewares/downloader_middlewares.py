"""下载器中间件"""


class DownloaderMiddleware1(object):

    def process_request(self, request):
        """用于处理请求对象"""
        print('下载器中间件1的process_request处理请求:%s' % request.url)
        # 返回处理后的请求对象
        return request

    def process_response(self, response):
        """用于处理响应对象"""
        print('下载器中间件1的process_response处理响应:%s' % response.url)

        return response


class DownloaderMiddleware2(object):

    def process_request(self, request):
        """用于处理请求对象"""
        print('下载器中间件2的process_request处理请求:%s' % request.url)
        # 返回处理后的请求对象
        return request

    def process_response(self, response):
        """用于处理响应对象"""
        print('下载器中间件2的process_response处理响应:%s' % response.url)

        return response
