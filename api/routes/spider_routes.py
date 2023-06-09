
from fastapi import APIRouter, BackgroundTasks
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from services.spider_subprocess import spider_crawl
from services.guardian_scraper.guardian_scraper.spiders import guardian_spider



spider_router = APIRouter()
    

@spider_router.get("/run_spider/{source}" ) 
async def read_source(source):
    # result = guardian_spider()
    # return result
    result =spider_crawl(source)
    return result
    
    # background_tasks.add_task(spider_crawl, source, message="some notification")  
    # return {"message": "Notification sent in the background"}

