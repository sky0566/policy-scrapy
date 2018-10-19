# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PolicyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 发布部门
    department = scrapy.Field()

    # 发布日期
    date = scrapy.Field()

    # 政策名称
    name = scrapy.Field()

    # 政策预览
    overview = scrapy.Field()

    # 政策内容
    content = scrapy.Field()


