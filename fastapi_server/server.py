# Logging Analytics System
from logs.analytics.logger import get_logging
LOG_SYS = None

# Support Modules
import os
import sys
import shutil
import signal
import logging
import zipfile
import aiofiles
import warnings

from datetime import datetime as dt

# Warnings Log Level Setup
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('torch').setLevel(logging.ERROR)
logging.getLogger('tensorflow').setLevel(logging.ERROR)
warnings.filterwarnings('ignore', category=UserWarning, module='torch')
warnings.filterwarnings('ignore', category=UserWarning, module='tensorflow')

# Setup Tensorflow
import tensorflow as tf

# Disable Eager Execution
tf.compat.v1.disable_eager_execution()

###################################################################################################

# Local server storage
LOCAL_MODELS = {}
LOCAL_DATASET = {}
STORAGE_TEMP_DIR = "../storage/tmp"
STORAGE_MODEL_DIR = "../storage/model"
STORAGE_DATASET_DIR = "../storage/dataset"

# Server
from fastapi import FastAPI, HTTPException, Header, Request, Response, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import Form, Query, Depends, UploadFile
import uvicorn

# Security and Client
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
import secrets

# Stuff
from models import *
from services import *

###################################################################################################

# To Run: uvicorn server:app --host 127.0.0.1 --port 8080 --reload
# To Run: uvicorn server:app --host 127.0.0.1 --port 8080

TAG = "FastAPI"

ACCESS_TOKEN = secrets.token_hex(16)

app = FastAPI(title="FastAPI - ML Test Suite",
              summary="Some easy API for a ML Test Suite.",
              description="A simple and fast api suite for a test suite for machine learning models.",
              contact={
                  "email": "antonio.garofalo125@gmail.com",
                  "name": "Antonio Garofalo",
                  "url": "https://github.com/Endless077"
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
    "http://127.0.0.1",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def access_control(token: str):
    if token != ACCESS_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized Access",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True

###################################################################################################

TAG_ATTACK = ["Attacks"]

# Attack Routes
@app.post("/attack/evasion/{attack_type}", status_code=200, tags=TAG_ATTACK,
          summary="Evasion attack perform route.",
          description="Route for start an evasion attack to personal model and dataset.")
async def evasion_attack(request: Request, evasion_model: EvasionModel, attack_type: str) -> JSONResponse:
    try:
        LOG_SYS.write(TAG, f"Execution of an evasion attack:")
        LOG_SYS.write(TAG, f"-- User Agent: {request.headers.get('user-agent')}.")
        LOG_SYS.write(TAG, f"-- Connected with client (ip): {request.client.host}.")
        LOG_SYS.write(TAG, f"Performing evasion attack of type: {attack_type} with dataset: {evasion_model.dataset_type}.")
        result = await perform_attack_service(evasion_model, attack_type)

        LOG_SYS.write(TAG, "Building headers.")
        headers = {
            "Content-Type": "application/json",
            "Attack-Category": "Evasion",
            "Attack-Type": attack_type,
            "Dataset-Type": evasion_model.dataset_type
        }

        LOG_SYS.write(TAG, "Building JSONResponse.")
        return JSONResponse(content=result, headers=headers, status_code=200, media_type="application/json")
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP occurred with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/attack/extraction/{attack_type}", status_code=200, tags=TAG_ATTACK,
          summary="Extraction attack perform route.",
          description="Route for start an extraction attack to personal model and dataset.")
async def extraction_attack(request: Request, extraction_model: ExtractionModel, attack_type: str) -> JSONResponse:
    try:
        LOG_SYS.write(TAG, f"Execution of an extraction attack:")
        LOG_SYS.write(TAG, f"-- User Agent: {request.headers.get('user-agent')}.")
        LOG_SYS.write(TAG, f"-- Connected with client (ip): {request.client.host}.")
        LOG_SYS.write(TAG, f"Performing extraction attack of type: {attack_type} with dataset: {extraction_model.dataset_type}.")
        result = await perform_attack_service(extraction_model, attack_type)

        LOG_SYS.write(TAG, "Building headers.")
        headers = {
            "Content-Type": "application/json",
            "Attack-Category": "Extraction",
            "Attack-Type": attack_type,
            "Dataset-Type": extraction_model.dataset_type
        }

        LOG_SYS.write(TAG, "Building JSONResponse.")
        return JSONResponse(content=result, headers=headers, status_code=200, media_type="application/json")
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP occurred with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/attack/inference/{attack_type}", status_code=200, tags=TAG_ATTACK,
          summary="Inference attack perform route.",
          description="Route for start an inference attack to personal model and dataset.")
async def inference_attack(request: Request, inference_model: InferenceModel, attack_type: str) -> JSONResponse:
    try:
        LOG_SYS.write(TAG, f"Execution of an inference attack:")
        LOG_SYS.write(TAG, f"-- User Agent: {request.headers.get('user-agent')}.")
        LOG_SYS.write(TAG, f"-- Connected with client (ip): {request.client.host}.")
        LOG_SYS.write(TAG, f"Performing inference attack of type: {attack_type} with dataset: {inference_model.dataset_type}.")
        result = await perform_attack_service(inference_model, attack_type)

        LOG_SYS.write(TAG, "Building headers.")
        headers = {
            "Content-Type": "application/json",
            "Attack-Category": "Inference",
            "Attack-Type": attack_type,
            "Dataset-Type": inference_model.dataset_type
        }

        LOG_SYS.write(TAG, "Building JSONResponse.")
        return JSONResponse(content=result, headers=headers, status_code=200, media_type="application/json")
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP occurred with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/attack/poisoning/{attack_type}", status_code=200, tags=TAG_ATTACK,
          summary="Poisoning attack perform route.",
          description="Route for start a poisoning attack to personal model and dataset.")
async def poisoning_attack(request: Request, poisoning_model: PoisoningModel, attack_type: str) -> JSONResponse:
    try:
        LOG_SYS.write(TAG, f"Execution of a poisoning attack:")
        LOG_SYS.write(TAG, f"-- User Agent: {request.headers.get('user-agent')}.")
        LOG_SYS.write(TAG, f"-- Connected with client (ip): {request.client.host}.")
        LOG_SYS.write(TAG, f"Performing poisoning attack of type: {attack_type} with dataset: {poisoning_model.dataset_type}.")
        result = await perform_attack_service(poisoning_model, attack_type)

        LOG_SYS.write(TAG, "Building headers.")
        headers = {
            "Content-Type": "application/json",
            "Attack-Category": "Poisoning",
            "Attack-Type": attack_type,
            "Dataset-Type": poisoning_model.dataset_type
        }

        LOG_SYS.write(TAG, "Building JSONResponse.")
        return JSONResponse(content=result, headers=headers, status_code=200, media_type="application/json")
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP occurred with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

###################################################################################################

TAG_DEFENSE = ["Defenses"]

# Defense Routes
@app.post("/defense/detector/{defense_type}", status_code=200, tags=TAG_DEFENSE,
          summary="Detector defense perform route.",
          description="Route for start a detector defense to personal model and dataset.")
async def detector_defense(request: Request, detector_model: DetectorModel, defense_type: str) -> JSONResponse:
    try:
        LOG_SYS.write(TAG, f"Execution of a detector defence:")
        LOG_SYS.write(TAG, f"-- User Agent: {request.headers.get('user-agent')}.")
        LOG_SYS.write(TAG, f"-- Connected with client (ip): {request.client.host}.")
        LOG_SYS.write(TAG, f"Performing detector defense of type: {defense_type} with dataset: {detector_model.dataset_type}.")
        result = await perform_defense_service(detector_model, defense_type)

        LOG_SYS.write(TAG, "Building headers.")
        headers = {
            "Content-Type": "application/json",
            "Defense-Category": "Detector",
            "Defense-Type": defense_type,
            "Dataset-Type": detector_model.dataset_type
        }

        LOG_SYS.write(TAG, "Building JSONResponse.")
        return JSONResponse(content=result, headers=headers, status_code=200, media_type="application/json")
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/defense/postprocessor/{defense_type}", status_code=200, tags=TAG_DEFENSE,
          summary="Postprocessor defense perform route.",
          description="Route for start a postprocessor defense to personal model and dataset.")
async def postprocessor_defense(request: Request, postprocessor_model: PostprocessorModel, defense_type: str) -> JSONResponse:
    try:
        LOG_SYS.write(TAG, f"Execution of a postprocessor defence:")
        LOG_SYS.write(TAG, f"-- User Agent: {request.headers.get('user-agent')}.")
        LOG_SYS.write(TAG, f"-- Connected with client (ip): {request.client.host}.")
        LOG_SYS.write(TAG, f"Performing postprocessor defense of type: {defense_type} with dataset: {postprocessor_model.dataset_type}.")
        result = await perform_defense_service(postprocessor_model, defense_type)

        LOG_SYS.write(TAG, "Building headers.")
        headers = {
            "Content-Type": "application/json",
            "Defense-Category": "Postprocessor",
            "Defense-Type": defense_type,
            "Dataset-Type": postprocessor_model.dataset_type
        }

        LOG_SYS.write(TAG, "Building JSONResponse.")
        return JSONResponse(content=result, headers=headers, status_code=200, media_type="application/json")
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/defense/preprocessor/{defense_type}", status_code=200, tags=TAG_DEFENSE,
          summary="Preprocessor defense perform route.",
          description="Route for start a preprocessor defense to personal model and dataset.")
async def preprocessor_defense(request: Request, preprocessor_model: PreprocessorModel, defense_type: str) -> JSONResponse:
    try:
        LOG_SYS.write(TAG, f"Execution of a preprocessor defence:")
        LOG_SYS.write(TAG, f"-- User Agent: {request.headers.get('user-agent')}.")
        LOG_SYS.write(TAG, f"-- Connected with client (ip): {request.client.host}.")
        LOG_SYS.write(TAG, f"Performing preprocessor defense of type: {defense_type} with dataset: {preprocessor_model.dataset_type}.")
        result = await perform_defense_service(preprocessor_model, defense_type)

        LOG_SYS.write(TAG, "Building headers.")
        headers = {
            "Content-Type": "application/json",
            "Defense-Category": "Preprocessor",
            "Defense-Type": defense_type,
            "Dataset-Type": preprocessor_model.dataset_type
        }

        LOG_SYS.write(TAG, "Building JSONResponse.")
        return JSONResponse(content=result, headers=headers, status_code=200, media_type="application/json")
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/defense/trainer/{defense_type}", status_code=200, tags=TAG_DEFENSE,
          summary="Trainer defense perform route.",
          description="Route for start a trainer defense to personal model and dataset.")
async def trainer_defense(request: Request, trainer_model: TrainerModel, defense_type: str) -> JSONResponse:
    try:
        LOG_SYS.write(TAG, f"Execution of a trainer defence:")
        LOG_SYS.write(TAG, f"-- User Agent: {request.headers.get('user-agent')}.")
        LOG_SYS.write(TAG, f"-- Connected with client (ip): {request.client.host}.")
        LOG_SYS.write(TAG, f"Performing trainer defense of type: {defense_type} with dataset: {trainer_model.dataset_type}.")
        result = await perform_defense_service(trainer_model, defense_type)

        LOG_SYS.write(TAG, "Building headers.")
        headers = {
            "Content-Type": "application/json",
            "Defense-Category": "Trainer",
            "Defense-Type": defense_type,
            "Dataset-Type": trainer_model.dataset_type
        }

        LOG_SYS.write(TAG, "Building JSONResponse.")
        return JSONResponse(content=result, headers=headers, status_code=200, media_type="application/json")
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/defense/transformer/{defense_type}", status_code=200, tags=TAG_DEFENSE,
          summary="Transformer defense perform route.",
          description="Route for start a transformer defense to personal model and dataset.")
async def transformer_defense(request: Request, transformer_model: TransformerModel, defense_type: str) -> JSONResponse:
    try:
        LOG_SYS.write(TAG, f"Execution of a transformer defence:")
        LOG_SYS.write(TAG, f"-- User Agent: {request.headers.get('user-agent')}.")
        LOG_SYS.write(TAG, f"-- Connected with client (ip): {request.client.host}.")
        LOG_SYS.write(TAG, f"Performing transformer defense of type: {defense_type} with dataset: {transformer_model.dataset_type}.")
        result = await perform_defense_service(transformer_model, defense_type)

        LOG_SYS.write(TAG, "Building headers.")
        headers = {
            "Content-Type": "application/json",
            "Defense-Category": "Transformer",
            "Defense-Type": defense_type,
            "Dataset-Type": transformer_model.dataset_type
        }

        LOG_SYS.write(TAG, "Building JSONResponse.")
        return JSONResponse(content=result, headers=headers, status_code=200, media_type="application/json")
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

###################################################################################################

@app.post("/upload/model", status_code=201, tags=["Upload"],
          summary="Upload a model",
          description="Upload a .h5 or Keras saveModel file.")
async def upload(request: Request, model: UploadFile, filename: str = Form(...)) -> JSONResponse:
    try:
        LOG_SYS.write(TAG, f"Execution of an model update:")
        LOG_SYS.write(TAG, f"-- User Agent: {request.headers.get('user-agent')}.")
        LOG_SYS.write(TAG, f"-- Connected with client (ip): {request.client.host}.")
        
        # Create the folder if it doesn't exist
        if not os.path.exists(STORAGE_MODEL_DIR):
            os.makedirs(STORAGE_MODEL_DIR)

        # Complete path to save the file
        saved_filename = f"{filename.replace(' ', '_')}-{dt.now().isoformat().replace(':', '-')}.h5"

        file_path = os.path.join(STORAGE_MODEL_DIR, saved_filename)

        # Saving the file using aiofiles
        LOG_SYS.write(TAG, f"Saving file model in server storage.")
        async with aiofiles.open(file_path, "wb") as out_file:
            # Read the uploaded file as bytes
            model_file = await model.read()

            # Asynchronously write the bytes to the file
            await out_file.write(model_file)

        # Save model in the local storage
        global LOCAL_MODELS
        LOCAL_MODELS[filename] = (load_model_service(saved_filename), saved_filename)
                
        LOG_SYS.write(TAG, f"Model file upload complete.")
        return JSONResponse(content={"message": "File uploaded successfully."}, status_code=201, media_type="application/json")
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected upload model error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload/dataset", status_code=201, tags=["Upload"],
          summary="Upload a dataset",
          description="Upload a dataset compressed file (ZIP) containing the directory.")
async def upload(request: Request, zipfile: UploadFile, directoryname: str = Form(...)) -> JSONResponse:
    try:
        LOG_SYS.write(TAG, f"Execution of a dataset update:")
        LOG_SYS.write(TAG, f"-- User Agent: {request.headers.get('user-agent')}.")
        LOG_SYS.write(TAG, f"-- Connected with client (ip): {request.client.host}.")
        LOG_SYS.write(TAG, f"Saving dataset directory struct in server storage.")
        
        # Create the uploaded file to a temporary location
        os.makedirs(STORAGE_TEMP_DIR, exist_ok=True)
        file_path = os.path.join(STORAGE_TEMP_DIR, zipfile.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(zipfile.file, buffer)

        # Extract the directory contents from the uploaded zip file
        extract_zip_contents(file_path, directoryname.replace(' ', '_'))
        
        LOG_SYS.write(TAG, f"Dataset directory struct upload complete.")
        return JSONResponse(content={"message": "Directory uploaded successfully."}, status_code=201, media_type="application/json")
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected directory error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def extract_zip_contents(zip_path: str, directoryname: str):
    # Create target directory path
    target_directory = os.path.join(STORAGE_DATASET_DIR, directoryname)
    os.makedirs(target_directory, exist_ok=True)

    # Open ZIP file and extract all
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(target_directory)

    # Find paths of 'train' and 'test' directories
    train_dir = None
    test_dir = None

    for root, dirs, files in os.walk(target_directory):
        if 'train' in dirs:
            train_dir = os.path.join(root, 'train')
        if 'test' in dirs:
            test_dir = os.path.join(root, 'test')

        # Break the loop if both 'train' and 'test' directories are found
        if train_dir and test_dir:
            break

    # Determine the dataset directory path
    if train_dir and test_dir:
        dataset_dir = os.path.dirname(train_dir)
    else:
        raise FileNotFoundError("No train or test directory found.")
    
    # Save the dataset directory path
    global LOCAL_DATASET
    LOCAL_DATASET[directoryname] = dataset_dir
    
    os.remove(zip_path)

###################################################################################################

@app.get("/", status_code=200, tags=["About"],
         summary="",
         description="About Route.")
@app.get("/about", status_code=200, tags=["About"],
         summary="",
         description="About Route.")
async def about():
    return RedirectResponse(url="/docs")
    
###################################################################################################

STARTUP_TAG = "STARTUP"
SHUTDOWN_TAG = "SHUTDOWN"


def startup():
    # Logging System Init
    global LOG_SYS
    LOG_SYS = get_logging()
    
    # Startup Message
    LOG_SYS.write(STARTUP_TAG, " ________               _        _       _______  _____  ")
    LOG_SYS.write(STARTUP_TAG, "|_   __  |             / |_     / \     |_   __ \|_   _| ")
    LOG_SYS.write(STARTUP_TAG, "  | |_ \_|,--.   .--. `| |-'   / _ \      | |__) | | |   ")
    LOG_SYS.write(STARTUP_TAG, "  |  _|  `'_\ : ( (`\] | |    / ___ \     |  ___/  | |   ")
    LOG_SYS.write(STARTUP_TAG, " _| |_   // | |, `'.'. | |, _/ /   \ \_  _| |_    _| |_  ")
    LOG_SYS.write(STARTUP_TAG, "|_____|  \'-;__/[\__) )\__/|____| |____||_____|  |_____| ")

    LOG_SYS.write(STARTUP_TAG, "**************************************************")
    LOG_SYS.write(STARTUP_TAG, f"ACCESS TOKEN: {ACCESS_TOKEN}")
    LOG_SYS.write(STARTUP_TAG, "**************************************************")


def shutdown(signum, frame):
    try:
        LOG_SYS.write(SHUTDOWN_TAG, "Shutdown FastAPI server.")
        sys.exit(0)
    except Exception as e:
        LOG_SYS.write(SHUTDOWN_TAG, f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == '__main__':
    # Call Signal Registration
    signal.signal(signal.SIGINT, shutdown)   # Ctrl+C
    signal.signal(signal.SIGTERM, shutdown)  # kill
    signal.signal(signal.SIGHUP, shutdown)   # Terminal closed
    signal.signal(signal.SIGQUIT, shutdown)  # Quit signal
    signal.signal(signal.SIGABRT, shutdown)  # Abort signal
    signal.signal(signal.SIGUSR1, shutdown)  # User-defined signal 1
    signal.signal(signal.SIGUSR2, shutdown)  # User-defined signal 2

    # Startup
    startup()

    # Debug Mode
    #uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

    # Start Uvicorn App
    uvicorn.run(app, host="127.0.0.1", port=8000)

###################################################################################################
