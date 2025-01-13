# utils/encryption_utils.py:
import base64
import os
from cryptography.fernet import Fernet, InvalidToken
from errors.custom_errors import InternalServerError, ValidationError

class EncryptionUtils:
    def __init__(self):
        self.key = os.getenv("ENCRYPTION_KEY")
        if not self.key:
            raise InternalServerError("Chave de criptografia não encontrada no ambiente.")
        try:
            # Corrigir o padding da chave
            padded_key = self.key + '=' * (-len(self.key) % 4)

            # Validar se a chave decodificada tem 32 bytes
            decoded_key = base64.urlsafe_b64decode(padded_key.encode())
            if len(decoded_key) != 32:
                raise ValueError("A chave deve ter exatamente 32 bytes após decodificação.")
            
            # Inicializar o objeto Fernet
            self.cipher = Fernet(padded_key)
        except Exception as e:
            raise InternalServerError(f"Chave de criptografia inválida. Certifique-se de que ela está no formato correto: {e}")

    def encrypt(self, data):
        try:
            encrypted_data = self.cipher.encrypt(data.encode())
            return encrypted_data.decode()
        except Exception as e:
            raise InternalServerError(f"Erro ao criptografar os dados: {e}")

    def decrypt(self, encrypted_data):
        try:
            decrypted_data = self.cipher.decrypt(encrypted_data.encode()).decode()
            return decrypted_data
        except InvalidToken:
            raise ValidationError(field="data", message="Dados criptografados inválidos ou corrompidos.")
        except Exception as e:
            raise InternalServerError(f"Erro ao descriptografar os dados: {e}")
