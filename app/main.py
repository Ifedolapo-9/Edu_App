from fastapi import FastAPI
from app.api.v1 import auth, course, user, enrollment
from app.core.config import settings


app = FastAPI(title="FastAPI EDU_APP")

app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(user.router, prefix=settings.API_V1_STR, tags=["users"])
app.include_router(course.router, prefix=settings.API_V1_STR, tags=["courses"])
app.include_router(enrollment.router, prefix=settings.API_V1_STR, tags=["enrollments"])


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI EDU_APP"}