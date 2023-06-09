
import subprocess
from dotenv import dotenv_values
import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# dotenv_values('.env')
# mongodb_uri = os.getenv("MONGODB_URI")
# mongodb_db = os.getenv("MONGODB_DATABASE")

# def spider_crawl(spider_name):
#     command =f"scrapy crawl -s MONGODB_URI={mongodb_uri} -s MONGODB_DATABASE= {mongodb_db} {spider_name}"  # noqa: E501
    
#     try:
#         subprocess.Popen(command, shell=True)
#         return {"message": f"Spider '{spider_name}' executed successfully."}
#     except subprocess.CalledProcessError as e:
#         return {"message": f"Failed to execute spider '{spider_name}'. Error: {e}"}
    
    
def spider_crawl(spider_name):
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(spider_name)
    process.start()
