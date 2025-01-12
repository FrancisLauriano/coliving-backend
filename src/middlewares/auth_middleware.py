# middlewares/auth_middleware.py:
import logging
from functools import wraps
from flask import request, jsonify, g
from utils.jwt_utils import JWTUtils
from repositories.person_repository import PersonRepository
from errors.custom_errors import UnauthorizedError, InvalidTokenError
from errors.error_handler import ErrorHandler

logger = logging.getLogger(__name__)

def jwt_required(f):
    """
    Middleware para validar a presença e validade do token JWT.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            logger.warning("Token ausente na requisição.")
            return ErrorHandler.handle_unauthorized_error(UnauthorizedError("Token é obrigatório."))

        try:
            # Verifica se o token está no formato correto: Bearer <token>
            parts = token.split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                token = parts[1]
            else:
                logger.warning("Formato de token inválido.")
                raise InvalidTokenError("Formato de token inválido. Use o formato 'Bearer <token>'.")

            # Decodifica o token e busca o usuário no banco de dados
            token_data = JWTUtils.decode_token(token)
            g.current_user = PersonRepository.get_by_id(token_data["data"]["id"])
            if not g.current_user:
                logger.warning("Usuário associado ao token não encontrado.")
                raise UnauthorizedError("Usuário não encontrado.")

            # Adiciona um novo token no contexto se o atual estiver próximo de expirar
            if "new_token" in token_data:
                g.new_token = token_data["new_token"]

        except UnauthorizedError as e:
            logger.warning(f"Erro de autorização: {e}")
            return ErrorHandler.handle_unauthorized_error(e)
        except InvalidTokenError as e:
            logger.error(f"Token inválido: {e}")
            return ErrorHandler.handle_invalid_token_error(e)

        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    """
    Middleware para limitar o acesso aos administradores.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if not g.current_user or g.current_user.person_type != "admin":
            logger.warning("Acesso não autorizado - Usuário não é administrador.")
            return ErrorHandler.handle_unauthorized_error(UnauthorizedError("Acesso restrito aos administradores."))
        return f(*args, **kwargs)
    return decorated
