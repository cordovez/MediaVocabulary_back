
import scrapy
from ..items import SmhScraperItem
from datetime import datetime

class SmhSpider(scrapy.Spider):
    name = "smh"
    allowed_domains = ["www.smh.com.au"]
    start_urls = ["https://www.smh.com.au/opinion"]

    def parse(self, response):
        for article in response.xpath('//div[contains(@class, "X3yYQ") and contains(@class, "undefined") and contains(@class, "_3lPXs")]')[:10]:  # noqa: E501
            article_title = article.css('h3[data-testid="article-headline"] a::text').get()  # noqa: E501
            author = article.css('ul li span[data-testid="byline"]::text').get()
            summary = article.css('p::text').get() 
            
            date_string = article.css('ul li time[datetime]::attr(datetime)').get()
            date_format = "%Y-%m-%dT%H:%M:%S%z"
            datetime_object = datetime.strptime(date_string, date_format)
            date = datetime_object
            
            base_url = "https://www.smh.com.au"
            uri =  article.css('h3 a::attr(href)').get() 
            url = f'{base_url}{uri}'
            
            yield scrapy.Request(url, callback=self.parse_article, meta={'url': url, 'article_title': article_title, 'author': author, 'summary': summary, 'date_of_pub': date })  # noqa: E501
            
    def parse_article(self, response):
        item = SmhScraperItem()

        item['article_title'] = response.meta['article_title']
        item['author'] = response.meta['author']
        item['summary'] = response.meta['summary']
        item['date_of_pub'] = response.meta['date_of_pub']
        
        text = response.css('div[data-testid="body-content"] p::text').getall()  # noqa: E501
        item['content'] = ''.join(text).strip() 
        item['url'] = response.meta['url']
        
        yield item        
"""
        
        from pathlib import Path
import scrapy

from ..items  import GuardianScraperItem

class GuardianSpider(scrapy.Spider):
    name = 'guardian'
    start_urls = ['https://www.theguardian.com/uk/commentisfree']

    
    def parse(self, response):
        for article in response.css("section.dcr-0 ol li"):
            
            base_url = 'https://www.theguardian.com'
            uri =  article.css('a').attrib['href']
            url = f'{base_url}{uri}'

            yield scrapy.Request(url, callback=self.parse_article, meta={'url': url})
        
    def parse_article(self, response):
            item = GuardianScraperItem()

            item['article_title'] = response.css('div.dcr-0 h1::text').get()
            item['author'] = response.css('div.dcr-0 a::text').get()
            item['summary'] = response.css('div.dcr-1yi1cnj p::text').get()
            item['date_of_pub'] = response.css('summary.dcr-1ybxn6r span::text').get()[:14]
            text = response.css('div.article-body-commercial-selector.article-body-viewer-selector.dcr-1r94quw p.dcr-94xsh ::text').getall()  # noqa: E501
            item['content'] = ''.join(text).strip() 
            item['url'] = response.meta['url']
            
            yield item


        """