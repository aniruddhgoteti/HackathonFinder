# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HackathonsnearItem(scrapy.Item):
	image: scrapy.Field()
	title: scrapy.Field()
	Date: scrapy.Field()
	Time: scrapy.Field()
	Location: scrapy.Field()
	GPS: scrapy.Field()
	Event_Description: scrapy.Field()
	Prizes: scrapy.Field()
	Schedule: scrapy.Field()
	Sponsor: scrapy.Field()
	Event_URL: scrapy.Field()
