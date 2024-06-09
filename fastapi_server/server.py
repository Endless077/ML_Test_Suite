# Logging
from logs.analytics.logger import get_logger
LOG_SYS = get_logger()

# TensorFlow/PyTorch Log Level
import os
import sys
import aiofiles
from datetime import datetime as dt
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

###################################################################################################

# Server
from fastapi import FastAPI, HTTPException, Header, Request, Response
from fastapi.responses import JSONResponse
from fastapi import Form, UploadFile
import uvicorn

# Security and Client
from fastapi.security import *
from fastapi.middleware.cors import CORSMiddleware

# Stuff
from models import *
from services import *

# Web 3.0
import web3

###################################################################################################

# To Run: uvicorn server:app --host 127.0.0.1 --port 8080 --reload
# To Run: uvicorn server:app --host 127.0.0.1 --port 8080

TAG = "FastAPI"

app = FastAPI(title="FastAPI - ML Test Suite",
              description="A simple and fast api suite for a test suite for machine learning models.",
              summary="Some easy API for a ML Test Suite.",
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
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

###################################################################################################

TAG_ATTACK = ["Attacks"]

# Attack Routes
@app.post("/attack/evasion/{attack_type}", status_code=200, tags=TAG_ATTACK, descritpion="Evasion attack perform route.")
async def evasion_attack(evasion_model: EvasionModel, attack_type: str) -> JSONResponse:
  try:
      LOG_SYS.write(TAG, f"Performing evasion attack of type: {attack_type} with dataset: {evasion_model.dataset_type}.")
      result = perform_attack(evasion_model, attack_type)
      
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

@app.post("/attack/extraction/{attack_type}", status_code=200, tags=TAG_ATTACK, descritpion="Extraction attack perform route.")
async def extraction_attack(extraction_model: ExtractionModel, attack_type: str) -> JSONResponse:
  try:
      LOG_SYS.write(TAG, f"Performing extraction attack of type: {attack_type} with dataset: {extraction_model.dataset_type}.")
      result = perform_attack(extraction_model, attack_type)
      
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

@app.post("/attack/inference/{attack_type}", status_code=200, tags=TAG_ATTACK, descritpion="Inference attack perform route.")
async def inference_attack(inference_model: InferenceModel, attack_type: str) -> JSONResponse:
  try:
      LOG_SYS.write(TAG, f"Performing inference attack of type: {attack_type} with dataset: {inference_model.dataset_type}.")
      result = perform_attack(inference_model, attack_type)
      
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

@app.post("/attack/poisoning/{attack_type}", status_code=200, tags=TAG_ATTACK, descritpion="Poisoning attack perform route.")
async def poisoning_attack(poisoning_model: PoisoningModel, attack_type: str) -> JSONResponse:
  try:
      LOG_SYS.write(TAG, f"Performing poisoning attack of type: {attack_type} with dataset: {poisoning_model.dataset_type}.")
      result = perform_attack(poisoning_model, attack_type)
      
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
@app.post("/defense/detector/{defense_type}", status_code=200, tags=TAG_DEFENSE, description="Detector defense perform route.")
async def detector_defense(detector_model: DetectorModel, defense_type: str) -> JSONResponse:
    try:
        LOG_SYS.write(TAG, f"Performing detector defense of type: {defense_type} with dataset: {detector_model.dataset_type}.")
        result = perform_defense(detector_model, defense_type)

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


@app.post("/defense/postprocessor/{defense_type}", status_code=200, tags=TAG_DEFENSE, description="Postprocessor defense perform route.")
async def postprocessor_defense(postprocessor_model: PostprocessorModel, defense_type: str) -> JSONResponse:
    try:
        LOG_SYS.write(TAG, f"Performing postprocessor defense of type: {defense_type} with dataset: {postprocessor_model.dataset_type}.")
        result = perform_defense(postprocessor_model, defense_type)

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


@app.post("/defense/preprocessor/{defense_type}", status_code=200, tags=TAG_DEFENSE, description="Preprocessor defense perform route.")
async def preprocessor_defense(preprocessor_model: PreprocessorModel, defense_type: str) -> JSONResponse:
    try:
        LOG_SYS.write(TAG, f"Performing preprocessor defense of type: {defense_type} with dataset: {preprocessor_model.dataset_type}.")
        result = perform_defense(preprocessor_model, defense_type)

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


@app.post("/defense/trainer/{defense_type}", status_code=200, tags=TAG_DEFENSE, description="Trainer defense perform route.")
async def trainer_defense(trainer_model: TrainerModel, defense_type: str) -> JSONResponse:
    try:
        LOG_SYS.write(TAG, f"Performing trainer defense of type: {defense_type} with dataset: {trainer_model.dataset_type}.")
        result = perform_defense(trainer_model, defense_type)

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


@app.post("/defense/transformer/{defense_type}", status_code=200, tags=TAG_DEFENSE, description="Transformer defense perform route.")
async def transformer_defense(transformer_model: TransformerModel, defense_type: str) -> JSONResponse:
    try:
        LOG_SYS.write(TAG, f"Performing transformer defense of type: {defense_type} with dataset: {transformer_model.dataset_type}.")
        result = perform_defense(transformer_model, defense_type)

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

@app.get("/", status_code=200, tags=["About"], description="About Route.")
@app.get("/about", status_code=200, tags=["About"], description="About Route.")
async def about():
    return {"app": "ML Test Suite"}

###################################################################################################

LOCAL_MODELS = {}
STORAGE_DIR = "../storage/models"

@app.post("/upload/model", status_code=201, tags=["Upload"], description="A simple model file upload route.")
async def upload(model: UploadFile, filename: str = Form(...), alreadyCompiled: bool = Form(...)) -> JSONResponse:
    # Create the folder if it doesn't exist
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)
        
    # Complete path to save the file
    file_path = os.path.join(STORAGE_DIR, f"{filename}-{dt.now().isoformat().replace(':', '-')}.h5")

    # Saving the file using aiofiles
    async with aiofiles.open(file_path, "wb") as out_file:
        # Read the uploaded file as bytes
        model_file = await model.read()

        # Asynchronously write the bytes to the file
        await out_file.write(model_file)
    
    return JSONResponse(content={"message": "File uploaded successfully."}, status_code=201, media_type="application/json")

@app.post("/upload/directory", status_code=201, tags=["Upload"], description="A simple directory of files upload route.")
async def upload(directory: UploadFile, directoryname: str = Form(...), alreadyCompiled: bool = Form(...)) -> JSONResponse:
    pass
        
###################################################################################################

if __name__ == '__main__':
    LOG_SYS.write(TAG, " ________               _        _       _______  _____  ")
    LOG_SYS.write(TAG, "|_   __  |             / |_     / \     |_   __ \|_   _| ")
    LOG_SYS.write(TAG, "  | |_ \_|,--.   .--. `| |-'   / _ \      | |__) | | |   ")
    LOG_SYS.write(TAG, "  |  _|  `'_\ : ( (`\] | |    / ___ \     |  ___/  | |   ")
    LOG_SYS.write(TAG, " _| |_   // | |, `'.'. | |, _/ /   \ \_  _| |_    _| |_  ")
    LOG_SYS.write(TAG, "|_____|  \'-;__/[\__) )\__/|____| |____||_____|  |_____| ")
    
    # Debug Mode
    #uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
    
    # Standard Mode
    uvicorn.run(app, host="127.0.0.1", port=8000)
