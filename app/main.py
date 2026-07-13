from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Daily Sales Tracker API is running"
    }