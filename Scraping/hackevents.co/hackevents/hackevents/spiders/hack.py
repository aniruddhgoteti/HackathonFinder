# -*- coding: utf-8 -*-
import scrapy
import datetime
from geopy.geocoders import Nominatim

from scrapy.http import Request
from scrapy import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class HackSpider(CrawlSpider):
    name = 'hack'
    allowed_domains = ['hackevents.co']
    start_urls = (
    	'https://hackevents.co/hackathons',
    	)

    def parse(self, response):
    	boxes = response.xpath('//div[@class="hackathons"]//a/@href').extract()

    	for url in boxes:

    		url_mod = "https://hackevents.co/" + url
    		if 'follow' == url_mod:
    			pass
    		elif 'q%5Bs%5D=' == url_mod:
    			pass
    		else:
    			yield Request(url_mod, callback= self.parse_application)

    	#process next pages		

    	next_page_url = response.xpath('//li[@class="next_page"]//a/@href').extract_first()
    	abs_next_page_url = response.urljoin("https://hackevents.co/" + next_page_url)
    	yield Request(abs_next_page_url)		

    def parse_application(self, response):
    	geolocator = Nominatim()
    	title = response.css('h2::text').extract_first()
    	a =  response.css('h3::text')[2].extract().strip()[6] + "/" + response.css('h3::text')[2].extract().strip()[0:4] + "/" + response.css('h3::text')[2].extract().strip()[14:19]   
    	b= response.css('h3::text')[2].extract().strip()[11] + "/" + response.css('h3::text')[2].extract().strip()[0:4] + "/" + response.css('h3::text')[2].extract().strip()[14:19]	
    	date= a + " - " + b		 
    	location=  response.css('address::text').extract()[3].strip()
    	GPS= geolocator.geocode(location).latitude,geolocator.geocode(location).longitude
    	event_URL = response.xpath('//a/@href').extract()[11].strip()
    	yield {
		'Image': print("N/A"),
		'Title of event': title,
		'Date':date,
		'Time':print("N/A"),
		'Location':location,
		'GPS':GPS,
		'Event Description':print("N/A"),
		'Prizes':print("N/A"),
		'Schedule':print("N/A"),
		'Sponsor':print("N/A"),
		"Event URL":event_URL }





		






  			

 

