
from fastapi import APIRouter
from ..controllers.data_controllers import get_guardian_data
from ..controllers.data_control import get_media_data

data_router = APIRouter()
    

@data_router.get("/data/{source}" ) 
async def get_data(source):
    """
    route returns all the data for a given media source depending on the source passed.
    
    four source options available: "guardian", "independent", "latimes", and "smh".
    """
    return  await get_media_data(source)
    # if source == "guardian":
    #     # return  await get_guardian_data()
    # else:
    #     return {"message": "that is not a valid resource"}