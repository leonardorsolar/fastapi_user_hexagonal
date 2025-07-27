from abc import ABC, abstractmethod
from src.domain.entities.user import User

class IUserRepository(ABC):

    @abstractmethod
    async def create(self, user: User) -> User:
        """Cria um novo usuário"""
        pass