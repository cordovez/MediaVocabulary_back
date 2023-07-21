
from fastapi import APIRouter, BackgroundTasks
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from services.spider_subprocess import spider_crawl

from services.guardian_scraper.guardian_scraper.spiders.guardian_spider import GuardianSpider

spider_router = APIRouter()
    

@spider_router.get("/run_spider/{source}" ) 
def run_spider():
    process = CrawlerProcess(settings={
        "BOT_NAME": "guardian_scraper",
        "SPIDER_MODULES": ["guardian_scraper.spiders"],
        "NEWSPIDER_MODULE": "guardian_scraper.spiders",
        # Add any other Scrapy settings if necessary
    })

    process.crawl(GuardianSpider)  # Replace with the actual name of your spider
    process.start()
    return {"message": "Spider started successfully!"}

# async def read_source(source):
#     if source == 'guardian':
#         result =spider_crawl(guardian_spider)
#         return result
   