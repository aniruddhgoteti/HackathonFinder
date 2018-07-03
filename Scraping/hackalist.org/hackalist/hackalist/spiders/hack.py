# -*- coding: utf-8 -*-
from scrapy import CrawlSpider
from geopy.geocoders import Nominatim
from selenium import selenium

from scrapy.http import Request
from scrapy import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector


def __init__(self):
        CrawlSpider.__init__(self)
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://www.domain.com")
        self.selenium.start()

        
class HackSpider(CrawlSpider):
    name = 'hack'
    allowed_domains = ['hackalist.org']
    start_urls = (
    	'http://hackalist.org/',
    	)

    def parse(self, response):
        pass
