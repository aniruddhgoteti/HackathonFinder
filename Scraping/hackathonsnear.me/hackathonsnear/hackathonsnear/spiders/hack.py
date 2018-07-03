# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from collections import OrderedDict
from hackathonsnear.items import HackathonsnearItem



class HackSpider(scrapy.Spider):
    name = 'hack'
    allowed_domains = ['http://hackathonsnear.me/']
    start_urls = ['http://hackathonsnear.me//']

    def __init__(self):
        self.driver = webdriver.Chrome()


    def parse(self, response):
        
        self.driver.get(response.url)

        

        item= HackathonsnearItem()

        sel= Selector(text= self.driver.page_source)

        titles= sel.xpath('//a[@class="hackathon-name ng-binding"]//text()').extract()

        for title in titles:
            item['title']= title


        dates= sel.xpath('//div[@class="columns small-3 medium-2 large-3 ng-binding"]//text()').extract()

        location= sel.xpath('//div[@class="columns small-4 medium-3 large-2 ng-binding"]//text()').extract()

        t=sel.xpath('//a/@href').extract()

        url= list(OrderedDict.fromkeys(t))

        #for title in titles:
        #   print(title)

