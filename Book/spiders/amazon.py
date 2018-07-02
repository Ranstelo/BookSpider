# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from Book.items import AmazonItem
import time
import re

class AmazonSpider(RedisCrawlSpider):
    name = 'amazon'
    allowed_domains = ['amazon.cn']
    # start_urls = ['https://www.amazon.cn/s/ref=nb_sb_noss?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&url=search-alias%3Dstripbooks']
    redis_key = "amazon"


    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//div[@class='a-row a-expander-container a-expander-extend-container']//li")), follow=True),
        Rule(LinkExtractor(restrict_xpaths=("//div[@id='mainResults']/ul/li//h2/..")), callback="book_detail"),
        Rule(LinkExtractor(restrict_xpaths=("//div[@id='pagn']",)), follow=True)
    )

    def book_detail(self, response):
        print("===========  ")
        item = AmazonItem()
        item["book_name"] = response.xpath("//span[@class='a-size-large']/text()").extract_first()
        # item["book_time"] = response.xpath("//h1[@id='title']/span[last()]/text()").extract_first().replace("– ","")
        item["book_author"] = response.xpath("//div[@id='bylineInfo']/span/a/text()").extract()
        item["book_author"] = response.xpath("//div[@id='bylineInfo']/span/a/text()").extract_first()
        item["book_cate"] = response.xpath("//div[@id='wayfinding-breadcrumbs_feature_div']/ul/li/span/a/text()").extract()
        item["book_cate"] = [i.strip() for i in item["book_cate"]]
        item["book_url"] = response.url
        item["book_press"] = response.xpath("//b[text()='出版社:']/../text()").extract_first()
        item["book_time"] = re.search(r'\(.*?\)',item["book_press"]).group()
        yield item

