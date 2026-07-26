from app.user.router import user_routes
from fastapi import FastAPI
from app.core.db import Base, engine
from app.tasks.router import task_routes
from app.utils.exceptions import register_error_handlers

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Register global HTTP and Validation exception handlers
register_error_handlers(app)

app.include_router(task_routes)
app.include_router(user_routes)


@app.get("/")
async def read_root():
    return {"message": "TaskFlow API is running"}
