from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware

from src.api.routes.authentication import authentication_router
from src.exceptions import InvalidCredentials

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="some-secret-key")
app.include_router(authentication_router)


# adding universal exception handlers
#
@app.exception_handler(InvalidCredentials)
def invalid_credentials_handler(request: Request, exc: InvalidCredentials):
    return JSONResponse(status_code=401, content={"detail": "Invalid credentials"})
