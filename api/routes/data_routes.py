
from fastapi import APIRouter, HTTPException, status
from ..controllers.data_control import get_media_data
from services.text_analysis.text_analysis import aggregate_content
from services.text_analysis.text_analysis import analyse_text

data_router = APIRouter()
    

@data_router.get("/data/{source}" ) 
async def get_data(source):
    """
    Route returns all the 10 articles for a given newspaper source depending 
    on the source passed as a parameter in the path.
    
    Four source options available: 
    "guardian", "independent", "latimes", and "smh".
    """
    try:
        return  await get_media_data(source)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@data_router.get("/data/aggregated_content/{source}" ) 
async def get_content(source):
    """ 
    Route returns a single aggregated text of the ten articles of the 
    newspaper source passed as a parameter in the path.
    
    """
    content = await aggregate_content(source)
    return content

@data_router.get("/data/article/" ) 
async def get_article_analysis(source, id):
    """ 
    Given a source (guardian, for example) and an _id, route returns the 
    results of a text analysis function.
    """
    result = await analyse_text(source, id)
    return result
 
