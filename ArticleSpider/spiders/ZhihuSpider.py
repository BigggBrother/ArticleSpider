# -*- coding: utf-8 -*-
import scrapy
import urlparse as parse
from scrapy.loader import ItemLoader

class ZhihuspiderSpider(scrapy.Spider):
    name = 'ZhihuSpider'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    def parse(self, response):
        pass

    def start_requests(self):
        return [scrapy.Request("https://www.zhihu.com/#signin", headers=self.headers, callback=self.login)]

    def login(self,response):
        #todo
        pass

