from pathlib import Path
import scrapy
from datetime import datetime


from ..items  import GuardianScraperItem

class GuardianSpider(scrapy.Spider):
    name = 'guardian'
    start_urls = ['https://www.theguardian.com/uk/commentisfree']
    
    
    @staticmethod
    def extract_if_available(selector):
        '''
        for cases where there is no value, return 'None'
        '''        
        try:
            return selector
        except AttributeError as err:
            print(err)
            return None

    
    def parse(self, response):
        for article in response.css("section.dcr-0 ol li"):
            
            base_url = 'https://www.theguardian.com'
            uri =  article.css('a').attrib['href']
            url = f'{base_url}{uri}'


            yield scrapy.Request(url, callback=self.parse_article, 
                                 meta={'url': url})
        
    def parse_article(self, response):
            item = GuardianScraperItem()

            item['article_title'] = self.extract_if_available(response.css('h1::text').get())  # noqa: E501

            author_element = response.css('a[rel="author"]')
            author_name = author_element.css('::text').get()
            if author_name is None:
                item['author'] = "Anonymous"
            else:
                item['author'] = author_name            
            item['summary'] = self.extract_if_available(response.css('div.dcr-1yi1cnj p::text').get())  # noqa: E501
            
            raw_date = self.extract_if_available(response.css('span.dcr-u0h1qy::text').get()[0:21])  # noqa: E501, F821
            if raw_date is not None:
                # Define the format of the date string based on its structure
                date_format = "%a %d %b %Y %H.%M"
                datetime_object = datetime.strptime(raw_date, date_format)

                item['date_of_pub'] = datetime_object
            else:
                item['date_of_pub'] = None
                    
            text = self.extract_if_available(response.css('div.article-body-commercial-selector.article-body-viewer-selector p ::text').getall())  # noqa: E501
            
           
            item['content'] = ''.join(text).strip() 
          
            item['url'] = response.meta['url']
            
            yield item

