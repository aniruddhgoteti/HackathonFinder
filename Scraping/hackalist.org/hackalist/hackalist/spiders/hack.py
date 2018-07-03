# -*- coding: utf-8 -*-
from scrapy import Spider


class HackSpider(Spider):
    name = 'hack'
    allowed_domains = ['hackalist.org']
    start_urls = ['http://hackalist.org/']

    def parse(self, response):
        pass
