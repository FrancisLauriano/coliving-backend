# utils/encryption_utils.py:
import os
from cryptography.fernet import Fernet
from errors.custom_errors import InternalServerError, ValidationError
import logging

logger = logging.getLogger(__name__)

class EncryptionUtils:
    """
    Utilitário para criptografia e descriptografia de dados.
    """
    def __init__(self):
        self.key = os.getenv("ENCRYPTION_KEY")
        if not self.key:
            logger.error("Chave de criptografia não encontrada.")
            raise InternalServerError("Chave de criptografia não encontrada.")
        self.cipher = Fernet(self.key.encode())

    def encrypt(self, data):
        """
        Criptografa uma string usando a chave de criptografia.
        """
        try:
            encrypted_data = self.cipher.encrypt(data.encode())
            logger.info("Dados criptografados com sucesso.")
            return encrypted_data.decode()
        except Exception as e:
            logger.error(f"Erro ao criptografar os dados: {e}")
            raise InternalServerError("Erro ao criptografar os dados.")

    def decrypt(self, encrypted_data):
        """
        Descriptografa uma string criptografada.
        """
        try:
            decrypted_data = self.cipher.decrypt(encrypted_data.encode()).decode()
            logger.info("Dados descriptografados com sucesso.")
            return decrypted_data
        except Exception as e:
            logger.error(f"Erro ao descriptografar os dados: {e}")
            raise ValidationError(field="data", message="Dados criptografados inválidos.")
