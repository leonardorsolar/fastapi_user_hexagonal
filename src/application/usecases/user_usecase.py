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