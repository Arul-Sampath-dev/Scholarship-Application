from src.command.commands.personal import Create, Update
from src.command.repositories.personal import PersonalRepository


class PersonalService:
    def __init__(self, personal_repo: PersonalRepository):
        self.personal_repo = personal_repo

    def get_details(self, user_id: str):
        pass

    def register(self, cmd: Create):
        return self.personal_repo.create(cmd=cmd)

    def update(self, cmd: Update):
        return self.personal_repo.update(cmd=cmd)
