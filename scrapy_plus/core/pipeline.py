"""管道模块"""


class Pipeline(object):
    """负责处理数据对象（Item）"""

    def process_item(self, item):
        # print(item.data)

        return item
