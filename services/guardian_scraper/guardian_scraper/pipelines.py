# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import sys
from .items import GuardianScraperItem

# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter


# class GuardianScraperPipeline:
#     def process_item(self, item, spider):
#         return item


# explanation of the following code at: 
# https://www.mongodb.com/basics/how-to-use-mongodb-to-store-scraped-data 
class MongoDBPipeline:
    
    collection = 'scrapy_items'
    
    def __init__(self, mongodb_uri, mongodb_db):
        self.mongodb_uri = mongodb_uri
        self.mongodb_db = mongodb_db
        if not self.mongodb_uri: sys.exit("You need to provide a Connection String")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodb_uri=crawler.settings.get('MONGODB_URI'),
            mongodb_db=crawler.settings.get('MONGODB_DATABASE', 'items')
        )
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]
        # start with a clean database
        self.db[self.collection].delete_many({})

    def close_spider(self, spider):
        self.client.close()
        
    def process_item(self, item, spider):
        data = dict(GuardianScraperItem(item))
        self.db[self.collection].insert_one(data)
        return item