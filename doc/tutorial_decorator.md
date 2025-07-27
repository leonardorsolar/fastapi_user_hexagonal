# Tutorial FastAPI com decorator- Arquitetura Hexagonal com SOLID e Design Patterns

## Sumário

1. [Introdução](#introdução)
2. [Estrutura do Projeto](#estrutura-do-projeto)
3. [Conceitos Aplicados](#conceitos-aplicados)
4. [Implementação](#implementação)
5. [Execução](#execução)

## Introdução

Este tutorial demonstra como criar uma API REST com FastAPI seguindo os princípios SOLID, padrões de design, injeção de dependência e arquitetura hexagonal. Vamos construir um sistema de gerenciamento de usuários completo.

### Conceitos Abordados

-   **Arquitetura Hexagonal (Ports & Adapters)**
-   **Princípios SOLID**
-   **Injeção e Inversão de Dependências**
-   **Design Patterns**: Repository, Factory, Strategy, Observer
-   **Clean Architecture**
-   **Domain-Driven Design (DDD)**

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

### 1. Domain Layer - Entidades

**src/domain/entities/user.py**

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

    def update_info(self, name: str = None, email: str = None, age: int = None):
        """Atualiza informações do usuário mantendo a data de atualização"""
        if name:
            self.name = name
        if email:
            self.email = email
        if age is not None:
            self.age = age
        self.updated_at = datetime.utcnow()
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
    """Interface para serviços de notificação"""

    @abstractmethod
    async def send_welcome_email(self, user: User) -> bool:
        pass

class UserDomainService:
    """
    Serviço de domínio para regras complexas que envolvem múltiplas entidades.
    Implementa o padrão Strategy para diferentes tipos de validação.
    """

    def __init__(self, notification_service: NotificationService):
        self._notification_service = notification_service

    async def validate_user_creation(self, user: User) -> bool:
        """Valida se um usuário pode ser criado"""
        if not user.name or len(user.name.strip()) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres")

        if not user.email or "@" not in user.email:
            raise ValueError("Email inválido")

        if user.age < 0 or user.age > 150:
            raise ValueError("Idade deve estar entre 0 e 150 anos")

        return True

    async def welcome_new_user(self, user: User) -> bool:
        """Envia boas-vindas para novo usuário"""
        return await self._notification_service.send_welcome_email(user)
```

### 4. Application Layer - DTOs

**src/application/dtos/user_dto.py**

```python
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class CreateUserRequest(BaseModel):
    """DTO para criação de usuário"""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=0, le=150)

class UpdateUserRequest(BaseModel):
    """DTO para atualização de usuário"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=0, le=150)

class UserResponse(BaseModel):
    """DTO para resposta de usuário"""
    id: str
    name: str
    email: str
    age: int
    is_adult: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginatedUsersResponse(BaseModel):
    """DTO para resposta paginada"""
    users: list[UserResponse]
    total: int
    skip: int
    limit: int
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

### 9. Presentation Layer - Dependency Container

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

### 10. Presentation Layer - Controller

**src/presentation/controllers/user_controller.py**

```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
from ...application.usecases.user_usecase import UserUseCase
from ...application.dtos.user_dto import (
    CreateUserRequest,
    UpdateUserRequest,
    UserResponse,
    PaginatedUsersResponse
)
from ..dependencies.container import get_user_usecase

class UserController:
    """
    Controlador REST para operações com usuários.
    Implementa o padrão MVC (Controller).
    """

    def __init__(self):
        self.router = APIRouter(prefix="/users", tags=["Users"])
        self._setup_routes()

    def _setup_routes(self):
        """Configura as rotas do controlador"""
        self.router.add_api_route(
            "/",
            self.create_user,
            methods=["POST"],
            response_model=UserResponse,
            status_code=status.HTTP_201_CREATED
        )

        self.router.add_api_route(
            "/",
            self.get_users,
            methods=["GET"],
            response_model=PaginatedUsersResponse
        )

        self.router.add_api_route(
            "/{user_id}",
            self.get_user,
            methods=["GET"],
            response_model=UserResponse
        )

        self.router.add_api_route(
            "/{user_id}",
            self.update_user,
            methods=["PUT"],
            response_model=UserResponse
        )

        self.router.add_api_route(
            "/{user_id}",
            self.delete_user,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT
        )

    async def create_user(
        self,
        request: CreateUserRequest,
        usecase: UserUseCase = Depends(get_user_usecase)
    ) -> UserResponse:
        """Endpoint para criar usuário"""
        try:
            return await usecase.create_user(request)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
            )

    async def get_users(
        self,
        skip: int = Query(0, ge=0, description="Itens a pular"),
        limit: int = Query(100, ge=1, le=1000, description="Limite de itens"),
        usecase: UserUseCase = Depends(get_user_usecase)
    ) -> PaginatedUsersResponse:
        """Endpoint para listar usuários"""
        try:
            return await usecase.get_all_users(skip, limit)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
            )

    async def get_user(
        self,
        user_id: str,
        usecase: UserUseCase = Depends(get_user_usecase)
    ) -> UserResponse:
        """Endpoint para buscar usuário por ID"""
        try:
            user = await usecase.get_user_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuário não encontrado"
                )
            return user
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
            )

    async def update_user(
        self,
        user_id: str,
        request: UpdateUserRequest,
        usecase: UserUseCase = Depends(get_user_usecase)
    ) -> UserResponse:
        """Endpoint para atualizar usuário"""
        try:
            user = await usecase.update_user(user_id, request)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuário não encontrado"
                )
            return user
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
            )

    async def delete_user(
        self,
        user_id: str,
        usecase: UserUseCase = Depends(get_user_usecase)
    ) -> None:
        """Endpoint para deletar usuário"""
        try:
            success = await usecase.delete_user(user_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuário não encontrado"
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
            )
```

### 11. Configuration

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

### 12. Main Application

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

### 13. Requirements

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
    service.validate_user_creation = AsyncMock()
    service.welcome_new_user = AsyncMock(return_value=True)
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
    assert result.name == "João Silva"
    assert result.email == "joao@email.com"
    assert result.age == 30
    mock_user_domain_service.validate_user_creation.assert_called_once()
    mock_user_domain_service.welcome_new_user.assert_called_once()

@pytest.mark.asyncio
async def test_create_user_email_already_exists(user_usecase, mock_user_repository):
    # Arrange
    request = CreateUserRequest(name="João Silva", email="joao@email.com", age=30)
    mock_user_repository.get_by_email.return_value = User(
        id="456", name="Outro João", email="joao@email.com", age=25
    )

    # Act & Assert
    with pytest.raises(ValueError, match="Email já está em uso"):
        await user_usecase.create_user(request)
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
