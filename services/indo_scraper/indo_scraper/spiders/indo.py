import scrapy
from ..items import IndoScraperItem 

@staticmethod
def extract_if_available(item, selector):
    '''
    for cases where there is no value, return 'None'
    '''        
    try:
       return item.css(selector).get()
    except AttributeError as err:
        print(err)
        return None
    
    
class IndoSpider(scrapy.Spider):
    name = "indo"
    allowed_domains = ["www.independent.ie"]
    start_urls = ["https://www.independent.ie/opinion/editorial"]

    def parse(self, response):
        for item in response.css('li a[data-teaser-type="free"]')[:10]:
            article_title = extract_if_available(item, 'h4 span::text')
            url = extract_if_available(item, 'a::attr("data-vr-contentbox-url")')
            
            yield scrapy.Request(url, callback=self.parse_article, 
                                 meta={'url': url})  
    
    def parse_article(self, response):
        item = IndoScraperItem()
        
        item['article_title'] = response.css('header h1::text').get()
        item['author'] = response.css('span[data-testid="article-author"]::text').get()
        item['summary'] = response.css('div[data-testid="article-intro"] p::text').get()
        item['date_of_pub'] = response.css('time[data-testid="article-date"]::text').get()[4:14]
        
        first_paragraph = response.css('div[data-testid="article-intro"] p::text').get()
        body = response.css('div[data-testid="article-body"] p::text').getall()
        clean_body = ''.join(body).strip()
        text = f'{first_paragraph}\n{clean_body}'
        item['content'] = text 
        item['url'] = response.meta['url']
        
        yield item

