"""item对象"""


class Item(object):
    """框架内置Item对象"""

    def __init__(self, data):
        """
        :param data: 封装的数据
        """
        self._data = data

    @property
    def data(self):
        # 返回数据
        return self._data
