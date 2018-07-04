# -*- coding: utf-8 -*-
from scrapy import CrawlSpider
from geopy.geocoders import Nominatim
from selenium import selenium


from scrapy.http import Request
from scrapy import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

class hack(scrapy.Item):
    
        
class HackSpider(CrawlSpider):

    name = 'hack'
    allowed_domains = ['hackalist.org']
    start_urls = (
    	'http://hackalist.org/',
    	)

    def parse(self, response):
        pass
