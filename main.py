import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.db import init_db

from api.routes.spider_routes import spider_router
from api.routes.data_routes import data_router
from api.routes.user_routes import users_router



app=FastAPI()
app.include_router(spider_router, tags=["spiders"])
app.include_router(data_router, tags=["data"])
app.include_router(users_router, tags=["users"])





origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(CORSMiddleware, 
                   allow_origins= origins, 
                   allow_credentials = True, 
                   allow_methods=["*"], 
                   allow_headers=["*"], )

@app.get("/", tags=["root"])
def root():
    return "Welcome to Media Vocabulary"

@app.on_event("startup")
async def connect():
    await init_db()

if __name__ == "__main__":
    uvicorn.run(reload=True, app="main:app")
    
  
