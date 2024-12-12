from typing import Optional,Dict
import pandas as pd
from fastapi import FastAPI, Query, Path, Body,File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from io import StringIO
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os


   ############## BACKEND  API  ##############


app = FastAPI()


origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Cargar las variables de entorno desde el archivo .env

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)


def create_tables():

    queries = [

        """
        CREATE SCHEMA IF NOT EXISTS globant;
        """,
        """
        CREATE TABLE IF NOT EXISTS globant.hired_employees(
        id int not null,
        name varchar(200),
        datetime varchar(40),
        department_id int,
        job_id int
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS globant.departments(
        id int not null,
        department varchar(100)
        );

        """,

        """
        CREATE TABLE IF NOT EXISTS globant.jobs(
        id int not null,
        job varchar(100)
        );

        """
    ]

    session = Session()

    try:
        for query in queries:
            session.execute(query)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error creating tables: {e}")

    finally:
        session.close()

create_tables()

def load_data_in_batches(df, table_name, batch_size=500):
    for start in range(0, len(df), batch_size):
        end = start + batch_size
        batch = df[start:end]
        batch.to_sql(table_name, engine, if_exists='append', index=False)

@app.get("/")
def message_test():
    return {"mensaje": "Hola Mundo"}

@app.post("/upload/jobs")
async def upload_csv_jobs(file: UploadFile = File(...)) -> Dict[str, str]:
    if not file.filename.endswith('.csv'):
        return {"error": "El archivo no es un CSV"}
        
    contents = await file.read()
    decoded_data=contents.decode('utf-8')
    data_io=StringIO(decoded_data)
    df = pd.read_csv(data_io)
    load_data_in_batches(df, 'jobs')
    return {"filename": file.filename}


@app.post("/upload/departments")
async def upload_csv_departments(file: UploadFile = File(...)) -> Dict[str, str]:
    if not file.filename.endswith('.csv'):
        return {"error": "El archivo no es un CSV"}

    contents = await file.read()
    decoded_data=contents.decode('utf-8')
    data_io=StringIO(decoded_data)
    df = pd.read_csv(data_io)
    load_data_in_batches(df, 'departments')
    return {"filename": file.filename}

@app.post("/upload/hired_employees")
async def upload_csv_hired_employees(file: UploadFile = File(...)) -> Dict[str, str]:
    if not file.filename.endswith('.csv'):
        return {"error": "El archivo no es un CSV"}

    contents = await file.read()
    decoded_data=contents.decode('utf-8')
    data_io=StringIO(decoded_data)
    df = pd.read_csv(data_io)
    load_data_in_batches(df, 'hired_employees')
    return {"filename": file.filename}