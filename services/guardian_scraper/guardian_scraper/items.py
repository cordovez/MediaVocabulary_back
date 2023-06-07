# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GuardianScraperItem(scrapy.Item):
    article_title = scrapy.Field()
    summary = scrapy.Field()
    author = scrapy.Field()
    date_of_pub = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    

    