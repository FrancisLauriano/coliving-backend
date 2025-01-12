# app/errors/custom_errors.py:
class AppError(Exception):
    """Classe base para erros personalizados na aplicação."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ValidationError(AppError):
    """Erro para validações de entrada."""
    def __init__(self, field, message="Invalid input"):
        self.field = field
        self.message = f"{message}: {field}"
        super().__init__(self.message)


class NotFoundError(AppError):
    """Erro para recursos não encontrados."""
    def __init__(self, resource, message="Resource not found"):
        self.resource = resource
        self.message = f"{message}: {resource}"
        super().__init__(self.message)


class UnauthorizedError(AppError):
    """Erro para acessos não autorizados."""
    def __init__(self, action="access", message="Unauthorized access"):
        self.action = action
        self.message = f"{message} for {action}"
        super().__init__(self.message)


class ExternalAPIError(AppError):
    """Erro para falhas em chamadas de APIs externas."""
    def __init__(self, service, message="Failed to connect to external service"):
        self.service = service
        self.message = f"{message}: {service}"
        super().__init__(self.message)


class ConflictError(AppError):
    """Erro para conflitos, como duplicidade de dados."""
    def __init__(self, resource, message="Conflict"):
        self.resource = resource
        self.message = f"{message}: {resource} already exists"
        super().__init__(self.message)


class InternalServerError(AppError):
    """Erro para falhas internas do servidor."""
    def __init__(self, message="Internal server error"):
        self.message = message
        super().__init__(self.message)


class InvalidTokenError(AppError):
    """Erro para tokens inválidos."""
    def __init__(self, message="Token inválido"):
        super().__init__(message)        