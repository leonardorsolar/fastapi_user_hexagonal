from src.domain.entities.user import User
from datetime import datetime
# executar:PYTHONPATH=. pytest -s
# executar:PYTHONPATH=. pytest -spytest --maxfail=1 --disable-warnings -v
# coverage report
# coverage run -m pytest
# coverage run -m pytest && coverage report && coverage html

# GIVEN um usuário com dados válidos
# WHEN ele for criado
# THEN ele deve ter nome, email, idade e um id gerado
def test_create_user_with_defaults():
    user = User(name="Leo", email="leo@example.com")
    print(repr(user))
    assert user.name == "Leo"
    assert user.email == "leo@example.com"
    assert user.user_id is not None
    assert user.created_at is not None
    assert user.updated_at is not None

def test_create_user_with_custom_id():
    custom_id = "123"
    user = User(user_id=custom_id, name="Ana", email="ana@example.com")
    assert user.user_id == custom_id

def test_valid_email():
    user = User(name="Maria", email="maria@example.com")
    assert user.is_valid_email() is True

def test_invalid_email():
    user = User(name="João", email="joaoexample.com")
    assert user.is_valid_email() is False

def test_create_user_auto_dates_are_recent():
    before = datetime.utcnow()
    user = User(name="Leo", email="leo@example.com")  # ← não passa datas
    after = datetime.utcnow()
    print(before, after)
    assert before <= user.created_at <= after
    assert before <= user.updated_at <= after
  