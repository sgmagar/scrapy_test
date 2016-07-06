import scrapy
from scrapy.http import Request, FormRequest
from scrapy.spiders import CrawlSpider
from scrapy_test.items import *
from datetime import datetime

from scrapy.conf import settings
import urllib
import csv
import json
import re
from datetime import datetime, timedelta
from dateutil import parser
from urllib import urlencode
from HTMLParser import HTMLParser

from scrapy_test.lib.phillips_parser import PhillipsParser


class PhillipsSpider(CrawlSpider):
    name = "phillips"

    allowed_domains = ["phillips.com"]

    start_urls = ['http://www.phillips.com']
    base_url = 'https://www.phillips.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Firefox/3.6.10 GTB7.1',
        'Accept-Language': 'en-us,en;q=0.5'
    }

    htmlParser =  PhillipsParser()

    def __init__(self, *args, **kwargs):
        super(PhillipsSpider, self).__init__(*args, **kwargs)
        settings.set('RETRY_HTTP_CODES', [500, 503, 504, 400, 408, 404] )
        settings.set('RETRY_TIMES', 5 )
        settings.set('REDIRECT_ENABLED', True)
        settings.set('METAREFRESH_ENABLED', True)
        settings.set('USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_auction_list, headers=self.headers)

    def parse_auction_list(self, response):
        ahref = response.xpath('//*[@id="primary-nav"]/ul/li[1]/ul/li/a/@href').extract()
        href = ahref[:-2]
        for link in href:
            yield Request(url=self.base_url+link,
                callback=self.parse_product_list,
                headers=self.headers)


    def parse_product_list(self, response):
      catalogueUrl = response.url
      url = self.htmlParser.get_product_list_url(response)
      if url:
        url = self.htmlParser.get_detail_url(self.base_url,url)
        for link in url:
          yield Request(url=link,
            callback=self.parse_product,
            headers=self.headers,
            meta={'catalogueUrl': catalogueUrl}
            )

    def parse_product(self, response):
        item = Product()
        url = self.htmlParser.get_url(response)
        # product = self.productClient.getProductByUrl(url)
        product = None
        if (product is not None):
            pass
          # logging.info('Already exists: ' + url)
        else:
            item['title'] = self.htmlParser.get_title(response)
            item['description'] = self.htmlParser.get_description(response)
            item['url'] = url
            item['valuationFrom'] = self.htmlParser.get_valuation_from(response)
            item['valuationTo'] = self.htmlParser.get_valuation_to(response)
            item['currency'] = self.htmlParser.get_currency(response)
            item['image_urls'] = self.htmlParser.get_images(response)
            item['thumb'] = self.htmlParser.get_thumb(response)
            item['sourceCategories'] = self.htmlParser.get_source(response)
            item['timeOfExpiry'] = self.htmlParser.getTimeOfExpiry(response)
            item['siteId'] = 13
            item['showroom'] = self.htmlParser.getLocation(response)
            item['newestBid'] = None
            item['soldFor'] = None
            item['endedAt'] = None

            item['catalogueName'] = self.htmlParser.get_source(response)
            item['catalogueUrl'] = response.meta['catalogueUrl']
            item['catalogueLocation'] = self.htmlParser.getLocation(response)
            item['catalogueStartDate'] = self.htmlParser.getTimeOfExpiry(response)
            item['catalogueEndDate'] = self.htmlParser.getTimeOfExpiry(response)



            yield item
