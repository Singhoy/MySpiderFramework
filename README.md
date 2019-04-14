# MySpiderFramework
This framework referenced from scrapy.

Scrapy

    # 创建项目
    scrapy startproject 项目名
    # 生成爬虫
    scrapy genspider 爬虫名 域名
    # 完善爬虫代码
    	# 提取数据或请求
    # 保存数据
    	# 在pipeline中保存数据
    # 启动爬虫
    scrapy crawl 爬虫名 [-o 保存文件名.文件格式]



    response.xpath() 返回的结果是selector对象，用extract()或者extract_first()提取数据

scrapy.Request()

    scrapy.Request(url[, callback, method='GET', headers, body, cookies, meta, dont_filter=False])
    	# 可选参数
        callback: 当前url交给谁处理
        method: 指定POST或GET请求
        headers: 接收一个字典，不包括cookies
        cookies: 接收一个字典，专门放置cookies
        body: 接收一个字典，为POST的数据
        meta: 数据在不同的解析函数中传递
        dont_filter: 默认False，会过滤请求过的url地址，需要重复请求的url设为True


