from fastapi import FastAPI
from app.routes import auth
from app.routes import user
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
from app.core.errors import error
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontend-freedive.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "code": 1502,
            "message": "Invalid or incomplete data",
            "errors": exc.errors()
        }
    )