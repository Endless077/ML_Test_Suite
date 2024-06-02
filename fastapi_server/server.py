# Logging Setup
from utils.utils import Logger
LOG_FILE = "test_suite"
LOG_DIR = "../storage/logs"
LOG_SYS = Logger(LOG_FILE, LOG_DIR)

# TensorFlow/PyTorch Log Level Setup
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Server
from fastapi import FastAPI, HTTPException, Request, Response
import uvicorn

# Security and Client
from fastapi import Form, UploadFile
from fastapi.security import *
from fastapi.middleware.cors import CORSMiddleware

# Stuff
from models import *
from services import *

# Web 3.0
import web3

TAG = "FastAPI"
ADMIN_TOKEN = "FastAPI-0x0000000000000001"

###################################################################################################

# To Run: uvicorn server:app --host 127.0.0.1 --port 8080 --reload
# To Run: uvicorn server:app --host 127.0.0.1 --port 8080

app = FastAPI(title="FastAPI - ML Test Suite",
              description="A simple and fast api suite for a test suite for machine learning models.",
              summary="Some easy API for a ML Test Suite.",
              contact={
                "name": "Antonio Garofalo",
                "url": "https://github.com/Endless077",
                "email": "antonio.garofalo125@gmail.com"
                },
              terms_of_service="http://example.com/terms/",
              license_info={
                "identifier": "GNU",
                "name": "GNU General Public License v3",
                "url": "https://opensource.org/license/gpl-3-0/"
                },
              version="1.0"
              )

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

###################################################################################################

# Attack Routes
@app.post("/attack/evasion/{attack_type}", status_code=200)
async def evasion_attack(evasion_model: EvasionModel, attack_type: str):
  pass

@app.post("/attack/extraction/{attack_type}", status_code=200)
async def extraction_attack(extraction_model: ExtractionModel, attack_type: str):
  pass

@app.post("/attack/inference/{attack_type}", status_code=200)
async def inference_attack(inference_model: InferenceModel, attack_type: str):
  pass

@app.post("/attack/poisoning/{attack_type}", status_code=200)
async def poisoning_attack(poisoning_model: PoisoningModel, attack_type: str):
  pass

###################################################################################################

# Defense Routes
@app.post("/defense/detector/{defense_type}", status_code=200)
async def detector_defense(detector_model: DetectorModel, defense_type: str):
  pass

@app.post("/defense/postprocessor/{defense_type}", status_code=200)
async def postprocessor_defense(postprocessor_model: PostprocessorModel, defense_type: str):
  pass

@app.post("/defense/preprocessor/{defense_type}", status_code=200)
async def preprocessor_defense(preprocessor_model: PreprocessorModel, defense_type: str):
  pass

@app.post("/defense/trainer/{defense_type}", status_code=200)
async def trainer_defense(trainer_model: TrainerModel, defense_type: str):
  pass

@app.post("/defense/transformer/{defense_type}", status_code=200)
async def transformer_defense(transformer_model: TransformerModel, defense_type: str):
  pass


###################################################################################################

@app.get("/", status_code=200)
@app.get("/about", status_code=200)
async def about():
    return {"message": "Hello, world!"}

###################################################################################################

@app.post("/upload", status_code=201)
async def upload(model: UploadFile, filename: str = Form(...)):
  pass

###################################################################################################

if __name__ == '__main__':
    print(" ________               _        _       _______  _____  ")
    print("|_   __  |             / |_     / \     |_   __ \|_   _| ")
    print("  | |_ \_|,--.   .--. `| |-'   / _ \      | |__) | | |   ")
    print("  |  _|  `'_\ : ( (`\] | |    / ___ \     |  ___/  | |   ")
    print(" _| |_   // | |, `'.'. | |, _/ /   \ \_  _| |_    _| |_  ")
    print("|_____|  \'-;__/[\__) )\__/|____| |____||_____|  |_____| ")
    
    uvicorn.run(app, host='127.0.0.1', port=8080)
