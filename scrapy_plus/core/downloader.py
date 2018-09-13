"""下载器模块"""
import requests

from .._http.response import Response


class Downloader(object):
    """根据请求对象，发起请求，拿到响应，构造响应对象并返回"""

    @staticmethod
    def get_response(request):
        """
        发起请求获取响应数据
        :param request: 请求对象
        :return: 响应对象
        """
        if request.method.upper() == 'GET':
            # get请求，用requests模块发起get请求
            res = requests.get(request.url, params=request.params, headers=request.headers)
        elif request.method.upper() == 'POST':
            res = requests.post(request.url, data=request.data, headers=request.headers)
        else:
            raise Exception('目前只支持GET和POST请求')

        # 把requests返回的Response封装成响应对象并返回
        return Response(res.url, res.status_code, headers=res.headers, body=res.content)
