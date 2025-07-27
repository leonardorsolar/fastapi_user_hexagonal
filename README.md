                # Tutorial FastAPI - Arquitetura Hexagonal com SOLID e Design Patterns

## Sumário

1. [Introdução](#introdução)
2. [Pré-requisitos e Instalação](#pré-requisitos-e-instalação)
3. [Estrutura do Projeto](#estrutura-do-projeto)
4. [Conceitos Aplicados](#conceitos-aplicados)
5. [Implementação](#implementação)
6. [Execução](#execução)

## Introdução

Este tutorial demonstra como criar uma API REST com FastAPI seguindo os princípios SOLID, padrões de design, injeção de dependência e arquitetura hexagonal. Vamos construir um sistema de gerenciamento de usuários completo **sem o uso de decorators nas camadas de domínio e aplicação**, mantendo essas camadas totalmente desacopladas de tecnologias específicas.

### Conceitos Abordados

-   **Arquitetura Hexagonal (Ports & Adapters)**
-   **Princípios SOLID**
-   **Injeção e Inversão de Dependências**
-   **Design Patterns**: Repository, Factory, Strategy, Observer
-   **Clean Architecture**
-   **Domain-Driven Design (DDD)**
-   **Desacoplamento tecnológico** nas camadas internas

## Pré-requisitos e Instalação

### 1. Instalação do Python

#### Windows:

```bash
# Baixar Python 3.11+ do site oficial: https://www.python.org/downloads/
# Durante a instalação, marcar "Add Python to PATH"

# Verificar instalação
python --version
pip --version
```

#### Linux (Ubuntu/Debian):

```bash
# Atualizar repositórios
sudo apt update

# Instalar Python 3.11+
sudo apt install python3.11 python3.11-pip python3.11-venv

# Verificar instalação
python3.11 --version
pip3.11 --version
```

#### macOS:

```bash
# Usando Homebrew
brew install python@3.11

# Ou baixar do site oficial
# Verificar instalação
python3 --version
pip3 --version
```

### 2. Configuração do Ambiente Virtual

```bash
# Criar diretório do projeto
mkdir fastapi-hexagonal-tutorial
cd fastapi-hexagonal-tutorial

# Criar ambiente virtual
python -m venv venv
ou
python3 -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Atualizar pip
python -m pip install --upgrade pip
```

### 3. Instalação das Dependências

crie o arquivo requirements.txt e adicione o conteúdo a seguir:

**requirements.txt**

```txt
# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Validação e Serialização
pydantic==2.5.0
pydantic-settings==2.1.0
email-validator==2.1.0

# Banco de Dados
aiosqlite==0.19.0

# Utilitários
python-multipart==0.0.6

# Desenvolvimento e Testes (opcional)
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
```

```bash
# Instalar dependências
pip install -r requirements.txt
```

### 4. Criando `.gitignore`:

-   Crie o arquivo `.gitignore` e inclua o seguinte conteudo:

```text
__pycache__/
*.pyc
*.pyo
venv/
.env/
```

### 5. Configuração do FastAPI

O FastAPI é um framework web moderno e rápido para construir APIs com Python. Principais características:

-   **Alto desempenho**: Baseado em Starlette e Pydantic
-   **Fácil de usar**: Sintaxe intuitiva com type hints
-   **Documentação automática**: Swagger UI e ReDoc integrados
-   **Validação automática**: Baseada em type hints
-   **Async/await nativo**: Suporte completo para programação assíncrona

## Estrutura do Projeto

```
src/
├── domain/
│   ├── entities/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── user_repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py
│   └── __init__.py
├── application/
│   ├── usecases/
│   │   ├── __init__.py
│   │   └── user_usecase.py
│   ├── dtos/
│   │   ├── __init__.py
│   │   └── user_dto.py
│   └── __init__.py
├── infrastructure/
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   └── models.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── sqlite_user_repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── email_service.py
│   └── __init__.py
├── presentation/
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── user_controller.py
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── container.py
│   └── __init__.py
├── config/
│   ├── __init__.py
│   └── settings.py
└── main.py
```

## Conceitos Aplicados

### 1. Arquitetura Hexagonal

A arquitetura hexagonal separa o código em três camadas:

-   **Domain**: Regras de negócio e entidades
-   **Application**: Casos de uso e orquestração
-   **Infrastructure**: Detalhes técnicos (banco, APIs externas)
-   **Presentation**: Interface (controladores, rotas)

### 2. Princípios SOLID

-   **S** - Single Responsibility: Cada classe tem uma única responsabilidade
-   **O** - Open/Closed: Aberto para extensão, fechado para modificação
-   **L** - Liskov Substitution: Subtipos devem ser substituíveis
-   **I** - Interface Segregation: Interfaces específicas são melhores
-   **D** - Dependency Inversion: Dependa de abstrações, não de concretizações

## Implementação

# 1. Domain Layer - Entidades

**src/domain/entities/user.py**

-   Crie o arquivo user.py em : src/domain/entities/user.py

```
src/
├── domain/
│   ├── entities/
│   │   ├── __init__.py
│   │   └── user.py

```

```python
from typing import Optional
import uuid

class User:
    id: Optional[str] = None

    def __init__(
            self,
            user_id: Optional[str] = None,
            name: str = "",
            email: str = "",
            created_at: Optional[datetime] = None,
            updated_at: Optional[datetime] = None
            ):
        self.user_id = user_id or str(uuid.uuid4())
        self.name = name
        self.email = email
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def is_valid_email(self) -> bool:
        return "@" in self.email and "." in self.email.split("@")[1]

    def __repr__(self):
        return f"User(user_id={self.user_id}, name={self.name}, email={self.email})"
```

Para criação da classe iremos utilizar o TDD e o BDD (give when then)

## 🧪 Criando a Entidade `User` com TDD + BDD

### 🎯 Objetivo

Construir a entidade `User` na camada de domínio usando **TDD** e escrever testes comportamentais com **BDD (Given-When-Then)**.

---

## 🗂️ Estrutura de Diretórios

```bash
src/
├── domain/
│   └── entities/
│       ├── __init__.py
│       └── user.py

tests/
└── domain/
    └── entities/
        ├── __init__.py
        └── test_user.py
```

---

## 🔧 Pré-requisitos

Instale o `pytest`:

```bash
pip install pytest
```

---

## ✅ Etapa 1: Criando os testes com BDD (`test_user.py`)

```gherkin
Feature: Criar o usuário

  Scenario: Verificar se usuário válido foi criado
    Given um usuário com dados válidos
    When ele for criado
    Then ele deve ter nome, email, idade e um id gerado
```

**Arquivo:** `tests/domain/entities/test_user.py`

```python
from src.domain.entities.user import User

# GIVEN um usuário com dados válidos
# WHEN ele for criado
# THEN ele deve ter nome, email, idade e um id gerado
def test_create_user():
    user = User(user_id=1, name="Leo", email="leo@gmail.com")
    assert user.name == "Leo"
```

## 🚀 Etapa 2: Rodar os testes

Execute no terminal:

```bash
pytest
```

obs.: Caso aconteceça erro de não encontrar src

crie o arquivo pytest.ini:

```text
# pytest.ini
[pytest]
pythonpath = .
asyncio_mode = strict
```

execute no terminal

```bash
PYTHONPATH=. pytest
```

Você deve ver algo como:

```
============================= test session starts ==============================
collected 1 items

tests/domain/entities/test_user.py .......                             [100%]

============================== 7 passed in 0.10s ===============================
```

**coverage** (cobertura dos testes) no seu projeto Python, siga estes passos simples:

## 1. Rode os testes com coverage:

```bash
coverage run -m pytest
```

Isso executa o `pytest` e coleta informações de cobertura.

---

## 2. Veja o relatório no terminal:

```bash
coverage report
```

Você verá um resumo como:

```
Name                             Stmts   Miss  Cover
----------------------------------------------------
src/domain/entities/user.py         7       1    86%
tests/domain/entities/test_user.py  4       0   100%
----------------------------------------------------
TOTAL                              14       1    93%
```

Esse relatório mostra a cobertura de testes do seu código:

-   Stmts é o número total de linhas de código,
-   Miss é quantas linhas não foram executadas pelos testes.
-   Cover é a porcentagem de linhas testadas.
    No exemplo, o arquivo user.py tem 7 linhas, com 1 linha não testada (86% coberto), e o arquivo de testes tem 4 linhas, todas testadas (100%). No total, o projeto tem 14 linhas com 1 linha sem cobertura, resultando em 93% de cobertura de testes.

---

## 3. Gere um relatório HTML (mais visual):

```bash
coverage html
```

Isso cria a pasta `htmlcov/`. Abra o arquivo:

```bash
firefox htmlcov/index.html
```

ou use outro navegador para ver a interface gráfica da cobertura.

---

## 4. Limpar dados antigos (opcional):

```bash
coverage erase
```

---

### Extra: rodar tudo em um comando só

```bash
coverage run -m pytest && coverage report && coverage html
```

Vamos continuar os testes:

```python
from src.domain.entities.user import User

# GIVEN um usuário com dados válidos
# WHEN ele for criado
# THEN ele deve ter nome, email, idade e um id gerado
def test_create_user():
    user = User(user_id="1", name="Leo", email="leo@gmail.com")  # user_id como str
    assert user.name == "Leo"
    assert user.user_id == "1"
    assert user.email == "leo@gmail.com"
    assert repr(user) == "User(user_id=1, name=Leo, email=leo@gmail.com)"
```

## 1. Rode os testes com coverage:

```bash
coverage run -m pytest
```

Isso executa o `pytest` e coleta informações de cobertura.

---

## 2. Veja o relatório no terminal:

```bash
coverage report
```

Você verá um resumo como:

```
Name                             Stmts   Miss  Cover
----------------------------------------------------
src/domain/entities/user.py         7       1   100%
tests/domain/entities/test_user.py  4       0   100%
----------------------------------------------------
TOTAL                              14       1   100%
```

Vamos continuar a implementar

```python
from src.domain.entities.user import User
from datetime import datetime
# executar:PYTHONPATH=. pytest -s
# executar:PYTHONPATH=. pytest -spytest --maxfail=1 --disable-warnings -v
# coverage report
# coverage run -m pytest


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

```

Inclua o restante do código:

```python
from datetime import datetime
from typing import Optional
import uuid

class User:
    id: Optional[str] = None

    def __init__(
            self,
            user_id: Optional[str] = None,
            name: str = "",
            email: str = "",
            created_at: Optional[datetime] = None,
            updated_at: Optional[datetime] = None
            ):
        self.user_id = user_id or str(uuid.uuid4())
        self.name = name
        self.email = email
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def is_valid_email(self) -> bool:
        return "@" in self.email and "." in self.email.split("@")[1]

    def __repr__(self):
        return f"User(user_id={self.user_id}, name={self.name}, email={self.email})"
```

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx

# 2. Application Layer - Use Cases

Vamos agora criara a camada de aplicação e criar funcionalidade riar usuários

**src/application/usecases/user_usecase.py**

```python
from ...domain.entities.user import User

class UserUseCase:

    def __init__(self):
        pass  # ou inicialize atributos aqui

    async def create_user(self, request: None) -> User:
        """Caso de uso: Criar usuário"""
        # Verifica se email já existe
        existing_user = True  # Simulação de verificação de email existente
        if existing_user:
            raise ValueError("Email já está em uso")

        # Cria entidade
        user = User(
            name=request.name,
            email=request.email,
            age=request.age
        )

        # Aplica validações de domínio
        # Persiste
        # Envia boas-vindas (padrão Observer)
        # Retorna a entidade criada
        return user
```

Veja o teste em: tests/application/usecases/test_user_usecase.py

Para implementar ainda mais o usecase precisamos:

-   Verifica se email já existe
-   Aplica validações de domínio
-   Persistencia
-   Envia boas-vindas (padrão Observer)
-   DTO

Vamos implementar o repositorio para realizarmos a verificação do email e a persistencia no banco de dados.

Para implementarmos o repositorio vamos primeiramente criar uma interface e implementar esta interface.

### Domain Layer - Repository Interface (Port)

src/domain/repositories/user_repository.py

crie o arquivo iuser_repository.py em src/domain/entities/repositories/iuser_repository.py

```python
from abc import ABC, abstractmethod
from src.domain.entities.user import User

class IUserRepository(ABC):

    @abstractmethod
    async def create(self, user: User) -> User:
        """Cria um novo usuário"""
        pass

```

Vamos implementar a interface:

### Infrastructure Layer - Repository Implementation

**src/infrastructure/repositories/sqlite_user_repository.py**

```python
from typing import List, Optional
import aiosqlite
from ...domain.repositories.user_repository import UserRepository
from ...domain.entities.user import User
from ..database.connection import DatabaseConnection
from ..database.models import UserModel

class SQLiteUserRepository(UserRepository):
    """
    Implementação concreta do repositório usando SQLite (Adapter).
    Implementa o padrão Repository.
    """

    def __init__(self, db_connection: DatabaseConnection):
        self._db_connection = db_connection

    async def create(self, user: User) -> User:
        """Implementa criação no SQLite"""
        model = UserModel.from_domain(user)

        async for connection in self._db_connection.get_connection():
            await connection.execute(
                """INSERT INTO users (id, name, email, age, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (model.id, model.name, model.email, model.age,
                 model.created_at, model.updated_at)
            )
            await connection.commit()

        return user

    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Implementa busca por ID no SQLite"""
        async for connection in self._db_connection.get_connection():
            cursor = await connection.execute(
                "SELECT * FROM users WHERE id = ?", (user_id,)
            )
            row = await cursor.fetchone()

            if row:
                model = UserModel(*row)
                return model.to_domain()

        return None

    async def get_by_email(self, email: str) -> Optional[User]:
        """Implementa busca por email no SQLite"""
        async for connection in self._db_connection.get_connection():
            cursor = await connection.execute(
                "SELECT * FROM users WHERE email = ?", (email,)
            )
            row = await cursor.fetchone()

            if row:
                model = UserModel(*row)
                return model.to_domain()

        return None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Implementa listagem com paginação no SQLite"""
        async for connection in self._db_connection.get_connection():
            cursor = await connection.execute(
                "SELECT * FROM users LIMIT ? OFFSET ?", (limit, skip)
            )
            rows = await cursor.fetchall()

            return [UserModel(*row).to_domain() for row in rows]

    async def update(self, user: User) -> User:
        """Implementa atualização no SQLite"""
        model = UserModel.from_domain(user)

        async for connection in self._db_connection.get_connection():
            await connection.execute(
                """UPDATE users SET name = ?, email = ?, age = ?, updated_at = ?
                   WHERE id = ?""",
                (model.name, model.email, model.age, model.updated_at, model.id)
            )
            await connection.commit()

        return user

    async def delete(self, user_id: str) -> bool:
        """Implementa remoção no SQLite"""
        async for connection in self._db_connection.get_connection():
            cursor = await connection.execute(
                "DELETE FROM users WHERE id = ?", (user_id,)
            )
            await connection.commit()

            return cursor.rowcount > 0
```

### Application Layer - DTOs

**src/application/dtos/user_dto.py**

```python
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

class CreateUserRequest(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    age: int = Field(0, ge=0)

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    age: int
    is_adult: bool
    created_at: datetime
    updated_at: datetime
```

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx
(em contrução daqui para baixo)

Vamos implementar ainda mais o usecase:

```python
from typing import List, Optional
from ..dtos.user_dto import CreateUserRequest, UserResponse
from ...domain.entities.user import User
from ...domain.repositories.user_repository import UserRepository
#from ...domain.services.user_service import UserDomainService

class UserUseCase:
    """
    Casos de uso para operações com usuários.
    Implementa a lógica de aplicação seguindo o padrão Command.
    """

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def create_user(self, request: CreateUserRequest) -> UserResponse:
        """Caso de uso: Criar usuário"""
        # Verifica se email já existe
        existing_user = await self._user_repository.get_by_email(request.email)
        if existing_user:
            raise ValueError("Email já está em uso")

        # Cria entidade
        user = User(
            name=request.name,
            email=request.email,
            age=request.age
        )

        # Aplica validações de domínio
        #await self._user_domain_service.validate_user_creation(user)

        # Persiste
        created_user = await self._user_repository.create(user)

        # Envia boas-vindas (padrão Observer)
        await self._user_domain_service.welcome_new_user(created_user)

        return UserResponse(
            id=created_user.id,
            name=created_user.name,
            email=created_user.email,
            age=created_user.age,
            is_adult=created_user.is_adult(),
            created_at=created_user.created_at,
            updated_at=created_user.updated_at
        )

    #async def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:

    #async def get_all_users(self, skip: int = 0, limit: int = 100) -> PaginatedUsersResponse:

    #async def update_user(self, user_id: str, request: UpdateUserRequest) -> Optional[UserResponse]:

    #async def delete_user(self, user_id: str) -> bool:

# Command significa encapsular uma ação de negócio (como criar, atualizar, deletar) dentro de um método ou objeto específico.
```

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx

# Projeto completo profissional:

---

## 🛠️ Etapa 1: Criar a classe `User` com base nos testes

---

### ✅ Classe `User` desacoplada (sem decoradores)

```python
from datetime import datetime
from typing import Optional
import uuid

class User:
    """
    Entidade User seguindo DDD, sem decoradores como @dataclass e @classmethod.
    """

    def __init__(
        self,
        name: str,
        email: str,
        age: int = 0,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.email = email
        self.age = age
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def is_adult(self) -> bool:
        """Regra de negócio: verifica se o usuário é maior de idade"""
        return self.age >= 18

    def is_valid_email(self) -> bool:
        """Regra de negócio: valida formato básico do email"""
        return "@" in self.email and "." in self.email.split("@")[1]

    def update_info(self, name: Optional[str] = None, email: Optional[str] = None, age: Optional[int] = None):
        """Atualiza informações do usuário mantendo a data de atualização"""
        if name:
            self.name = name
        if email:
            self.email = email
        if age is not None:
            self.age = age
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> dict:
        """Converte a entidade para dicionário (sem dependências externas)"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "is_adult": self.is_adult(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def from_dict(data: dict) -> 'User':
        """Cria uma entidade a partir de um dicionário"""
        created_at = datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None
        updated_at = datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else None

        return User(
            id=data.get("id"),
            name=data.get("name", ""),
            email=data.get("email", ""),
            age=data.get("age", 0),
            created_at=created_at,
            updated_at=updated_at
        )
```

### ✅ Diferenças principais:

-   `__init__` personalizado substitui `@dataclass` e `__post_init__`
-   `from_dict` agora é `@staticmethod`, não mais `@classmethod`
-   Sem nenhuma dependência externa além da biblioteca padrão (`datetime`, `uuid`)

Appliando os conhecimentos:

### 🧩 `@dataclass` — Facilita a criação de classes de dados

O `@dataclass` é um **decorador** da biblioteca `dataclasses` (desde o Python 3.7) que reduz o **boilerplate** (código repetitivo) ao criar classes que servem basicamente para armazenar dados.

#### ✅ O que ele faz automaticamente:

-   Cria o método `__init__`
-   Cria o `__repr__` (representação)
-   Cria o `__eq__` (comparação de igualdade)
-   Pode gerar métodos como `__lt__`, `__le__`, etc., se configurado

#### 🧪 Exemplo com e sem `@dataclass`

**Sem `@dataclass`:**

```python
class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade
```

**Com `@dataclass`:**

```python
from dataclasses import dataclass

@dataclass
class Pessoa:
    nome: str
    idade: int
```

---

### 🧠 `@classmethod` — Método da classe (não da instância)

O `@classmethod` define um método que **recebe a classe como primeiro argumento** (chamado `cls`), e não a instância (`self`). É útil para **fábricas de objetos** ou lógica que envolve a classe em si.

#### ✅ Quando usar:

-   Criar instâncias com lógica extra (`factories`)
-   Modificar atributos da classe
-   Métodos utilitários relacionados à classe

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid

@dataclass
class User:
    """
    Entidade User seguindo DDD.
    Representa um usuário no domínio da aplicação.
    IMPORTANTE: Esta classe não possui dependências externas ou decorators.
    """
    id: Optional[str] = None
    name: str = ""
    email: str = ""
    age: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())

        if self.created_at is None:
            self.created_at = datetime.utcnow()

        self.updated_at = datetime.utcnow()

    def is_adult(self) -> bool:
        """Regra de negócio: verifica se o usuário é maior de idade"""
        return self.age >= 18

    def is_valid_email(self) -> bool:
        """Regra de negócio: valida formato básico do email"""
        return "@" in self.email and "." in self.email.split("@")[1]

    def update_info(self, name: str = None, email: str = None, age: int = None):
        """Atualiza informações do usuário mantendo a data de atualização"""
        if name:
            self.name = name
        if email:
            self.email = email
        if age is not None:
            self.age = age
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> dict:
        """Converte a entidade para dicionário (sem dependências externas)"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "is_adult": self.is_adult(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Cria uma entidade a partir de um dicionário"""
        user = cls(
            id=data.get("id"),
            name=data.get("name", ""),
            email=data.get("email", ""),
            age=data.get("age", 0)
        )

        if data.get("created_at"):
            user.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("updated_at"):
            user.updated_at = datetime.fromisoformat(data["updated_at"])

        return user
```

### 2. Domain Layer - Repository Interface (Port)

**src/domain/repositories/user_repository.py**

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.user import User

class UserRepository(ABC):
    """
    Interface do repositório (Port) - Princípio da Inversão de Dependência.
    Define o contrato sem implementação específica.
    """

    @abstractmethod
    async def create(self, user: User) -> User:
        """Cria um novo usuário"""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Busca usuário por ID"""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Busca usuário por email"""
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Lista todos os usuários com paginação"""
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """Atualiza um usuário"""
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        """Remove um usuário"""
        pass
```

### 3. Domain Layer - Service Interface

**src/domain/services/user_service.py**

```python
from abc import ABC, abstractmethod
from ..entities.user import User

class NotificationService(ABC):
    """Interface para serviços de notificação - SEM decorators ou dependências externas"""

    @abstractmethod
    async def send_welcome_email(self, user: User) -> bool:
        """Envia email de boas-vindas para o usuário"""
        pass

class UserDomainService:
    """
    Serviço de domínio para regras complexas que envolvem múltiplas entidades.
    Implementa o padrão Strategy para diferentes tipos de validação.
    IMPORTANTE: Esta classe não possui decorators ou dependências de frameworks.
    """

    def __init__(self, notification_service: NotificationService):
        self._notification_service = notification_service

    def validate_user_creation(self, user: User) -> tuple[bool, list[str]]:
        """
        Valida se um usuário pode ser criado.
        Retorna (é_válido, lista_de_erros)
        """
        errors = []

        if not user.name or len(user.name.strip()) < 2:
            errors.append("Nome deve ter pelo menos 2 caracteres")

        if not user.is_valid_email():
            errors.append("Email inválido")

        if user.age < 0 or user.age > 150:
            errors.append("Idade deve estar entre 0 e 150 anos")

        if len(user.name) > 100:
            errors.append("Nome não pode ter mais de 100 caracteres")

        return len(errors) == 0, errors

    def validate_user_update(self, user: User, current_data: dict) -> tuple[bool, list[str]]:
        """
        Valida atualização de usuário considerando dados atuais.
        Permite validações mais específicas para updates.
        """
        is_valid, errors = self.validate_user_creation(user)

        # Regras específicas para update podem ser adicionadas aqui
        if user.id != current_data.get("id"):
            errors.append("ID do usuário não pode ser alterado")

        return len(errors) == 0, errors

    async def welcome_new_user(self, user: User) -> bool:
        """Envia boas-vindas para novo usuário"""
        try:
            return await self._notification_service.send_welcome_email(user)
        except Exception:
            # Em um cenário real, você poderia logar o erro
            return False

    def calculate_user_category(self, user: User) -> str:
        """
        Regra de negócio: categoriza usuário baseado na idade.
        Exemplo de lógica de domínio complexa.
        """
        if user.age < 13:
            return "crianca"
        elif user.age < 18:
            return "adolescente"
        elif user.age < 60:
            return "adulto"
        else:
            return "idoso"

    def can_user_perform_action(self, user: User, action: str) -> bool:
        """
        Regra de negócio: verifica se usuário pode realizar determinada ação.
        Exemplo de autorização baseada em domínio.
        """
        action_rules = {
            "create_content": user.is_adult(),
            "purchase": user.is_adult(),
            "view_content": user.age >= 13,
            "basic_actions": True
        }

        return action_rules.get(action, False)
```

### 4. Application Layer - DTOs

**src/application/dtos/user_dto.py**

```python
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

# DTOs usando dataclasses puras - SEM dependências de Pydantic
# Mantém a camada de aplicação desacoplada de frameworks

@dataclass
class CreateUserRequest:
    """DTO para criação de usuário - SEM decorators de framework"""
    name: str
    email: str
    age: int

    def validate(self) -> tuple[bool, list[str]]:
        """Validação básica dos dados de entrada"""
        errors = []

        if not self.name or not isinstance(self.name, str):
            errors.append("Nome é obrigatório e deve ser texto")
        elif len(self.name.strip()) < 2:
            errors.append("Nome deve ter pelo menos 2 caracteres")
        elif len(self.name) > 100:
            errors.append("Nome não pode ter mais de 100 caracteres")

        if not self.email or not isinstance(self.email, str):
            errors.append("Email é obrigatório")
        elif "@" not in self.email:
            errors.append("Email deve conter @")

        if not isinstance(self.age, int):
            errors.append("Idade deve ser um número inteiro")
        elif self.age < 0 or self.age > 150:
            errors.append("Idade deve estar entre 0 e 150 anos")

        return len(errors) == 0, errors

@dataclass
class UpdateUserRequest:
    """DTO para atualização de usuário"""
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None

    def validate(self) -> tuple[bool, list[str]]:
        """Validação dos dados de atualização"""
        errors = []

        if self.name is not None:
            if not isinstance(self.name, str):
                errors.append("Nome deve ser texto")
            elif len(self.name.strip()) < 2:
                errors.append("Nome deve ter pelo menos 2 caracteres")
            elif len(self.name) > 100:
                errors.append("Nome não pode ter mais de 100 caracteres")

        if self.email is not None:
            if not isinstance(self.email, str):
                errors.append("Email deve ser texto")
            elif "@" not in self.email:
                errors.append("Email deve conter @")

        if self.age is not None:
            if not isinstance(self.age, int):
                errors.append("Idade deve ser um número inteiro")
            elif self.age < 0 or self.age > 150:
                errors.append("Idade deve estar entre 0 e 150 anos")

        return len(errors) == 0, errors

    def has_updates(self) -> bool:
        """Verifica se há pelo menos um campo para atualizar"""
        return any([self.name is not None, self.email is not None, self.age is not None])

@dataclass
class UserResponse:
    """DTO para resposta de usuário"""
    id: str
    name: str
    email: str
    age: int
    is_adult: bool
    category: str
    created_at: str  # ISO format string
    updated_at: str  # ISO format string

    @classmethod
    def from_domain(cls, user, category: str = None) -> 'UserResponse':
        """Cria UserResponse a partir da entidade de domínio"""
        return cls(
            id=user.id,
            name=user.name,
            email=user.email,
            age=user.age,
            is_adult=user.is_adult(),
            category=category or "unknown",
            created_at=user.created_at.isoformat() if user.created_at else "",
            updated_at=user.updated_at.isoformat() if user.updated_at else ""
        )

@dataclass
class PaginatedUsersResponse:
    """DTO para resposta paginada"""
    users: list[UserResponse]
    total: int
    skip: int
    limit: int
    has_next: bool
    has_previous: bool

    @classmethod
    def create(cls, users: list[UserResponse], total: int, skip: int, limit: int) -> 'PaginatedUsersResponse':
        """Factory method para criar resposta paginada"""
        return cls(
            users=users,
            total=total,
            skip=skip,
            limit=limit,
            has_next=skip + limit < total,
            has_previous=skip > 0
        )

@dataclass
class UserCreatedEvent:
    """DTO para evento de usuário criado - para notificações"""
    user_id: str
    user_name: str
    user_email: str
    timestamp: str

    @classmethod
    def from_user(cls, user) -> 'UserCreatedEvent':
        """Cria evento a partir da entidade de usuário"""
        return cls(
            user_id=user.id,
            user_name=user.name,
            user_email=user.email,
            timestamp=datetime.utcnow().isoformat()
        )

# Classes de resultado para operações
@dataclass
class OperationResult:
    """Resultado base para operações"""
    success: bool
    message: str
    errors: list[str]

    @classmethod
    def success_result(cls, message: str = "Operação realizada com sucesso") -> 'OperationResult':
        return cls(success=True, message=message, errors=[])

    @classmethod
    def error_result(cls, message: str, errors: list[str] = None) -> 'OperationResult':
        return cls(success=False, message=message, errors=errors or [])

@dataclass
class UserOperationResult(OperationResult):
    """Resultado específico para operações com usuário"""
    user: Optional[UserResponse] = None

    @classmethod
    def success_with_user(cls, user: UserResponse, message: str = "Usuário processado com sucesso") -> 'UserOperationResult':
        return cls(success=True, message=message, errors=[], user=user)
```

### 5. Application Layer - Use Cases

**src/application/usecases/user_usecase.py**

```python
from typing import List, Optional
from ..dtos.user_dto import CreateUserRequest, UpdateUserRequest, UserResponse, PaginatedUsersResponse
from ...domain.entities.user import User
from ...domain.repositories.user_repository import UserRepository
from ...domain.services.user_service import UserDomainService

class UserUseCase:
    """
    Casos de uso para operações com usuários.
    Implementa a lógica de aplicação seguindo o padrão Command.
    """

    def __init__(self, user_repository: UserRepository, user_domain_service: UserDomainService):
        self._user_repository = user_repository
        self._user_domain_service = user_domain_service

    async def create_user(self, request: CreateUserRequest) -> UserResponse:
        """Caso de uso: Criar usuário"""
        # Verifica se email já existe
        existing_user = await self._user_repository.get_by_email(request.email)
        if existing_user:
            raise ValueError("Email já está em uso")

        # Cria entidade
        user = User(
            name=request.name,
            email=request.email,
            age=request.age
        )

        # Aplica validações de domínio
        await self._user_domain_service.validate_user_creation(user)

        # Persiste
        created_user = await self._user_repository.create(user)

        # Envia boas-vindas (padrão Observer)
        await self._user_domain_service.welcome_new_user(created_user)

        return UserResponse(
            id=created_user.id,
            name=created_user.name,
            email=created_user.email,
            age=created_user.age,
            is_adult=created_user.is_adult(),
            created_at=created_user.created_at,
            updated_at=created_user.updated_at
        )

    async def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        """Caso de uso: Buscar usuário por ID"""
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            return None

        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            age=user.age,
            is_adult=user.is_adult(),
            created_at=user.created_at,
            updated_at=user.updated_at
        )

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> PaginatedUsersResponse:
        """Caso de uso: Listar usuários"""
        users = await self._user_repository.get_all(skip, limit)

        user_responses = [
            UserResponse(
                id=user.id,
                name=user.name,
                email=user.email,
                age=user.age,
                is_adult=user.is_adult(),
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            for user in users
        ]

        return PaginatedUsersResponse(
            users=user_responses,
            total=len(user_responses),
            skip=skip,
            limit=limit
        )

    async def update_user(self, user_id: str, request: UpdateUserRequest) -> Optional[UserResponse]:
        """Caso de uso: Atualizar usuário"""
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            return None

        # Verifica se novo email já existe (se fornecido)
        if request.email and request.email != user.email:
            existing_user = await self._user_repository.get_by_email(request.email)
            if existing_user:
                raise ValueError("Email já está em uso")

        # Atualiza dados
        user.update_info(
            name=request.name,
            email=request.email,
            age=request.age
        )

        # Valida novamente
        await self._user_domain_service.validate_user_creation(user)

        # Persiste
        updated_user = await self._user_repository.update(user)

        return UserResponse(
            id=updated_user.id,
            name=updated_user.name,
            email=updated_user.email,
            age=updated_user.age,
            is_adult=updated_user.is_adult(),
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at
        )

    async def delete_user(self, user_id: str) -> bool:
        """Caso de uso: Deletar usuário"""
        return await self._user_repository.delete(user_id)
```

### 6. Infrastructure Layer - Database

**src/infrastructure/database/connection.py**

```python
import aiosqlite
from typing import AsyncGenerator
import os

class DatabaseConnection:
    """
    Gerenciador de conexão com banco SQLite.
    Implementa o padrão Singleton para garantir uma única instância.
    """
    _instance = None
    _database_path = "users.db"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def get_connection(self) -> AsyncGenerator[aiosqlite.Connection, None]:
        """Fornece conexão com o banco"""
        async with aiosqlite.connect(self._database_path) as connection:
            yield connection

    async def init_database(self):
        """Inicializa o banco de dados criando as tabelas"""
        async with aiosqlite.connect(self._database_path) as connection:
            await connection.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    age INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            await connection.commit()
```

**src/infrastructure/database/models.py**

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class UserModel:
    """Modelo de dados para persistência (Adapter)"""
    id: str
    name: str
    email: str
    age: int
    created_at: str
    updated_at: str

    @classmethod
    def from_domain(cls, user) -> 'UserModel':
        """Converte entidade de domínio para modelo de dados"""
        return cls(
            id=user.id,
            name=user.name,
            email=user.email,
            age=user.age,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat()
        )

    def to_domain(self):
        """Converte modelo de dados para entidade de domínio"""
        from ...domain.entities.user import User
        return User(
            id=self.id,
            name=self.name,
            email=self.email,
            age=self.age,
            created_at=datetime.fromisoformat(self.created_at),
            updated_at=datetime.fromisoformat(self.updated_at)
        )
```

### 7. Infrastructure Layer - Repository Implementation

**src/infrastructure/repositories/sqlite_user_repository.py**

```python
from typing import List, Optional
import aiosqlite
from ...domain.repositories.user_repository import UserRepository
from ...domain.entities.user import User
from ..database.connection import DatabaseConnection
from ..database.models import UserModel

class SQLiteUserRepository(UserRepository):
    """
    Implementação concreta do repositório usando SQLite (Adapter).
    Implementa o padrão Repository.
    """

    def __init__(self, db_connection: DatabaseConnection):
        self._db_connection = db_connection

    async def create(self, user: User) -> User:
        """Implementa criação no SQLite"""
        model = UserModel.from_domain(user)

        async for connection in self._db_connection.get_connection():
            await connection.execute(
                """INSERT INTO users (id, name, email, age, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (model.id, model.name, model.email, model.age,
                 model.created_at, model.updated_at)
            )
            await connection.commit()

        return user

    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Implementa busca por ID no SQLite"""
        async for connection in self._db_connection.get_connection():
            cursor = await connection.execute(
                "SELECT * FROM users WHERE id = ?", (user_id,)
            )
            row = await cursor.fetchone()

            if row:
                model = UserModel(*row)
                return model.to_domain()

        return None

    async def get_by_email(self, email: str) -> Optional[User]:
        """Implementa busca por email no SQLite"""
        async for connection in self._db_connection.get_connection():
            cursor = await connection.execute(
                "SELECT * FROM users WHERE email = ?", (email,)
            )
            row = await cursor.fetchone()

            if row:
                model = UserModel(*row)
                return model.to_domain()

        return None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Implementa listagem com paginação no SQLite"""
        async for connection in self._db_connection.get_connection():
            cursor = await connection.execute(
                "SELECT * FROM users LIMIT ? OFFSET ?", (limit, skip)
            )
            rows = await cursor.fetchall()

            return [UserModel(*row).to_domain() for row in rows]

    async def update(self, user: User) -> User:
        """Implementa atualização no SQLite"""
        model = UserModel.from_domain(user)

        async for connection in self._db_connection.get_connection():
            await connection.execute(
                """UPDATE users SET name = ?, email = ?, age = ?, updated_at = ?
                   WHERE id = ?""",
                (model.name, model.email, model.age, model.updated_at, model.id)
            )
            await connection.commit()

        return user

    async def delete(self, user_id: str) -> bool:
        """Implementa remoção no SQLite"""
        async for connection in self._db_connection.get_connection():
            cursor = await connection.execute(
                "DELETE FROM users WHERE id = ?", (user_id,)
            )
            await connection.commit()

            return cursor.rowcount > 0
```

### 8. Infrastructure Layer - External Services

**src/infrastructure/services/email_service.py**

```python
import logging
from ...domain.services.user_service import NotificationService
from ...domain.entities.user import User

class EmailService(NotificationService):
    """
    Implementação concreta do serviço de notificação.
    Em produção, integraria com serviços como SendGrid, SES, etc.
    """

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    async def send_welcome_email(self, user: User) -> bool:
        """Simula envio de email de boas-vindas"""
        try:
            # Em produção, aqui faria a integração real
            self._logger.info(f"Enviando email de boas-vindas para {user.email}")

            # Simula sucesso
            return True

        except Exception as e:
            self._logger.error(f"Erro ao enviar email: {e}")
            return False

class MockEmailService(NotificationService):
    """Implementação mock para testes"""

    async def send_welcome_email(self, user: User) -> bool:
        print(f"📧 Email de boas-vindas enviado para {user.name} ({user.email})")
        return True
```

### 9. Presentation Layer - FastAPI DTOs (Adapters)

**src/presentation/dtos/fastapi_user_dto.py**

```python
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from ...application.dtos.user_dto import CreateUserRequest, UpdateUserRequest, UserResponse

# Estes DTOs são adaptadores que fazem a ponte entre FastAPI e a camada de aplicação
# Eles possuem decorators e dependências do Pydantic/FastAPI

class FastAPICreateUserRequest(BaseModel):
    """Adapter do DTO de criação para FastAPI com validações do Pydantic"""
    name: str = Field(..., min_length=2, max_length=100, description="Nome do usuário")
    email: EmailStr = Field(..., description="Email válido do usuário")
    age: int = Field(..., ge=0, le=150, description="Idade do usuário")

    def to_application_dto(self) -> CreateUserRequest:
        """Converte para DTO da camada de aplicação"""
        return CreateUserRequest(
            name=self.name,
            email=str(self.email),
            age=self.age
        )

class FastAPIUpdateUserRequest(BaseModel):
    """Adapter do DTO de atualização para FastAPI"""
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Novo nome do usuário")
    email: Optional[EmailStr] = Field(None, description="Novo email do usuário")
    age: Optional[int] = Field(None, ge=0, le=150, description="Nova idade do usuário")

    def to_application_dto(self) -> UpdateUserRequest:
        """Converte para DTO da camada de aplicação"""
        return UpdateUserRequest(
            name=self.name,
            email=str(self.email) if self.email else None,
            age=self.age
        )

class FastAPIUserResponse(BaseModel):
    """Adapter do DTO de resposta para FastAPI"""
    id: str
    name: str
    email: str
    age: int
    is_adult: bool
    category: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_application_dto(cls, user_response: UserResponse) -> 'FastAPIUserResponse':
        """Converte do DTO da camada de aplicação"""
        return cls(
            id=user_response.id,
            name=user_response.name,
            email=user_response.email,
            age=user_response.age,
            is_adult=user_response.is_adult,
            category=user_response.category,
            created_at=datetime.fromisoformat(user_response.created_at),
            updated_at=datetime.fromisoformat(user_response.updated_at)
        )

class FastAPIPaginatedUsersResponse(BaseModel):
    """Adapter do DTO paginado para FastAPI"""
    users: list[FastAPIUserResponse]
    total: int = Field(..., description="Total de usuários")
    skip: int = Field(..., description="Itens ignorados")
    limit: int = Field(..., description="Limite de itens")
    has_next: bool = Field(..., description="Possui próxima página")
    has_previous: bool = Field(..., description="Possui página anterior")

class FastAPIErrorResponse(BaseModel):
    """Resposta de erro padronizada para FastAPI"""
    success: bool = False
    message: str
    errors: list[str] = []

class FastAPISuccessResponse(BaseModel):
    """Resposta de sucesso padronizada para FastAPI"""
    success: bool = True
    message: str

class FastAPIUserPermissionRequest(BaseModel):
    """Request para verificação de permissões"""
    action: str = Field(..., description="Ação que o usuário deseja realizar")

class FastAPIUserPermissionResponse(BaseModel):
    """Resposta de verificação de permissões"""
    user_id: str
    action: str
    can_perform: bool
    message: str
```

**src/presentation/dependencies/container.py**

```python
from functools import lru_cache
from ...infrastructure.database.connection import DatabaseConnection
from ...infrastructure.repositories.sqlite_user_repository import SQLiteUserRepository
from ...infrastructure.services.email_service import MockEmailService
from ...domain.services.user_service import UserDomainService
from ...application.usecases.user_usecase import UserUseCase

class DependencyContainer:
    """
    Container de injeção de dependências.
    Implementa o padrão Factory e Dependency Injection.
    """

    def __init__(self):
        self._instances = {}

    @lru_cache()
    def get_database_connection(self) -> DatabaseConnection:
        """Factory para conexão com banco"""
        if 'db_connection' not in self._instances:
            self._instances['db_connection'] = DatabaseConnection()
        return self._instances['db_connection']

    @lru_cache()
    def get_user_repository(self) -> SQLiteUserRepository:
        """Factory para repositório de usuários"""
        if 'user_repository' not in self._instances:
            db_connection = self.get_database_connection()
            self._instances['user_repository'] = SQLiteUserRepository(db_connection)
        return self._instances['user_repository']

    @lru_cache()
    def get_email_service(self) -> MockEmailService:
        """Factory para serviço de email"""
        if 'email_service' not in self._instances:
            self._instances['email_service'] = MockEmailService()
        return self._instances['email_service']

    @lru_cache()
    def get_user_domain_service(self) -> UserDomainService:
        """Factory para serviço de domínio"""
        if 'user_domain_service' not in self._instances:
            email_service = self.get_email_service()
            self._instances['user_domain_service'] = UserDomainService(email_service)
        return self._instances['user_domain_service']

    @lru_cache()
    def get_user_usecase(self) -> UserUseCase:
        """Factory para caso de uso de usuários"""
        if 'user_usecase' not in self._instances:
            user_repository = self.get_user_repository()
            user_domain_service = self.get_user_domain_service()
            self._instances['user_usecase'] = UserUseCase(user_repository, user_domain_service)
        return self._instances['user_usecase']

# Instância global do container
container = DependencyContainer()

# Funções de dependência para FastAPI
def get_user_usecase() -> UserUseCase:
    return container.get_user_usecase()

async def init_database():
    """Inicializa o banco de dados"""
    db_connection = container.get_database_connection()
    await db_connection.init_database()
```

### 11. Presentation Layer - Controller

**src/presentation/controllers/user_controller.py**

```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
from ...application.usecases.user_usecase import UserUseCase
from ..dtos.fastapi_user_dto import (
    FastAPICreateUserRequest,
    FastAPIUpdateUserRequest,
    FastAPIUserResponse,
    FastAPIPaginatedUsersResponse,
    FastAPIErrorResponse,
    FastAPISuccessResponse,
    FastAPIUserPermissionRequest,
    FastAPIUserPermissionResponse
)
from ..dependencies.container import get_user_usecase

class UserController:
    """
    Controlador REST para operações com usuários.
    Implementa o padrão MVC (Controller).
    Esta classe SIM possui decorators pois é da camada de apresentação.
    """

    def __init__(self):
        self.router = APIRouter(
            prefix="/users",
            tags=["Users"],
            responses={
                400: {"model": FastAPIErrorResponse, "description": "Erro de validação"},
                404: {"model": FastAPIErrorResponse, "description": "Recurso não encontrado"},
                500: {"model": FastAPIErrorResponse, "description": "Erro interno"}
            }
        )
        self._setup_routes()

    def _setup_routes(self):
        """Configura as rotas do controlador"""
        self.router.add_api_route(
            "/",
            self.create_user,
            methods=["POST"],
            response_model=FastAPIUserResponse,
            status_code=status.HTTP_201_CREATED,
            summary="Criar usuário",
            description="Cria um novo usuário no sistema"
        )

        self.router.add_api_route(
            "/",
            self.get_users,
            methods=["GET"],
            response_model=FastAPIPaginatedUsersResponse,
            summary="Listar usuários",
            description="Lista usuários com paginação"
        )

        self.router.add_api_route(
            "/{user_id}",
            self.get_user,
            methods=["GET"],
            response_model=FastAPIUserResponse,
            summary="Buscar usuário",
            description="Busca um usuário específico por ID"
        )

        self.router.add_api_route(
            "/{user_id}",
            self.update_user,
            methods=["PUT"],
            response_model=FastAPIUserResponse,
            summary="Atualizar usuário",
            description="Atualiza dados de um usuário existente"
        )

        self.router.add_api_route(
            "/{user_id}",
            self.delete_user,
            methods=["DELETE"],
            response_model=FastAPISuccessResponse,
            summary="Deletar usuário",
            description="Remove um usuário do sistema"
        )

        self.router.add_api_route(
            "/email/{email}",
            self.get_user_by_email,
            methods=["GET"],
            response_model=FastAPIUserResponse,
            summary="Buscar por email",
            description="Busca um usuário pelo endereço de email"
        )

        self.router.add_api_route(
            "/{user_id}/permissions",
            self.check_user_permissions,
            methods=["POST"],
            response_model=FastAPIUserPermissionResponse,
            summary="Verificar permissões",
            description="Verifica se o usuário pode realizar uma ação específica"
        )

    async def create_user(
        self,
        request: FastAPICreateUserRequest,
        usecase: UserUseCase = Depends(get_user_usecase)
    ) -> FastAPIUserResponse:
        """Endpoint para criar usuário"""
        try:
            # Converte FastAPI DTO para Application DTO
            app_request = request.to_application_dto()

            # Executa caso de uso
            result = await usecase.create_user(app_request)

            if not result.success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "message": result.message,
                        "errors": result.errors
                    }
                )

            # Converte Application DTO para FastAPI DTO
            return FastAPIUserResponse.from_application_dto(result.user)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": "Erro interno do servidor", "errors": [str(e)]}
            )

    async def get_users(
        self,
        skip: int = Query(0, ge=0, description="Número de itens a pular"),
        limit: int = Query(100, ge=1, le=1000, description="Limite de itens por página"),
        usecase: UserUseCase = Depends(get_user_usecase)
    ) -> FastAPIPaginatedUsersResponse:
        """Endpoint para listar usuários"""
        try:
            success, message, paginated_response = await usecase.get_all_users(skip, limit)

            if not success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"message": message, "errors": []}
                )

            # Converte usuários para FastAPI DTOs
            fastapi_users = [
                FastAPIUserResponse.from_application_dto(user)
                for user in paginated_response.users
            ]

            return FastAPIPaginatedUsersResponse(
                users=fastapi_users,
                total=paginated_response.total,
                skip=paginated_response.skip,
                limit=paginated_response.limit,
                has_next=paginated_response.has_next,
                has_previous=paginated_response.has_previous
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": "Erro interno do servidor", "errors": [str(e)]}
            )

    async def get_user(
        self,
        user_id: str,
        usecase: UserUseCase = Depends(get_user_usecase)
    ) -> FastAPIUserResponse:
        """Endpoint para buscar usuário por ID"""
        try:
            result = await usecase.get_user_by_id(user_id)

            if not result.success:
                status_code = status.HTTP_404_NOT_FOUND if "não encontrado" in result.message.lower() else status.HTTP_400_BAD_REQUEST
                raise HTTPException(
                    status_code=status_code,
                    detail={
                        "message": result.message,
                        "errors": result.errors
                    }
                )

            return FastAPIUserResponse.from_application_dto(result.user)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": "Erro interno do servidor", "errors": [str(e)]}
            )

    async def update_user(
        self,
        user_id: str,
        request: FastAPIUpdateUserRequest,
        usecase: UserUseCase = Depends(get_user_usecase)
    ) -> FastAPIUserResponse:
        """Endpoint para atualizar usuário"""
        try:
            app_request = request.to_application_dto()
            result = await usecase.update_user(user_id, app_request)

            if not result.success:
                status_code = status.HTTP_404_NOT_FOUND if "não encontrado" in result.message.lower() else status.HTTP_400_BAD_REQUEST
                raise HTTPException(
                    status_code=status_code,
                    detail={
                        "message": result.message,
                        "errors": result.errors
                    }
                )

            return FastAPIUserResponse.from_application_dto(result.user)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": "Erro interno do servidor", "errors": [str(e)]}
            )

    async def delete_user(
        self,
        user_id: str,
        usecase: UserUseCase = Depends(get_user_usecase)
    ) -> FastAPISuccessResponse:
        """Endpoint para deletar usuário"""
        try:
            result = await usecase.delete_user(user_id)

            if not result.success:
                status_code = status.HTTP_404_NOT_FOUND if "não encontrado" in result.message.lower() else status.HTTP_400_BAD_REQUEST
                raise HTTPException(
                    status_code=status_code,
                    detail={
                        "message": result.message,
                        "errors": result.errors
                    }
                )

            return FastAPISuccessResponse(message=result.message)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": "Erro interno do servidor", "errors": [str(e)]}
            )

    async def get_user_by_email(
        self,
        email: str,
        usecase: UserUseCase = Depends(get_user_usecase)
    ) -> FastAPIUserResponse:
        """Endpoint para buscar usuário por email"""
        try:
            result = await usecase.get_user_by_email(email)

            if not result.success:
                status_code = status.HTTP_404_NOT_FOUND if "não encontrado" in result.message.lower() else status.HTTP_400_BAD_REQUEST
                raise HTTPException(
                    status_code=status_code,
                    detail={
                        "message": result.message,
                        "errors": result.errors
                    }
                )

            return FastAPIUserResponse.from_application_dto(result.user)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": "Erro interno do servidor", "errors": [str(e)]}
            )

    async def check_user_permissions(
        self,
        user_id: str,
        request: FastAPIUserPermissionRequest,
        usecase: UserUseCase = Depends(get_user_usecase)
    ) -> FastAPIUserPermissionResponse:
        """Endpoint para verificar permissões do usuário"""
        try:
            success, message, can_perform = await usecase.check_user_permissions(user_id, request.action)

            if not success:
                status_code = status.HTTP_404_NOT_FOUND if "não encontrado" in message.lower() else status.HTTP_400_BAD_REQUEST
                raise HTTPException(
                    status_code=status_code,
                    detail={"message": message, "errors": []}
                )

            return FastAPIUserPermissionResponse(
                user_id=user_id,
                action=request.action,
                can_perform=can_perform,
                message=message
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": "Erro interno do servidor", "errors": [str(e)]}
            )
```

### 12. Configuration

**src/config/settings.py**

```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    Configurações da aplicação usando Pydantic Settings.
    Permite injeção via variáveis de ambiente.
    """

    # Database
    database_url: str = "sqlite:///users.db"

    # API
    api_title: str = "User Management API"
    api_description: str = "API para gerenciamento de usuários com arquitetura hexagonal"
    api_version: str = "1.0.0"

    # Security
    secret_key: Optional[str] = None

    # Email
    email_provider: str = "mock"  # mock, sendgrid, ses, etc.

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
```

### 13. Main Application

**src/main.py**

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn

from src.config.settings import settings
from src.presentation.controllers.user_controller import UserController
from src.presentation.dependencies.container import init_database

# Configuração de logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

class FastAPIApp:
    """
    Classe principal da aplicação FastAPI.
    Implementa o padrão Builder para configuração da aplicação.
    """

    def __init__(self):
        self.app = FastAPI(
            title=settings.api_title,
            description=settings.api_description,
            version=settings.api_version,
            docs_url="/docs",
            redoc_url="/redoc"
        )
        self._setup_middleware()
        self._setup_routes()
        self._setup_event_handlers()
        self._setup_exception_handlers()

    def _setup_middleware(self):
        """Configura middlewares"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Em produção, especificar origins
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _setup_routes(self):
        """Configura rotas da aplicação"""
        # Health check
        @self.app.get("/health")
        async def health_check():
            return {"status": "healthy", "service": "user-management-api"}

        # Controladores
        user_controller = UserController()
        self.app.include_router(user_controller.router, prefix="/api/v1")

    def _setup_event_handlers(self):
        """Configura eventos de inicialização e finalização"""
        @self.app.on_event("startup")
        async def startup_event():
            logger.info("Iniciando aplicação...")
            await init_database()
            logger.info("Banco de dados inicializado")
            logger.info("Aplicação iniciada com sucesso!")

        @self.app.on_event("shutdown")
        async def shutdown_event():
            logger.info("Finalizando aplicação...")

    def _setup_exception_handlers(self):
        """Configura tratamento global de exceções"""
        @self.app.exception_handler(Exception)
        async def global_exception_handler(request: Request, exc: Exception):
            logger.error(f"Erro não tratado: {exc}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={"detail": "Erro interno do servidor"}
            )

# Instância da aplicação
app_instance = FastAPIApp()
app = app_instance.app

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.log_level.lower()
    )
```

### 14. Requirements e Configuração

**requirements.txt**

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
email-validator==2.1.0
aiosqlite==0.19.0
python-multipart==0.0.6
```

### 14. Arquivo de Exemplo - Docker

**Dockerfile**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY main.py .

EXPOSE 8000

CMD ["python", "main.py"]
```

**docker-compose.yml**

```yaml
version: "3.8"

services:
    api:
        build: .
        ports:
            - "8000:8000"
        volumes:
            - ./src:/app/src
        environment:
            - LOG_LEVEL=DEBUG
        restart: unless-stopped
```

## Execução

### 1. Instalação das Dependências

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 2. Executar a Aplicação

```bash
# Desenvolvimento
python src/main.py

# Ou usando uvicorn diretamente
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Testar a API

```bash
# Criar usuário
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao@email.com",
    "age": 30
  }'

# Listar usuários
curl "http://localhost:8000/api/v1/users/"

# Buscar usuário por ID
curl "http://localhost:8000/api/v1/users/{user_id}"

# Atualizar usuário
curl -X PUT "http://localhost:8000/api/v1/users/{user_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Santos",
    "age": 31
  }'

# Deletar usuário
curl -X DELETE "http://localhost:8000/api/v1/users/{user_id}"
```

### 4. Documentação da API

Acesse a documentação interativa em:

-   Swagger UI: http://localhost:8000/docs
-   ReDoc: http://localhost:8000/redoc

## Conceitos Demonstrados

### ✅ Arquitetura Hexagonal

-   **Domínio** independente de frameworks
-   **Portas** (interfaces) e **Adaptadores** (implementações)
-   **Inversão de dependência** entre camadas

### ✅ Princípios SOLID

**Single Responsibility:**

-   Cada classe tem uma única responsabilidade
-   `UserController` apenas gerencia HTTP
-   `UserRepository` apenas persiste dados
-   `UserUseCase` apenas orquestra regras de negócio

**Open/Closed:**

-   Interfaces permitem extensão sem modificação
-   `NotificationService` pode ter múltiplas implementações

**Liskov Substitution:**

-   `SQLiteUserRepository` pode ser substituída por `PostgreSQLUserRepository`
-   `MockEmailService` substitui `EmailService` em testes

**Interface Segregation:**

-   Interfaces específicas (`UserRepository`, `NotificationService`)
-   Clientes dependem apenas do que usam

**Dependency Inversion:**

-   Módulos de alto nível não dependem de baixo nível
-   Abstrações não dependem de detalhes

### ✅ Design Patterns

**Repository Pattern:**

-   `UserRepository` abstrai persistência
-   `SQLiteUserRepository` implementa para SQLite

**Factory Pattern:**

-   `DependencyContainer` cria instâncias
-   Factories específicas para cada dependência

**Strategy Pattern:**

-   `NotificationService` permite diferentes estratégias
-   Validações podem usar diferentes estratégias

**Observer Pattern:**

-   Eventos de domínio (welcome email)
-   Extensível para outros observadores

**Singleton Pattern:**

-   `DatabaseConnection` garante única instância
-   Container de dependências

### ✅ Injeção de Dependência

-   FastAPI `Depends()` para injeção automática
-   Container centralizado gerencia dependências
-   Testabilidade através de mocks

### ✅ Clean Architecture

-   Regras de negócio no domínio
-   Casos de uso na aplicação
-   Detalhes na infraestrutura
-   Interface na apresentação

## Vantagens da Arquitetura

1. **Testabilidade**: Fácil mock de dependências
2. **Manutenibilidade**: Código organizado e desacoplado
3. **Extensibilidade**: Novas funcionalidades sem modificar existentes
4. **Flexibilidade**: Troca de tecnologias sem impacto no domínio
5. **Reutilização**: Casos de uso independentes de interface
6. **Qualidade**: Princípios SOLID garantem código limpo

Este tutorial demonstra uma implementação completa seguindo as melhores práticas de arquitetura de software, proporcionando uma base sólida para aplicações empresariais escaláveis.

### 15. Testes Unitários (Exemplo)

**tests/test_user_usecase.py**

```python
import pytest
from unittest.mock import AsyncMock, MagicMock
from src.application.usecases.user_usecase import UserUseCase
from src.application.dtos.user_dto import CreateUserRequest
from src.domain.entities.user import User

@pytest.fixture
def mock_user_repository():
    return AsyncMock()

@pytest.fixture
def mock_user_domain_service():
    service = MagicMock()
    service.validate_user_creation = MagicMock(return_value=(True, []))
    service.validate_user_update = MagicMock(return_value=(True, []))
    service.welcome_new_user = AsyncMock(return_value=True)
    service.calculate_user_category = MagicMock(return_value="adulto")
    return service

@pytest.fixture
def user_usecase(mock_user_repository, mock_user_domain_service):
    return UserUseCase(mock_user_repository, mock_user_domain_service)

@pytest.mark.asyncio
async def test_create_user_success(user_usecase, mock_user_repository, mock_user_domain_service):
    # Arrange
    request = CreateUserRequest(name="João Silva", email="joao@email.com", age=30)
    mock_user_repository.get_by_email.return_value = None
    mock_user_repository.create.return_value = User(
        id="123", name="João Silva", email="joao@email.com", age=30
    )

    # Act
    result = await user_usecase.create_user(request)

    # Assert
    assert result.success is True
    assert result.user.name == "João Silva"
    assert result.user.email == "joao@email.com"
    assert result.user.age == 30
    mock_user_domain_service.validate_user_creation.assert_called_once()
    mock_user_domain_service.welcome_new_user.assert_called_once()

@pytest.mark.asyncio
async def test_create_user_email_already_exists(user_usecase, mock_user_repository):
    # Arrange
    request = CreateUserRequest(name="João Silva", email="joao@email.com", age=30)
    mock_user_repository.get_by_email.return_value = User(
        id="456", name="Outro João", email="joao@email.com", age=25
    )

    # Act
    result = await user_usecase.create_user(request)

    # Assert
    assert result.success is False
    assert "Email já está em uso" in result.message
    assert result.user is None

@pytest.mark.asyncio
async def test_create_user_invalid_data():
    # Arrange
    request = CreateUserRequest(name="", email="invalid-email", age=-5)

    # Act
    is_valid, errors = request.validate()

    # Assert
    assert is_valid is False
    assert len(errors) > 0
    assert any("Nome" in error for error in errors)
    assert any("Email" in error for error in errors)
    assert any("Idade" in error for error in errors)

# Teste de integração simples
@pytest.mark.asyncio
async def test_user_domain_service_validation():
    from src.domain.services.user_service import UserDomainService
    from src.infrastructure.services.email_service import MockEmailService

    # Arrange
    email_service = MockEmailService()
    domain_service = UserDomainService(email_service)
    user = User(name="João", email="joao@email.com", age=30)

    # Act
    is_valid, errors = domain_service.validate_user_creation(user)

    # Assert
    assert is_valid is True
    assert len(errors) == 0

def test_user_entity_business_rules():
    # Arrange & Act
    adult_user = User(name="João", email="joao@email.com", age=25)
    minor_user = User(name="Maria", email="maria@email.com", age=16)

    # Assert
    assert adult_user.is_adult() is True
    assert minor_user.is_adult() is False
    assert adult_user.is_valid_email() is True
```

## Execução

### 1. Configuração Inicial

```bash
# 1. Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Verificar estrutura do projeto
mkdir -p src/{domain/{entities,repositories,services},application/{usecases,dtos},infrastructure/{database,repositories,services},presentation/{controllers,dependencies,dtos},config}
touch src/__init__.py
# ... criar todos os arquivos conforme estrutura
```

### 2. Executar a Aplicação

```bash
# Desenvolvimento
python src/main.py

# Ou usando uvicorn diretamente
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Produção
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 3. Executar Testes

```bash
# Instalar dependências de teste
pip install pytest pytest-asyncio httpx

# Executar todos os testes
pytest

# Executar com cobertura
pip install pytest-cov
pytest --cov=src --cov-report=html

# Executar testes específicos
pytest tests/test_user_usecase.py -v
```

### 4. Testar a API

```bash
# Health check
curl "http://localhost:8000/health"

# Criar usuário
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao@email.com",
    "age": 30
  }'

# Listar usuários
curl "http://localhost:8000/api/v1/users/?skip=0&limit=10"

# Buscar usuário por ID
curl "http://localhost:8000/api/v1/users/{user_id}"

# Buscar usuário por email
curl "http://localhost:8000/api/v1/users/email/joao@email.com"

# Atualizar usuário
curl -X PUT "http://localhost:8000/api/v1/users/{user_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Santos",
    "age": 31
  }'

# Verificar permissões
curl -X POST "http://localhost:8000/api/v1/users/{user_id}/permissions" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "purchase"
  }'

# Deletar usuário
curl -X DELETE "http://localhost:8000/api/v1/users/{user_id}"
```

### 5. Documentação da API

Acesse a documentação interativa:

-   **Swagger UI**: http://localhost:8000/docs
-   **ReDoc**: http://localhost:8000/redoc
-   **OpenAPI JSON**: http://localhost:8000/openapi.json

### 6. Estrutura de Arquivos Final

```
projeto/
├── src/
│   ├── domain/                      # ❌ SEM decorators/frameworks
│   │   ├── entities/
│   │   │   ├── __init__.py
│   │   │   └── user.py             # Entidade pura
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   └── user_repository.py   # Interface/Port
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── user_service.py     # Serviços de domínio
│   │   └── __init__.py
│   ├── application/                 # ❌ SEM decorators/frameworks
│   │   ├── usecases/
│   │   │   ├── __init__.py
│   │   │   └── user_usecase.py     # Casos de uso
│   │   ├── dtos/
│   │   │   ├── __init__.py
│   │   │   └── user_dto.py         # DTOs puros
│   │   └── __init__.py
│   ├── infrastructure/              # ✅ Pode ter dependências externas
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── connection.py
│   │   │   └── models.py
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   └── sqlite_user_repository.py  # Adapter
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── email_service.py
│   │   └── __init__.py
│   ├── presentation/                # ✅ Pode ter decorators FastAPI
│   │   ├── controllers/
│   │   │   ├── __init__.py
│   │   │   └── user_controller.py  # Controllers com decorators
│   │   ├── dependencies/
│   │   │   ├── __init__.py
│   │   │   └── container.py        # DI Container
│   │   ├── dtos/
│   │   │   ├── __init__.py
│   │   │   └── fastapi_user_dto.py # DTOs com Pydantic
│   │   └── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   ├── test_user_usecase.py
│   └── test_user_entity.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## Conceitos Demonstrados - Resumo

### ✅ **Desacoplamento Tecnológico**

**Camadas SEM decorators/frameworks:**

-   **Domain**: Entidades e serviços puros em Python
-   **Application**: Casos de uso e DTOs independentes

**Camadas COM decorators/frameworks:**

-   **Infrastructure**: Implementações específicas (SQLite, email)
-   **Presentation**: Controllers FastAPI com decorators

### ✅ **Arquitetura Hexagonal Completa**

1. **Núcleo (Domain + Application)**: Independente de tecnologia
2. **Ports**: Interfaces que definem contratos
3. **Adapters**: Implementações concretas na infraestrutura
4. **Presentation**: Interface HTTP com FastAPI

### ✅ **Princípios SOLID Aplicados**

-   **S**: Cada classe tem responsabilidade única
-   **O**: Extensível via interfaces
-   **L**: Implementações substituíveis
-   **I**: Interfaces segregadas e específicas
-   **D**: Dependências invertidas através de abstrações

### ✅ **Design Patterns Implementados**

-   **Repository**: Abstração de persistência
-   **Factory**: Container de dependências
-   **Strategy**: Diferentes serviços de notificação
-   **Adapter**: Conversão entre camadas
-   **Observer**: Eventos de domínio

### ✅ **Benefícios da Arquitetura**

1. **Testabilidade**: Fácil mock das dependências
2. **Manutenibilidade**: Código organizado e limpo
3. **Flexibilidade**: Troca de tecnologias sem impacto
4. **Reutilização**: Lógica independente de interface
5. **Escalabilidade**: Base sólida para crescimento
6. **Qualidade**: Código seguindo melhores práticas

Esta implementação demonstra como manter as camadas internas (domain e application) completamente livres de dependências de frameworks, enquanto as camadas externas (infrastructure e presentation) podem utilizar tecnologias específicas como FastAPI, SQLite, etc. Isso garante que as regras de negócio permaneçam puras e testáveis, seguindo os princípios da Clean Architecture.

### 5. Application Layer - Use Cases

**src/application/usecases/user_usecase.py**

```python
from typing import List, Optional
from ..dtos.user_dto import (
    CreateUserRequest, UpdateUserRequest, UserResponse,
    PaginatedUsersResponse, UserOperationResult, OperationResult
)
from ...domain.entities.user import User
from ...domain.repositories.user_repository import UserRepository
from ...domain.services.user_service import UserDomainService

class UserUseCase:
    """
    Casos de uso para operações com usuários.
    Implementa a lógica de aplicação seguindo o padrão Command.
    IMPORTANTE: Esta classe não possui decorators ou dependências de frameworks.
    """

    def __init__(self, user_repository: UserRepository, user_domain_service: UserDomainService):
        self._user_repository = user_repository
        self._user_domain_service = user_domain_service

    async def create_user(self, request: CreateUserRequest) -> UserOperationResult:
        """Caso de uso: Criar usuário"""
        try:
            # Valida dados de entrada
            is_valid, validation_errors = request.validate()
            if not is_valid:
                return UserOperationResult.error_result(
                    "Dados de entrada inválidos",
                    validation_errors
                )

            # Verifica se email já existe
            existing_user = await self._user_repository.get_by_email(request.email)
            if existing_user:
                return UserOperationResult.error_result(
                    "Email já está em uso",
                    ["Um usuário com este email já existe"]
                )

            # Cria entidade de domínio
            user = User(
                name=request.name.strip(),
                email=request.email.lower().strip(),
                age=request.age
            )

            # Aplica validações de domínio
            is_domain_valid, domain_errors = self._user_domain_service.validate_user_creation(user)
            if not is_domain_valid:
                return UserOperationResult.error_result(
                    "Falha na validação de domínio",
                    domain_errors
                )

            # Persiste o usuário
            created_user = await self._user_repository.create(user)

            # Calcula categoria do usuário
            category = self._user_domain_service.calculate_user_category(created_user)

            # Cria resposta
            user_response = UserResponse.from_domain(created_user, category)

            # Envia boas-vindas (padrão Observer)
            await self._user_domain_service.welcome_new_user(created_user)

            return UserOperationResult.success_with_user(
                user_response,
                "Usuário criado com sucesso"
            )

        except Exception as e:
            return UserOperationResult.error_result(
                "Erro interno ao criar usuário",
                [str(e)]
            )

    async def get_user_by_id(self, user_id: str) -> UserOperationResult:
        """Caso de uso: Buscar usuário por ID"""
        try:
            if not user_id or not isinstance(user_id, str):
                return UserOperationResult.error_result(
                    "ID do usuário é obrigatório",
                    ["ID deve ser uma string não vazia"]
                )

            user = await self._user_repository.get_by_id(user_id.strip())
            if not user:
                return UserOperationResult.error_result(
                    "Usuário não encontrado",
                    [f"Nenhum usuário encontrado com ID: {user_id}"]
                )

            category = self._user_domain_service.calculate_user_category(user)
            user_response = UserResponse.from_domain(user, category)

            return UserOperationResult.success_with_user(
                user_response,
                "Usuário encontrado"
            )

        except Exception as e:
            return UserOperationResult.error_result(
                "Erro interno ao buscar usuário",
                [str(e)]
            )

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> tuple[bool, str, PaginatedUsersResponse]:
        """Caso de uso: Listar usuários com paginação"""
        try:
            # Valida parâmetros de paginação
            if skip < 0:
                return False, "Skip deve ser >= 0", None
            if limit < 1 or limit > 1000:
                return False, "Limit deve estar entre 1 e 1000", None

            # Busca usuários
            users = await self._user_repository.get_all(skip, limit)

            # Converte para DTOs
            user_responses = []
            for user in users:
                category = self._user_domain_service.calculate_user_category(user)
                user_response = UserResponse.from_domain(user, category)
                user_responses.append(user_response)

            # Calcula total (simplificado - em produção usar count otimizado)
            all_users = await self._user_repository.get_all(0, 999999)
            total = len(all_users)

            # Cria resposta paginada
            paginated_response = PaginatedUsersResponse.create(
                users=user_responses,
                total=total,
                skip=skip,
                limit=limit
            )

            return True, "Usuários listados com sucesso", paginated_response

        except Exception as e:
            return False, f"Erro interno ao listar usuários: {str(e)}", None

    async def update_user(self, user_id: str, request: UpdateUserRequest) -> UserOperationResult:
        """Caso de uso: Atualizar usuário"""
        try:
            # Valida parâmetros
            if not user_id or not isinstance(user_id, str):
                return UserOperationResult.error_result(
                    "ID do usuário é obrigatório",
                    ["ID deve ser uma string não vazia"]
                )

            # Valida dados de entrada
            is_valid, validation_errors = request.validate()
            if not is_valid:
                return UserOperationResult.error_result(
                    "Dados de entrada inválidos",
                    validation_errors
                )

            # Verifica se há atualizações
            if not request.has_updates():
                return UserOperationResult.error_result(
                    "Nenhum campo para atualizar",
                    ["Pelo menos um campo deve ser fornecido para atualização"]
                )

            # Busca usuário existente
            user = await self._user_repository.get_by_id(user_id.strip())
            if not user:
                return UserOperationResult.error_result(
                    "Usuário não encontrado",
                    [f"Nenhum usuário encontrado com ID: {user_id}"]
                )

            # Verifica se novo email já existe (se fornecido)
            if request.email and request.email.lower().strip() != user.email.lower():
                existing_user = await self._user_repository.get_by_email(request.email.lower().strip())
                if existing_user:
                    return UserOperationResult.error_result(
                        "Email já está em uso",
                        ["Um usuário com este email já existe"]
                    )

            # Atualiza dados do usuário
            user.update_info(
                name=request.name.strip() if request.name else None,
                email=request.email.lower().strip() if request.email else None,
                age=request.age
            )

            # Valida usuário atualizado
            current_data = {"id": user_id}
            is_domain_valid, domain_errors = self._user_domain_service.validate_user_update(user, current_data)
            if not is_domain_valid:
                return UserOperationResult.error_result(
                    "Falha na validação de domínio",
                    domain_errors
                )

            # Persiste as alterações
            updated_user = await self._user_repository.update(user)

            # Calcula categoria atualizada
            category = self._user_domain_service.calculate_user_category(updated_user)
            user_response = UserResponse.from_domain(updated_user, category)

            return UserOperationResult.success_with_user(
                user_response,
                "Usuário atualizado com sucesso"
            )

        except Exception as e:
            return UserOperationResult.error_result(
                "Erro interno ao atualizar usuário",
                [str(e)]
            )

    async def delete_user(self, user_id: str) -> OperationResult:
        """Caso de uso: Deletar usuário"""
        try:
            if not user_id or not isinstance(user_id, str):
                return OperationResult.error_result(
                    "ID do usuário é obrigatório",
                    ["ID deve ser uma string não vazia"]
                )

            # Verifica se usuário existe antes de deletar
            existing_user = await self._user_repository.get_by_id(user_id.strip())
            if not existing_user:
                return OperationResult.error_result(
                    "Usuário não encontrado",
                    [f"Nenhum usuário encontrado com ID: {user_id}"]
                )

            # Executa a deleção
            success = await self._user_repository.delete(user_id.strip())

            if success:
                return OperationResult.success_result("Usuário deletado com sucesso")
            else:
                return OperationResult.error_result(
                    "Falha ao deletar usuário",
                    ["Não foi possível deletar o usuário"]
                )

        except Exception as e:
            return OperationResult.error_result(
                "Erro interno ao deletar usuário",
                [str(e)]
            )

    async def get_user_by_email(self, email: str) -> UserOperationResult:
        """Caso de uso: Buscar usuário por email"""
        try:
            if not email or not isinstance(email, str):
                return UserOperationResult.error_result(
                    "Email é obrigatório",
                    ["Email deve ser uma string não vazia"]
                )

            user = await self._user_repository.get_by_email(email.lower().strip())
            if not user:
                return UserOperationResult.error_result(
                    "Usuário não encontrado",
                    [f"Nenhum usuário encontrado com email: {email}"]
                )

            category = self._user_domain_service.calculate_user_category(user)
            user_response = UserResponse.from_domain(user, category)

            return UserOperationResult.success_with_user(
                user_response,
                "Usuário encontrado"
            )

        except Exception as e:
            return UserOperationResult.error_result(
                "Erro interno ao buscar usuário por email",
                [str(e)]
            )

    async def check_user_permissions(self, user_id: str, action: str) -> tuple[bool, str, bool]:
        """Caso de uso: Verificar permissões do usuário para uma ação"""
        try:
            if not user_id or not action:
                return False, "ID do usuário e ação são obrigatórios", False

            user = await self._user_repository.get_by_id(user_id.strip())
            if not user:
                return False, "Usuário não encontrado", False

            can_perform = self._user_domain_service.can_user_perform_action(user, action.lower())

            message = f"Usuário {'pode' if can_perform else 'não pode'} realizar a ação: {action}"
            return True, message, can_perform

        except Exception as e:
            return False, f"Erro ao verificar permissões: {str(e)}", False
```

# Adiiconais:

O que é `pytest-bdd`, `behave` ou `Gherkin` para escrever os testes em arquivos `.feature`.

Claro! Aqui vai uma explicação **objetiva e simples**:

---

### ✅ `Gherkin`

-   Linguagem **simples e legível** usada para escrever **cenários de teste BDD**.
-   Usa palavras-chave como `Given`, `When`, `Then`.

**Exemplo:**

```gherkin
Scenario: Verificar se usuário é adulto
  Given um usuário com 20 anos
  When eu verificar se ele é adulto
  Then o resultado deve ser verdadeiro
```

---

### ✅ `behave`

-   Framework Python que **executa arquivos `.feature`** escritos em Gherkin.
-   Usa funções Python para implementar cada passo (`step`) do cenário.

---

### ✅ `pytest-bdd`

-   Extensão do `pytest` que permite usar arquivos `.feature` com Gherkin.
-   Mesma ideia do `behave`, mas **integrado ao pytest**.

---

### 🔁 Diferença principal:

| Ferramenta | Base      | Usa `.feature`? | Integra com `pytest`? |
| ---------- | --------- | --------------- | --------------------- |
| Gherkin    | Linguagem | ✅ Sim          | —                     |
| behave     | Próprio   | ✅ Sim          | ❌ Não                |
| pytest-bdd | pytest    | ✅ Sim          | ✅ Sim                |
