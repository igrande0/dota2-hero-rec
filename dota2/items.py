# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Dota2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
  name = scrapy.Field()
  success = scrapy.Field()
  hero = scrapy.Field()
  played = scrapy.Field()
  winrate = scrapy.Field()
  kda = scrapy.Field()
  pass
