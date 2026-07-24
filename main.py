from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "TaskFlow API is running"}


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="[IP_ADDRESS]", port=8000)
