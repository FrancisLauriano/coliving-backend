# services/person_service.py:
import logging
import marshmallow
from repositories.person_repository import PersonRepository
from validators.person_validator import PersonSchema
from utils.encryption_utils import EncryptionUtils
from errors.custom_errors import NotFoundError, ConflictError, InternalServerError, ValidationError
from errors.error_handler import ErrorHandler

logger = logging.getLogger(__name__)

class PersonService:
    def __init__(self):
        self.encryption = EncryptionUtils()
        self.schema = PersonSchema()

    def _normalize_data(self, data):
        """Converte campos específicos para letras minúsculas."""
        for key in ['name', 'email', 'person_type']:
            if key in data and isinstance(data[key], str):
                data[key] = data[key].lower()
        return data

    def get_all(self):
        """Retorna todas as pessoas cadastradas."""
        try:
            people = PersonRepository.get_all()
            logger.info("Pessoas obtidas com sucesso.")
            return people
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar pessoas: {e}")
            raise InternalServerError("Erro inesperado ao buscar pessoas.")

    def get_by_id(self, person_id):
        """Busca uma pessoa específica pelo ID."""
        try:
            if not person_id or not isinstance(person_id, str):
                raise ValidationError(field="person_id", message="ID inválido.")

            person = PersonRepository.get_by_id(person_id)
            if not person:
                logger.warning(f"Pessoa com ID {person_id} não encontrada.")
                raise NotFoundError(resource="Person", message="Pessoa não encontrada.")
            
            logger.info(f"Pessoa com ID {person_id} encontrada com sucesso.")
            return person
        except ValidationError as err:
            logger.warning(f"Erro na validação do ID: {err.message}")
            raise
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar pessoa {person_id}: {e}")
            raise InternalServerError("Erro inesperado ao buscar pessoa.")

    def create(self, data):
        """Cria uma nova pessoa no banco de dados."""
        try:
            if not data or not isinstance(data, dict):
                raise ValidationError(field="data", message="Dados de entrada inválidos.")

            normalized_data = self._normalize_data(data)

            if PersonRepository.get_by_email(normalized_data['email']):
                logger.warning("Tentativa de criação com e-mail já cadastrado.")
                raise ConflictError(resource="E-mail", message="E-mail já está cadastrado.")

            try:
                validated_data = self.schema.load(normalized_data)
            except marshmallow.exceptions.ValidationError as marshmallow_error:
                ErrorHandler.handle_marshmallow_errors(marshmallow_error.messages)

            validated_data['password'] = self.encryption.encrypt(validated_data['password'])
            person = PersonRepository.create(validated_data)
            logger.info(f"Pessoa criada com sucesso: ID {person.id}")
            return person
        except ValidationError as err:
            logger.warning(f"Erro na validação de entrada: {err.message}")
            raise
        except ConflictError:
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao criar pessoa: {e}")
            raise InternalServerError("Erro inesperado ao criar pessoa.")

    def update(self, person_id, data):
        """Atualiza os dados de uma pessoa."""
        try:
            if not person_id or not isinstance(person_id, str):
                raise ValidationError(field="person_id", message="ID inválido.")
            if not data or not isinstance(data, dict):
                raise ValidationError(field="data", message="Dados inválidos para atualização.")

            person = PersonRepository.get_by_id(person_id)
            if not person:
                logger.warning(f"Pessoa com ID {person_id} não encontrada.")
                raise NotFoundError(resource="Person", message="Pessoa não encontrada.")

            normalized_data = self._normalize_data(data)

            if 'email' in normalized_data and normalized_data['email'] != person.email:
                if PersonRepository.get_by_email(normalized_data['email']):
                    logger.warning(f"E-mail {normalized_data['email']} já em uso.")
                    raise ConflictError(resource="E-mail", message="E-mail já está cadastrado.")

            try:
                updated_data = self.schema.load(normalized_data, partial=True)
            except marshmallow.exceptions.ValidationError as marshmallow_error:
                ErrorHandler.handle_marshmallow_errors(marshmallow_error.messages)

            if 'password' in updated_data:
                updated_data['password'] = self.encryption.encrypt(updated_data['password'])

            for key, value in updated_data.items():
                setattr(person, key, value)

            updated_person = PersonRepository.update(person)
            logger.info(f"Pessoa {person_id} atualizada com sucesso.")
            return updated_person
        except ValidationError as err:
            logger.warning(f"Erro na validação de entrada: {err.message}")
            raise
        except NotFoundError:
            raise
        except ConflictError:
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar pessoa {person_id}: {e}")
            raise InternalServerError("Erro inesperado ao atualizar pessoa.")

    def delete(self, person_id):
        """Remove uma pessoa pelo ID."""
        try:
            if not person_id or not isinstance(person_id, str):
                raise ValidationError(field="person_id", message="ID inválido.")

            person = PersonRepository.get_by_id(person_id)
            if not person:
                logger.warning(f"Tentativa de deletar pessoa com ID {person_id} não encontrada.")
                raise NotFoundError(resource="Person", message="Pessoa não encontrada.")

            PersonRepository.delete(person_id)
            logger.info(f"Pessoa {person_id} deletada com sucesso.")
            return {"message": "Pessoa deletada com sucesso."}
        except ValidationError as err:
            logger.warning(f"Erro na validação do ID: {err.message}")
            raise
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao deletar pessoa {person_id}: {e}")
            raise InternalServerError("Erro inesperado ao deletar pessoa.")
