
from fastapi import HTTPException, status

from models.media_models import TheGuardian
from models.media_models import Independent
from models.media_models import LATimes
from models.media_models import SMH

async def get_media_data(source):
    if source == "guardian":
        result =  await TheGuardian.find().to_list()
    elif source == "latimes":
        result =  await LATimes.find().to_list()
    elif source == "independent":
        result =  await Independent.find().to_list()
    elif source == "smh":
        result =  await SMH.find().to_list()
    else:
        result =  None

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return result