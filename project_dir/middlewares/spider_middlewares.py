"""爬虫中间件"""


class SpiderMiddleware1(object):

    def process_request(self, request):
        print('爬虫中间件1的process_request处理请求:%s' % request.url)
        return request

    def process_response(self, response):
        print('爬虫中间件1的process_response处理请求:%s' % response.url)
        return response


class SpiderMiddleware2(object):

    def process_request(self, request):
        print('爬虫中间件2的process_request处理请求:%s' % request.url)
        return request

    def process_response(self, response):
        print('爬虫中间件2的process_response处理请求:%s' % response.url)
        return response
