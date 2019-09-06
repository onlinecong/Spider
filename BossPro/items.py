# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BossproItem(scrapy.Item):
    # 岗位名称
    jobName = scrapy.Field()
    # 薪资待遇
    salary = scrapy.Field()
    # 岗位要求
    require = scrapy.Field()
    # 岗位描述
    jobInfo = scrapy.Field()
    # 公司介绍
    companyInfo = scrapy.Field()
    # 公司规模
    companySize = scrapy.Field()
    # 公司福利
    companyFuli = scrapy.Field()
    # 公司地址
    address = scrapy.Field()

