from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware

from src.api.exception_registry import exception_registry
from src.api.routes.authentication import authentication_router
from src.exceptions import DomainException

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="some-secret-key")
app.include_router(authentication_router)


# adding universal exception handlers
#  Handling the global exception Here i handle all domain exceptions because all exceptions comes under domain execptions


@app.exception_handler(DomainException)
def domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR  # default status code = 500

    for exception_type, status in exception_registry.items():
        if isinstance(exc, exception_type):
            status_code = status
            break

    return JSONResponse(
        status_code=status_code,
        content={
            "sucess": False,
            "error": {"message": exc.message, "type": exc.__class__.__name__},
        },
    )
