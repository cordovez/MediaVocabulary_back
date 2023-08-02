import beanie
import motor
import motor.motor_asyncio

from dotenv import dotenv_values
from  models.media_models import TheGuardian, LATimes, Independent, SMH
from models.user_models import User_MongoDB

""" Beanie uses a single model to create database models and give responses, so
    models have to be imported into the client initialization.
"""

env = dotenv_values(".env")


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(env["MONGODB_URI"])
    await beanie.init_beanie(
        database=client.scrapy,
        document_models=[TheGuardian, LATimes, Independent, SMH, User_MongoDB],
        

    )
