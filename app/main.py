from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, course, user, enrollment
from app.core.config import settings

app = FastAPI(title="FastAPI EDU_APP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(user.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(course.router, prefix=f"{settings.API_V1_STR}/courses", tags=["courses"])
app.include_router(enrollment.router, prefix=f"{settings.API_V1_STR}/enrollments", tags=["enrollments"])


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI EDU_APP"}

