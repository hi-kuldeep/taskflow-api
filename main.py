from fastapi import FastAPI
from app.core.db import Base, engine
from app.tasks.router import task_routes

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(task_routes)

@app.get("/")
async def read_root():
    return {"message": "TaskFlow API is running"}


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="[IP_ADDRESS]", port=8000)
