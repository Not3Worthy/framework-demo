from fastapi import FastAPI

app = FastAPI(title="FastAPI Microservice")

@app.get("/")
def read_root():
    return {"message": "Hello this is a demo endpoint, you made it!"}