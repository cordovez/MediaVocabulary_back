import scrapy
from ..items import LatScraperItem
from datetime import datetime

class LatimesSpider(scrapy.Spider):
    name = "latimes"
    allowed_domains = ["www.latimes.com"]
    start_urls = ["https://www.latimes.com/topic/op-ed"]

    def parse(self, response):
        for item in response.css('div.promo-content')[:10]:
            url = item.css('h2.promo-title a::attr(href)').get()

            yield scrapy.Request(url, callback=self.parse_article, 
                                 meta={'url': url})
            
    def parse_article(self, response):
        item = LatScraperItem()
        
        item['article_title'] = response.css('h1.headline::text').get().replace('\xa0', ' ').strip()  # noqa: E501
        item['author'] = response.css('div.author-name a::text').get()
        item['summary'] = response.css('div[data-testid="article-intro"] p::text').get()

        date_string = response.css('time ::attr(datetime)').get()
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        datetime_object = datetime.strptime(date_string, date_format)
        item['date_of_pub'] = datetime_object
        
        body = response.css('div[data-element="story-body"] p ::text').getall()
        clean_body = ''.join(body).strip()
        item['content'] = clean_body 
        item['url'] = response.meta['url']
        
        yield item
        