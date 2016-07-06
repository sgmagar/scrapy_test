# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Product(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    valuationFrom = scrapy.Field()
    valuationTo = scrapy.Field()
    showroom = scrapy.Field()
    timeOfExpiry = scrapy.Field()
    newestBid = scrapy.Field()
    thumb = scrapy.Field()
    images = scrapy.Field()
    sourceCategories = scrapy.Field()
    currency = scrapy.Field()
    soldFor = scrapy.Field()
    endedAt = scrapy.Field()
    siteId = scrapy.Field()
    id = scrapy.Field()
    image_urls = scrapy.Field()
    thumb_path = scrapy.Field()
    startingPrice = scrapy.Field()
    catalogueName = scrapy.Field()
    catalogueUrl = scrapy.Field()
    catalogueStartDate = scrapy.Field()
    catalogueEndDate = scrapy.Field()
    catalogueLocation = scrapy.Field()
