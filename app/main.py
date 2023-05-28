from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import numpy as np
import os
import plotly.express as px
from tempfile import NamedTemporaryFile
import shutil
from tqdm import tqdm
from schemas import NormalizationData


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=
    [
        "http://127.0.0.1:5173",
        "http://178.170.192.87:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.mount("/permanent", StaticFiles(directory="normalized/permanent"), name="permanent")


@app.post('/incidents')
def upload_incidents(table: UploadFile):
    with open('tmp/' + table.filename, "wb") as wf:
        shutil.copyfileobj(table.file, wf)
        table.file.close()
    read_file = pd.read_excel(str('tmp/' + table.filename))
    read_file.to_csv(r'csv/incidents.csv', index = None, header=True)
    os.remove('tmp/' + table.filename) 
    return table.filename


@app.post('/works')
def upload_works(table: UploadFile):
    with open('tmp/' + table.filename, "wb") as wf:
        shutil.copyfileobj(table.file, wf)
        table.file.close()
    read_file = pd.read_excel(str('tmp/' + table.filename))
    read_file.to_csv(r'csv/works.csv', index = None, header=True)
    os.remove('tmp/' + table.filename) 
    return table.filename


@app.post('/normalize')
def normalize(data: NormalizationData):
    normalized_data = pd.DataFrame()
    for incidents_name in data.incidents:
        current_data = pd.read_csv("csv/" + incidents_name)
        current_data = current_data.drop(['Дата и время завершения события во'], axis=1)
        current_data = current_data.drop(['Дата закрытия'], axis=1)
        current_data = current_data.drop(['Округ'], axis=1)
        current_data = current_data.drop(['Наименование'],axis=1)
        constant_features = current_data.columns[current_data.nunique() <= 1]
        current_data = current_data.drop(constant_features, axis=1)
        missing_percentage = current_data.isnull().mean()
        high_missing_features = missing_percentage[missing_percentage > 0.8].index
        current_data = current_data.drop(high_missing_features, axis=1)
        current_data = current_data.loc[current_data['Источник']!='ASUPR']
        current_data = current_data.loc[current_data['Источник']!='EDC']
        normalized_data = pd.concat([normalized_data, current_data], ignore_index=True)
    normalized_data = normalized_data.drop_duplicates(subset=["Адрес"], keep=False)
    print(normalized_data.info())
    normalized_data.to_csv('normalized/permanent/normalized_data.csv')
    return 'normalized_data.csv'


