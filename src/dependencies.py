from src.command.repositories.authentication import AuthenticationRepository
from src.command.services.authentication import AuthenticationService
from src.core.authentication import JWTHandler, PasswordHandler
from src.database import DBManager

db = DBManager()
auth_repo = AuthenticationRepository(db)

password_handler = PasswordHandler()
jwt_handler = JWTHandler()
auth_service = AuthenticationService(auth_repo, password_handler, jwt_handler)
