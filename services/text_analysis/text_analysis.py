from fastapi import HTTPException, status
from models.media_models import Independent, LATimes, SMH, TheGuardian

async def  aggregate_content(source):
    if source == "guardian":
        content =  [doc.content for doc in await TheGuardian.find().to_list()]
    elif source == "latimes":
        content =  [doc.content for doc in await LATimes.find().to_list()]
    elif source == "independent":
        content =  [doc.content for doc in await Independent.find().to_list()]
    elif source == "smh":
        content =  [doc.content for doc in await SMH.find().to_list()]
    else:
        content =  None

    if not content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return content

    
    aggregated_content = " ".join(content)
    
    return aggregated_content