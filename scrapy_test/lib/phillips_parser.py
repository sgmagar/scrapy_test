# -*- coding: utf-8 -*-
import re
import json
from dateutil import parser
import logging

class PhillipsParser():
  def get_product_list_url(self, response):
    return response.xpath('//div[@class="image"]/a/@href').extract()

  def get_detail_url(self, base_url, url_list):
    detail_url_list = []
    for link in url_list:
      link_item = link.split('/')
      url = base_url + '/getdetail/' + link_item[-2] +  '/' +link_item[-1]
      detail_url_list.append(url)

    return detail_url_list

  def get_title(self, response):
    data = response.xpath('//p').extract()[0][3:-4]
    json_data = json.loads(data)
    try:
      return json_data['Lot']['Title'] + ', ' + json_data['Lot']['Circa']
    except Exception:
      return ''


  def get_description(self, response):
    data = response.xpath('//p').extract()[0][3:-4]
    json_data = json.loads(data)
    try:
      return json_data['Lot']['Medium'] + ' ' + json_data['Lot']['Dimensions'] + ' ' + json_data['Lot']['SigEdtMan']
    except Exception:
      return ''
  def get_url(self, response):
    data = response.xpath('//p').extract()[0][3:-4]
    json_data = json.loads(data)
    try:
      return 'https://www.phillips.com' + json_data['Lot']['DetailLink']
    except Exception:
      return ''
  def get_valuation_from(self, response):
    data = response.xpath('//p').extract()[0][3:-4]
    json_data = json.loads(data)
    try:
      return int(json_data['Lot']['LowEstimate'])
    except Exception:
      return ''

  def get_valuation_to(self, response):
    data = response.xpath('//p').extract()[0][3:-4]
    json_data = json.loads(data)
    try:
      return int(json_data['Lot']['HighEstimate'])
    except Exception:
      return ''

  def get_currency(self, response):
    data = response.xpath('//p').extract()[0][3:-4]
    json_data = json.loads(data)
    try:
      currency = json_data['Lot']['CurrencySign']
    except Exception:
      currency = ''
    if currency == u'\x24':
      return 'USD'
    elif currency == u'\xa3':
      return 'GBP'
    else:
      return currency

  def get_thumb(self, response):
    data = response.xpath('//p').extract()[0][3:-4]
    json_data = json.loads(data)
    try:
      return json_data['Lot']['ImagePath'] + '/172/220'
    except Exception:
      return ''

  def get_images(self, response):
    data = response.xpath('//p').extract()[0][3:-4]
    json_data = json.loads(data)
    try:
      return [json_data['Lot']['ImagePath']]
    except Exception:
      return ''

  def get_source(self, response):
    data = response.xpath('//p').extract()[0][3:-4]
    json_data = json.loads(data)
    try:
      return json_data['Lot']['Auction']['Title']
    except Exception:
      return ''

  def getLocation(self, response):
    data = response.xpath('//p').extract()[0][3:-4]
    json_data = json.loads(data)
    try:
      d = json_data['Lot']['Auction']['DetailsSmall']
      return d.split('Auction')[0].strip()
    except Exception:
      return ''

  def getTimeOfExpiry(self, response):
    data = response.xpath('//p').extract()[0][3:-4]
    json_data = json.loads(data)
    d = json_data['Lot']['Auction']['DetailsSmall']
    date = d.split('Auction')[1].strip().replace('&nbsp;', '')
    date = parser.parse(date)
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')
