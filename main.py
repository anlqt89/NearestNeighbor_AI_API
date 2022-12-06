from typing import Union
from __init__ import run_ai
from fastapi import FastAPI, UploadFile, File
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import shutil
import pandas as pd
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/ai/{filename}")
def read_item(filename: str, q: Union[str, None] = None):
    # return run_ai(filename)
    return "as"

@app.post("/uploadfile")
async def create_upload_file( file: UploadFile = File(...),  q: Union[str, None] = None):
    with open(f'{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename}