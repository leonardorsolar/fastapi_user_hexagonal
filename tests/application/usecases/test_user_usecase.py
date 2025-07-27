import pytest
from src.domain.entities.user import User
from src.application.usecases.user_usecase import UserUseCase

# executar:PYTHONPATH=. pytest -s
# executar:PYTHONPATH=. pytest -spytest --maxfail=1 --disable-warnings -v
# coverage report

class DummyRequest:
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age

@pytest.mark.asyncio
async def test_create_user_with_existing_email_should_raise_error():
    usecase = UserUseCase()

    # Simulando uma requisição
    request = DummyRequest("Leo", "leo@gmail.com", 30)

    with pytest.raises(ValueError, match="Email já está em uso"):
        await usecase.create_user(request)
