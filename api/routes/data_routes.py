
from fastapi import APIRouter, HTTPException, status
from ..controllers.data_control import get_media_data

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
   