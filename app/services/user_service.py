from app.services.base_service import BaseService


class UserService(BaseService):
    def __init__(self, user_repository):
        self.user_repository = user_repository
        super().__init__(user_repository)
