# services/auth_service.py:
import logging
from utils.jwt_utils import JWTUtils
from utils.encryption_utils import EncryptionUtils
from repositories.person_repository import PersonRepository
from validators.person_validator import PersonSchema
from errors.custom_errors import UnauthorizedError, ValidationError, NotFoundError, InternalServerError
from marshmallow.exceptions import ValidationError as MarshmallowValidationError

logger = logging.getLogger(__name__)

class AuthService:
    """
    Serviço para autenticação e gerenciamento de usuários.
    Responsável por login, validação e renovação de tokens JWT.
    """

    def __init__(self):
        self.encryption = EncryptionUtils()
        self.schema = PersonSchema()

    def login(self, data):
        """
        Autentica um usuário e retorna um token JWT.

        Args:
            data (dict): Dados de login contendo email e senha.

        Returns:
            dict: Dicionário contendo o token JWT e os dados do usuário.
        """
        try:
            if not data or not isinstance(data, dict):
                raise ValidationError(field="data", message="Dados de login inválidos.")

            email = data.get("email", "").strip().lower()
            password = data.get("password", "").strip()

            if not email:
                raise ValidationError(field="email", message="O campo 'email' é obrigatório.")
            if not password:
                raise ValidationError(field="password", message="O campo 'password' é obrigatório.")

            # Buscar o usuário pelo email
            user = PersonRepository.get_by_email(email)
            if not user:
                logger.warning(f"Usuário não encontrado: {email}")
                raise UnauthorizedError("E-mail ou senha inválidos.")

            # Verificar a senha
            decrypted_password = self.encryption.decrypt(user.password)
            if decrypted_password != password:
                logger.warning(f"Senha inválida para o usuário: {email}")
                raise UnauthorizedError("E-mail ou senha inválidos.")

            # Gerar o token JWT
            token = JWTUtils.create_token({"id": str(user.id), "email": user.email, "person_type": user.person_type})
            logger.info(f"Usuário autenticado com sucesso: {email}")

            return {
                "token": token,
                "user": {
                    "id": str(user.id),
                    "name": user.name,
                    "email": user.email,
                    "person_type": user.person_type
                }
            }

        except ValidationError as err:
            logger.warning(f"Erro de validação ao autenticar: {err}")
            raise
        except UnauthorizedError as err:
            logger.warning(f"Erro de autorização: {err}")
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao autenticar usuário: {e}")
            raise InternalServerError("Erro ao realizar login.")

    def validate_token(self, token):
        """
        Valida um token JWT e retorna os dados do usuário autenticado.

        Args:
            token (str): Token JWT.

        Returns:
            dict: Dados do usuário autenticado.
        """
        try:
            token_data = JWTUtils.decode_token(token)
            user_id = token_data["data"]["id"]

            # Buscar o usuário pelo ID
            user = PersonRepository.get_by_id(user_id)
            if not user:
                logger.warning("Usuário associado ao token não encontrado.")
                raise NotFoundError(resource="Person", message="Usuário associado ao token não encontrado.")

            return {
                "id": str(user.id),
                "name": user.name,
                "email": user.email,
                "person_type": user.person_type
            }

        except ValidationError as err:
            logger.warning(f"Erro de validação no token: {err}")
            raise
        except NotFoundError as err:
            logger.warning(f"Erro ao encontrar usuário: {err}")
            raise
        except Exception as e:
            logger.error(f"Erro ao validar token: {e}")
            raise UnauthorizedError("Erro ao validar token.")

    def refresh_token(self, token):
        """
        Gera um novo token JWT antes que o atual expire.

        Args:
            token (str): Token JWT atual.

        Returns:
            dict: Novo token JWT e os dados do usuário.
        """
        try:
            token_data = JWTUtils.decode_token(token)
            user_id = token_data["data"]["id"]

            # Buscar o usuário pelo ID
            user = PersonRepository.get_by_id(user_id)
            if not user:
                logger.warning("Usuário associado ao token não encontrado.")
                raise NotFoundError(resource="Person", message="Usuário associado ao token não encontrado.")

            # Gerar um novo token
            new_token = JWTUtils.create_token({"id": str(user.id), "email": user.email, "person_type": user.person_type})
            logger.info(f"Token renovado com sucesso para o usuário: {user.email}")

            return {
                "new_token": new_token,
                "user": {
                    "id": str(user.id),
                    "name": user.name,
                    "email": user.email,
                    "person_type": user.person_type
                }
            }

        except ValidationError as err:
            logger.warning(f"Erro de validação no token: {err}")
            raise
        except NotFoundError as err:
            logger.warning(f"Erro ao encontrar usuário: {err}")
            raise
        except Exception as e:
            logger.error(f"Erro ao renovar token: {e}")
            raise UnauthorizedError("Erro ao renovar token.")
