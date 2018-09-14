"""Response对象"""
import json
import re

from lxml import etree


class Response(object):
    """框架内置Response对象"""

    def __init__(self, url, status_code, headers={}, body=None, meta={}):
        """
        :param url: 响应的URL
        :param status_code: 状态码
        :param headers: 响应头
        :param body: 响应的数据（二进制的）
        """
        self.url = url
        self.status_code = status_code
        self.headers = headers
        self.body = body
        self.meta = meta

    def xpath(self, rule):
        """
        用xpath来提取响应中的数据
        :param rule: xpath的路径表达式
        :return: 使用xpath获取的结果
        """
        # 把响应数据转换为Element对象
        element = etree.HTML(self.body)
        # 使用xpath来提取数据，返回列表，如果没有获取到数据就返回一个空列表
        return element.xpath(rule)

    def find_all(self, pattern, content=None):
        """
        使用正则的findall方法来提取数据
        :param pattern: 正则表达式
        :param content: 被匹配的字符串，如果为None，就是response.body
        :return: 匹配的结果
        """
        if content is None:
            content = self.body.decode()

        # 使用正则在content中提取数据
        result = re.findall(pattern, content)

        return result

    def json(self):
        """
        用于解析json数据，要求整个响应是一个json字符串
        :return: json对应的python类型数据
        """
        return json.loads(self.body.decode())
