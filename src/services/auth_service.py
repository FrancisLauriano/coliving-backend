# services/auth_service.py:

import logging
from utils.jwt_utils import JWTUtils
from utils.encryption_utils import EncryptionUtils
from repositories.person_repository import PersonRepository
from validators.person_validator import PersonValidator
from errors.custom_errors import UnauthorizedError, ValidationError, NotFoundError

logger = logging.getLogger(__name__)

class AuthService:
    """
    Serviço para autenticação e gerenciamento de usuários.
    Responsável por login e verificação de credenciais.
    """

    @staticmethod
    def login(data):
        """
        Autentica um usuário e retorna um token JWT.

        Args:
            data (dict): Dados de login contendo email e senha.

        Returns:
            dict: Dicionário contendo o token JWT e os dados do usuário.
        """
        try:
            # Validar dados de entrada
            validator = PersonValidator()
            validated_data = validator.validate_and_load({
                "email": data.get("email"),
                "password": data.get("password")
            })

            email = validated_data.get("email")
            password = validated_data.get("password")

            # Buscar o usuário pelo email
            user = PersonRepository.get_all()
            user = next((u for u in user if u.email == email), None)

            if not user:
                logger.warning(f"Usuário não encontrado: {email}")
                raise NotFoundError(resource="Person", message="Usuário ou senha inválidos.")

            # Verificar a senha
            encryption = EncryptionUtils()
            if not encryption.decrypt(user.password) == password:
                logger.warning(f"Senha inválida para o usuário: {email}")
                raise UnauthorizedError("Usuário ou senha inválidos.")

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

        except ValidationError as e:
            logger.warning(f"Erro de validação ao autenticar: {e}")
            raise e
        except NotFoundError as e:
            logger.warning(f"Erro ao encontrar usuário: {e}")
            raise e
        except Exception as e:
            logger.error(f"Erro ao autenticar usuário: {e}")
            raise UnauthorizedError("Erro ao realizar login.")

    @staticmethod
    def validate_token(token):
        """
        Valida um token JWT e retorna os dados do usuário autenticado.

        Args:
            token (str): Token JWT.

        Returns:
            dict: Dados do usuário autenticado.
        """
        try:
            token_data = JWTUtils.decode_token(token)
            user = PersonRepository.get_by_id(token_data["data"]["id"])

            if not user:
                logger.warning("Usuário associado ao token não encontrado.")
                raise NotFoundError(resource="Person", message="Usuário associado ao token não encontrado.")

            return {
                "id": str(user.id),
                "name": user.name,
                "email": user.email,
                "person_type": user.person_type
            }

        except UnauthorizedError as e:
            logger.warning(f"Erro de autorização: {e}")
            raise e
        except Exception as e:
            logger.error(f"Erro ao validar token: {e}")
            raise UnauthorizedError("Erro ao validar token.")

    @staticmethod
    def refresh_token(token):
        """
        Gera um novo token JWT antes que o atual expire.

        Args:
            token (str): Token JWT atual.

        Returns:
            dict: Novo token JWT e os dados do usuário.
        """
        try:
            # Decodificar o token e verificar renovação
            token_data = JWTUtils.decode_token(token)
            new_token = token_data.get("new_token")

            user = PersonRepository.get_by_id(token_data["data"]["id"])
            if not user:
                logger.warning("Usuário associado ao token não encontrado.")
                raise NotFoundError(resource="Person", message="Usuário associado ao token não encontrado.")

            return {
                "new_token": new_token,
                "user": {
                    "id": str(user.id),
                    "name": user.name,
                    "email": user.email,
                    "person_type": user.person_type
                }
            }

        except UnauthorizedError as e:
            logger.warning(f"Erro ao renovar token: {e}")
            raise e
        except Exception as e:
            logger.error(f"Erro ao renovar token: {e}")
            raise UnauthorizedError("Erro ao renovar token.")
