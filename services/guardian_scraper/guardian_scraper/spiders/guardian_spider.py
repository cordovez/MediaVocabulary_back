import scrapy
import re

class GuardianSpider(scrapy.Spider):
    name = 'guardian'
    start_urls = ['https://www.theguardian.com/uk/commentisfree']
    
    def parse(self, response):
        for articles in response.css("section.dcr-0 ol li"):
            # number = articles.css('::attr(data-link-name)').get()
            # number = re.search(r'\d+', number).group()
            base_url = 'https://www.theguardian.com/'
            uri =  articles.css('a').attrib['href']
            url = f'{base_url}{uri}'
            
            yield scrapy.Request(url, callback=self.parse_article)
            
            # yield {
            #     'number': number,
            #     'title': articles.css('a span::text').get(),
            #     'url' : url,
            #     'article': ""
            # }
        
    def parse_article(self, response):
        title = response.css('div.dcr-0 h1::text').get()
        author = response.css('div.dcr-0 a::text').get()
        summary = response.css('div.dcr-1yi1cnj p::text').get()
        date = response.css('summary.dcr-1ybxn6r span::text').get()[:14]
        text = response.css('div.article-body-commercial-selector.article-body-viewer-selector.dcr-1r94quw p.dcr-94xsh ::text').getall()  # noqa: E501
        text = ' '.join(text).strip() 
        
        yield { 
               'title': title,
               'summary': summary,
               'author': author,
               'date_of_pub': date,
               'content' : text,
               }
        

# articles = response.css("section.dcr-0 ol li")
# title = articles.css('a span::text')
# uri = articles.css('a').attrib['href']
# response.css('div.dcr-0 a::text').get()