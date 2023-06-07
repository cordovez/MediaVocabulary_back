from fastapi import APIRouter, Depends, Query, status
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from services.guardian_scraper.guardian_scraper.spiders.guardian_spider import GuardianSpider



spider_router = APIRouter()


def run_spider(source):
    settings = get_project_settings()
    settings.set('SPIDER_MODULES', 
                 ['services.guardian_scraper.guardian_scraper.spiders'])
    process = CrawlerProcess(get_project_settings())
    process.crawl(GuardianSpider)  
        
    process.start()
    

@spider_router.get("/run_spider/{source}" ) 
async def read_source(source: str):
    run_spider(source)
    return {'message': "Spider has been triggered"}
