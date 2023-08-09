
from typing import Annotated


from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models.user_models import User

from ..authorization.auth import get_current_user

from ..controllers.data_control import get_media_data
from services.text_analysis.text_analysis import (analyse_text,
                                                  aggregate_content, analyse_aggregated_text)


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

data_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@data_router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")



@data_router.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@data_router.get("/data/{source}" ) 
async def get_articles(source):
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
async def get_aggregated_publication_content(source):
    """ 
    Route returns a single aggregated text of the ten articles of the 
    newspaper source passed as a parameter in the path.
    
    """
    content = await aggregate_content(source)
    return content

@data_router.get("/data/aggregated_analysis/{source}" ) 
async def get_aggregated_content_analysis(source):
    content = await aggregate_content(source)
    result = await analyse_aggregated_text(content)
    return result
    

@data_router.get("/data/article/{source}/{id}" ) 
async def get_article_analysis(source, id):
    """ 
    Given a source (guardian, for example) and an _id, route returns the 
    results of a text analysis function.
    """
    result = await analyse_text(source, id)
    return result
 
