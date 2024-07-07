from typing import Union

from fastapi import FastAPI
from crud import fabric_router

app = FastAPI()

app.include_router(fabric_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}