# Import Modules

# Set the log level to ERROR (hides warning messages).
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import uvicorn
from models import *
from services import *
from fastapi import FastAPI, Form, Cookie, Request, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Web 3.0 Modules
import web3

ADMIN_AUTH = "FastAPI-0x0000000000000001"

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

def is_authenticated(session_cookie: str):
    # Checks if the session cookie is present and has a valid value.
    return session_cookie == "authenticated"
  
def verify_auth(message: str, address: str, signature: str):
  # Verify the signature using the public key of the address.
  # This is a simplified example, in practice you should use a library like Web3.py to do this.
  # Return True if the signature is valid, False otherwise.
  return True

@app.post("/auth")
async def auth(request: Request):
  message = request.headers.get("Message")
  address = request.headers.get("Address")
  signature = request.headers.get("Signature")
  
  # Check message/address/signature values
  if not message or not address or not signature:
    raise HTTPException(status_code=400, detail="Missing required headers")
  
  if verify_auth(message, address, signature):
    # Setup Session cookie
    response = {"message": "Login successful. Session cookie set."}
    return response, 200, {"Set-Cookie": "session=authenticated"}
  else:
    raise HTTPException(status_code=401, detail="Invalid signature")

@app.get("/test", status_code=200)
async def test(session: str = Cookie(None)):
    if not is_authenticated(session):
        raise HTTPException(status_code=401, detail="Authentication required")
    return {"message": "Access granted to protected route"}

###################################################################################################

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
