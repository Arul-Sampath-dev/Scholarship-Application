from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse

from src.api.dependencies import AuthenticationDependency
from src.api.shemas.authentication import CreateUser, FromProvider, LoginSuccess
from src.command.commands.authentication import (
    CreateUserWithConfirm,
    LoginUser,
)
from src.command.commands.provider import Provider
from src.core.oauth2 import oauth
from src.exceptions import MissingTokenError

authentication_router = APIRouter(
    tags=["authentication"],
    prefix="/auth",
)


@authentication_router.post("/register", response_model=LoginSuccess)
def create_user(
    cmd: CreateUser, auth_service: AuthenticationDependency, response: Response
):

    token = auth_service.register(CreateUserWithConfirm(**cmd.model_dump()))
    response.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24,
        secure=False,
    )
    return LoginSuccess(message="User registered successfully")


@authentication_router.post("/login")
def login(cmd: LoginUser, auth_service: AuthenticationDependency, response: Response):
    token = auth_service.login(LoginUser(**cmd.model_dump()))
    response.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24,
        secure=False,
    )
    return LoginSuccess(message="Login successful")


@authentication_router.get("/login/google")
async def login_via_google(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
        access_type="offline",
    )


@authentication_router.get("/google/callback")
async def google_callback(request: Request, auth_service: AuthenticationDependency):
    token = await oauth.google.authorize_access_token(request)
    user = token["userinfo"]

    token = auth_service.login_via_oauth(
        FromProvider(
            username=user["name"], email=user["email"], provider=Provider.GOOGLE
        )
    )

    redirect = RedirectResponse(url="http://localhost:5173/dashboard", status_code=302)

    redirect.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24,
        secure=False,
    )
    print(redirect.headers.get("set-cookie"))

    return redirect


@authentication_router.get("/login/microsoft")
async def login_via_microsoft(request: Request):
    redirect_uri = request.url_for("microsoft_callback")
    return await oauth.microsoft.authorize_redirect(
        request,
        redirect_uri,
        access_type="offline",
    )


@authentication_router.get("/microsoft/callback")
async def microsoft_callback(
    request: Request, auth_service: AuthenticationDependency, response: Response
):
    token = await oauth.microsoft.authorize_access_token(request, claims_options={})
    user = token["userinfo"]
    token = auth_service.login_via_oauth(
        FromProvider(
            username=user["name"], email=user["email"], provider=Provider.MICROSOFT
        )
    )
    response.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24,
        secure=False,
    )
    return LoginSuccess(message="Login successful")


@authentication_router.get("/me")
async def user_context(request: Request, auth_service: AuthenticationDependency):
    token = request.cookies.get("access_token")
    if not token:
        raise MissingTokenError()
    return auth_service.get_user_by_token(token)
