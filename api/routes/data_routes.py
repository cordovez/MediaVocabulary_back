
from fastapi import APIRouter, HTTPException, status
from ..controllers.data_control import get_media_data
from services.text_analysis.text_analysis import aggregate_content
from services.text_analysis.text_analysis import analyse_text

data_router = APIRouter()
    

@data_router.get("/data/{source}" ) 
async def get_data(source):
    """
    Route returns all the data for a given media source depending 
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
    content = await aggregate_content(source)
    return content

@data_router.get("/data/article/" ) 
async def get_article_analysis(source, id):
    result = await analyse_text(source, id)
    return result
 
