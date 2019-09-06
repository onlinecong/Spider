# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from BossPro.items import BossproItem
from scrapy_redis.spiders import RedisCrawlSpider

class JobSpider(RedisCrawlSpider):
    name = 'job'
    allowed_domains = ['zhipin.com']
    # start_urls = ['https://www.zhipin.com/c101010100-p100109/?page=1&ka=page-1']

    redis_key = "job:start_urls"

    rules = (
        Rule(LinkExtractor(allow=r'page=\d+'), callback='parse_item', follow=True),
        # /c101010100-p100109/?page=2
    )

    def parse_item(self, response):
        joblist = response.xpath("//div[@class='job-list']//li")
        for job in joblist:
            # 一级页面没有item中的字段，匹配出下级页面url，请求下级页面取解析
            next_url = "https://www.zhipin.com" + job.xpath(".//div[@class='info-primary']//h3/a/@href").extract_first()
            yield scrapy.Request(url=next_url,callback=self.parse_info)

    # 封装一个回调函数，用于解析职位详情页
    def parse_info(self, response):
        # print(response)
        item = BossproItem()
        item["jobName"] = response.xpath("//div[@class='info-primary']//h1/text()").extract_first()
        item["salary"] = response.xpath("//span[@class='salary']/text()").extract_first()
        item["require"] = " ".join(response.xpath("//div[starts-with(@class,'job-primary')]/div[@class='info-primary']//p//text()").extract()[1:])
        item["jobInfo"] = "".join(response.xpath("//div[@class='job-sec']/div[@class='text']/text()").extract())
        item["companyInfo"] = "".join(response.xpath("//div[@class='job-sec company-info']/div[@class='text']/text()").extract())
        item["companySize"] = " ".join(response.xpath("//div[@class='sider-company']/p//text()").extract()[1:4])
        item["companyFuli"] = " ".join(response.xpath("//div[@class='job-tags']")[0].xpath(".//text()").extract())
        item["address"] = response.xpath("//div[@class='location-address']/text()").extract_first()
        yield item
