import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()

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

if __name__ == "__main__":
    uvicorn.run(reload=True, app="main:app")
