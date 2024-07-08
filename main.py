from typing import Union

from fastapi import FastAPI
from crud import fabric_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Set up CORS
origins = [
    "http://localhost:8080",  # Add the origins (Vue.js app URL) from where requests are allowed
    "http://192.168.19.83:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fabric_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}