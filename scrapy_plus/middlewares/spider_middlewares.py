"""爬虫中间件"""


class SpiderMiddleware(object):

    @staticmethod
    def process_request(request):
        """用于处理请求对象"""
        print('SpiderMiddleware的process_request处理请求：', request.url)

        return request

    @staticmethod
    def process_response(response):
        """用于处理响应对象"""
        print('SpiderMiddleware的process_response处理响应：', response.url)

        return response
