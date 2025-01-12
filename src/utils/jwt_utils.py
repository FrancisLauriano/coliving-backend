# utils/jwt_utils.py:
import jwt
import os
from datetime import datetime, timedelta
from errors.custom_errors import UnauthorizedError, InvalidTokenError
import logging

logger = logging.getLogger(__name__)

class JWTUtils:
    """
    Utilitário para criar e validar tokens JWT.
    """
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret_key")
    ACCESS_EXPIRATION = int(os.getenv("ACCESS_EXPIRATION", 60))  # Expiração em minutos
    RENEWAL_THRESHOLD = int(os.getenv("RENEWAL_THRESHOLD", 5))  # Renovação automática antes de expirar

    @staticmethod
    def create_token(data, expires_in=None):
        """
        Gera um token JWT com os dados fornecidos.
        """
        try:
            expiration = datetime.utcnow() + timedelta(minutes=expires_in or JWTUtils.ACCESS_EXPIRATION)
            token = jwt.encode({'data': data, 'exp': expiration}, JWTUtils.SECRET_KEY, algorithm="HS256")
            logger.info("Token JWT criado com sucesso.")
            return token
        except Exception as e:
            logger.error(f"Erro ao criar token JWT: {e}")
            raise UnauthorizedError("Erro ao criar token JWT.")

    @staticmethod
    def decode_token(token):
        """
        Decodifica e valida um token JWT.
        """
        try:
            payload = jwt.decode(token, JWTUtils.SECRET_KEY, algorithms=["HS256"])
            expiration = datetime.fromtimestamp(payload['exp'])
            if (expiration - datetime.utcnow()).total_seconds() < JWTUtils.RENEWAL_THRESHOLD * 60:
                new_token = JWTUtils.create_token(payload["data"])
                payload["new_token"] = new_token
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token expirado.")
            raise UnauthorizedError("Token expirado.")
        except jwt.InvalidTokenError:
            logger.error("Token inválido.")
            raise InvalidTokenError("Token inválido.")
        except Exception as e:
            logger.error(f"Erro ao decodificar token JWT: {e}")
            raise UnauthorizedError("Erro ao validar token JWT.")
