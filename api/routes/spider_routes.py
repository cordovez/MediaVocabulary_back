
import subprocess
import os
from dotenv import load_dotenv

from fastapi import APIRouter

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")

def get_path_to_project(spider):
    """ function takes in a spider name ("source") and it is matched to 
    its corresponding scrapy project directory"""
    if spider == 'guardian':
        project = 'guardian_scraper'
    elif spider == 'indo':
        project = 'indo_scraper'
    elif spider == 'latimes':
        project = 'lat_scraper'
    elif spider == 'smh':
        project = 'smh_scraper'
    else: 
        project = 'does_not_exist'
    
    return project
    
spider_router = APIRouter()

@spider_router.get("/run_spider/{source}" ) 
def run_spider(source):
    """ This route requires a source as a path parameter and it depends on the name of that source matching the name of the corresponding spider. The options are:

    - guardian
    - indo
    - latimes
    - smh

"""  # noqa: E501

    # scrapy requires that the "command" be called from within the directory 
    # that contains the spider. This creates the absolute path.
    scraper_project_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'services', get_path_to_project(source)))

    # This changes the directory to the above path and calls the command.
    os.chdir(scraper_project_route)
    command = f"scrapy crawl -s MONGODB_URI='{MONGODB_URI}' -s MONGODB_DATABASE='{MONGODB_DATABASE}' {source}"  # noqa: E501
    
    subprocess.run(command, shell=True)
    
    return {"message": "Spider execution initiated!"}
