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
            
