# Import Modules
import uvicorn
from fastapi import FastAPI, Form, Cookie, Request, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Web 3.0 Modules
import web3

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

###################################################################################################

@app.post("/auth")
async def auth(request: Request):
  message = request.headers.get("Message")
  address = request.headers.get("Address")
  signature = request.headers.get("Signature")
  
  # Check message/address/signature values
  if not message or not address or not signature:
    raise HTTPException(status_code=400, detail="Missing required headers")
  
  # Verify auth
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
  
@app.get("/", status_code=200)
@app.get("/about", status_code=200)
async def about():
    return {"message": "Hello, world!"}

###################################################################################################

if __name__ == '__main__':
    uvicorn.run(app,
                host='127.0.0.1',
                port=8080,
                reload=True
                )
