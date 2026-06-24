from authlib.integrations.starlette_client import OAuth

from src.settings import settings

oauth = OAuth()

oauth.register(
    name="google",
    client_id=settings.google.client_id,
    client_secret=settings.google.client_secret,
    server_metadata_url=settings.google.server_metadata_url,
    client_kwargs={"scope": "openid email profile"},
)

# oauth.register(
#     name="github",
#     client_id=settings.github.client_id,
#     client_secret=settings.github.client_secret,
#     access_token_url=settings.github.access_token_url,
#     authorize_url=settings.github.authorize_url,
#     api_base_url=settings.github.api_base_url,
#     client_kwargs={"scope": "user:email"},
# )

oauth.register(
    name="microsoft",
    client_id=settings.microsoft.client_id,
    client_secret=settings.microsoft.client_secret,
    server_metadata_url=settings.microsoft.server_metadata_url,
    client_kwargs={"scope": "openid profile User.Read"},
)
