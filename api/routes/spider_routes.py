import subprocess
import os
from dotenv import load_dotenv

from fastapi import APIRouter
from models.media_models import NewsSource

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")

MEDIA = {
    "guardian": "guardian_scraper",
    "indo": "indo_scraper",
    "latimes": "lat_scraper",
    "smh": "smh_scraper",
}


spider_router = APIRouter()


@spider_router.get("/run_spider/")
def run_spider(source: NewsSource):
    """This route requires a source as a path parameter and it depends on the name of that source matching the name of the corresponding spider. The options are:

    - guardian
    - indo
    - latimes
    - smh

    """  # noqa: E501

    # scrapy requires that the "command" be called from within the directory
    # that contains the spider. This creates the absolute path to that directory.
    scraper_project_route = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "services", MEDIA[source])
    )

    # This navigates to the directory to the above path and calls the scrapycommand.
    os.chdir(scraper_project_route)
    command = f"scrapy crawl -s MONGODB_URI='{MONGODB_URI}' -s MONGODB_DATABASE='{MONGODB_DATABASE}' {source}"  # noqa: E501

    subprocess.run(command, shell=True)

    return {"message": "Spider execution initiated!"}
