# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from Book.items import AmazonItem

client = MongoClient()
collection = client["book"]["amazon"]

class BookPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,AmazonItem):
            collection.insert(dict(item))
            print("保存成功")

        return item
