# controllers/auth_controller:
import logging
from flask import request, jsonify
from services.auth_service import AuthService
from errors.error_handler import ErrorHandler
from errors.custom_errors import UnauthorizedError, ValidationError, NotFoundError

logger = logging.getLogger(__name__)

class AuthController:
    """
    Controlador para autenticação de usuários.
    """

    @staticmethod
    def login():
        """
        Realiza login do usuário e retorna um token JWT.
        """
        try:
            data = request.get_json()
            if not data or not isinstance(data, dict):
                raise ValidationError(field="data", message="Dados de entrada inválidos.")

            result = AuthService.login(data)
            logger.info("Login realizado com sucesso.")
            return jsonify(result), 200
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except UnauthorizedError as e:
            return ErrorHandler.handle_unauthorized_error(e)
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            logger.error("Erro inesperado ao realizar login.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def validate_token():
        """
        Valida o token JWT e retorna os dados do usuário autenticado.
        """
        try:
            token = request.headers.get("Authorization")
            if not token or not token.startswith("Bearer "):
                raise ValidationError(field="token", message="Token de autenticação inválido ou ausente.")

            token = token.split(" ")[1]  # Extrai o token do formato "Bearer <token>"
            user_data = AuthService.validate_token(token)
            logger.info("Token validado com sucesso.")
            return jsonify(user_data), 200
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except UnauthorizedError as e:
            return ErrorHandler.handle_unauthorized_error(e)
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            logger.error("Erro inesperado ao validar token.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def refresh_token():
        """
        Gera um novo token JWT baseado no token atual.
        """
        try:
            token = request.headers.get("Authorization")
            if not token or not token.startswith("Bearer "):
                raise ValidationError(field="token", message="Token de autenticação inválido ou ausente.")

            token = token.split(" ")[1]  # Extrai o token do formato "Bearer <token>"
            result = AuthService.refresh_token(token)
            logger.info("Token renovado com sucesso.")
            return jsonify(result), 200
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except UnauthorizedError as e:
            return ErrorHandler.handle_unauthorized_error(e)
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            logger.error("Erro inesperado ao renovar token.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)
