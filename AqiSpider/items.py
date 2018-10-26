# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AqispiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	date = scrapy.Field()
	aqi = scrapy.Field()
	level = scrapy.Field()
	pm2_5 = scrapy.Field()
	pm10 = scrapy.Field()
	so2 = scrapy.Field()
	co = scrapy.Field()
	no2 = scrapy.Field()
	o3_8h = scrapy.Field()
	time = scrapy.Field()
	spider = scrapy.Field()