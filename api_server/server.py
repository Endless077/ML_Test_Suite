# Import Modules
import uvicorn
from fastapi import FastAPI

# To Run: uvicorn server:app --host 127.0.0.1 --port 6969 --reload
# To Run: uvicorn server:app --host 127.0.0.1 --port 6969
app = FastAPI()

@app.get("/", status_code=200)
@app.get("/about", status_code=200)
async def about():
    return {"message": "Hello, world!"}

if __name__ == '__main__':
    uvicorn.run(app,
                host='127.0.0.1',
                port=6969,
                reload=True
                )
    