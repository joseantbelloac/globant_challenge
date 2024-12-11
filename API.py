from typing import Optional,Dict
import pandas as pd
from fastapi import FastAPI, Query, Path, Body,File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from io import StringIO

############## BACKEND  API  ##############

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def message_test():
    return {"mensaje": "Hola Mundo"}

@app.post("/upload/jobs")
async def upload_csv_jobs(file: UploadFile = File(...)) -> Dict[str, str]:
    if not file.filename.endswith('.csv'):
        return {"error": "El archivo no es un CSV"}
    contents = await file.read()
    df = pd.read_csv(pd.compat.StringIO(contents.decode('utf-8')))
    return {"filename": file.filename}

@app.post("/upload/departments")
async def upload_csv_departments(file: UploadFile = File(...)) -> Dict[str, str]:
    if not file.filename.endswith('.csv'):
        return {"error": "El archivo no es un CSV"}
    contents = await file.read()
    decoded_data=contents.decode('utf-8')
    data_io = StringIO(decoded_data)
    df = pd.read_csv(data_io)
    print(df.head())
    return {"filename": file.filename}


@app.post("/upload/hired_employees")
async def upload_csv_hired_employees(file: UploadFile = File(...)) -> Dict[str, str]:
    if not file.filename.endswith('.csv'):
        return {"error": "El archivo no es un CSV"}
    contents = await file.read()
    decoded_data=contents.decode('utf-8')
    data_io = StringIO(decoded_data)
    df = pd.read_csv(data_io)
    print(df.head())
    return {"filename": file.filename}