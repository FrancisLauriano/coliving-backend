# services/person_service.py

import logging
from repositories.person_repository import PersonRepository
from utils.encryption_utils import EncryptionUtils
from validators.person_validator import PersonValidator
from errors.custom_errors import NotFoundError, ConflictError, InternalServerError

logger = logging.getLogger(__name__)

class PersonService:
    """
    Serviço para a entidade Person.
    Responsável pela lógica de negócios e integração com o repositório e validadores.
    """

    @staticmethod
    def get_all():
        """
        Retorna todas as pessoas do banco de dados.
        """
        try:
            people = PersonRepository.get_all()
            return [person.to_dict() for person in people]
        except InternalServerError as e:
            logger.error(f"Erro ao buscar pessoas: {e}")
            raise e

    @staticmethod
    def get_by_id(person_id):
        """
        Busca uma pessoa específica pelo ID.
        """
        try:
            person = PersonRepository.get_by_id(person_id)
            return person.to_dict()
        except NotFoundError as e:
            logger.warning(f"Pessoa não encontrada: {person_id}")
            raise e
        except InternalServerError as e:
            logger.error(f"Erro ao buscar pessoa com ID {person_id}: {e}")
            raise e

    @staticmethod
    def create(data):
        """
        Cria uma nova pessoa no banco de dados.
        """
        try:
            # Validação dos dados de entrada
            validator = PersonValidator()
            validated_data = validator.validate_and_load(data)

            # Criptografar a senha
            encryption = EncryptionUtils()
            validated_data["password"] = encryption.encrypt(validated_data["password"])

            # Criar pessoa no repositório
            person = PersonRepository.create(validated_data)
            logger.info(f"Pessoa criada com sucesso: {person.id}")
            return person.to_dict()
        except ConflictError as e:
            logger.warning(f"Conflito ao criar pessoa: {e}")
            raise e
        except Exception as e:
            logger.error(f"Erro ao criar pessoa: {e}")
            raise InternalServerError("Erro ao criar pessoa.")

    @staticmethod
    def update(person_id, data):
        """
        Atualiza os dados de uma pessoa existente.
        """
        try:
            # Buscar pessoa existente
            person = PersonRepository.get_by_id(person_id)

            # Validação dos dados de entrada
            validator = PersonValidator()
            validated_data = validator.validate_and_load(data)

            # Atualizar atributos da pessoa
            for key, value in validated_data.items():
                if key != "password":  # Evitar sobrescrever a senha diretamente
                    setattr(person, key, value)

            if "password" in validated_data:
                encryption = EncryptionUtils()
                person.password = encryption.encrypt(validated_data["password"])

            # Atualizar pessoa no repositório
            updated_person = PersonRepository.update(person)
            logger.info(f"Pessoa atualizada com sucesso: {updated_person.id}")
            return updated_person.to_dict()
        except NotFoundError as e:
            logger.warning(f"Pessoa não encontrada: {person_id}")
            raise e
        except ConflictError as e:
            logger.warning(f"Conflito ao atualizar pessoa: {e}")
            raise e
        except Exception as e:
            logger.error(f"Erro ao atualizar pessoa: {e}")
            raise InternalServerError("Erro ao atualizar pessoa.")

    @staticmethod
    def delete(person_id):
        """
        Remove uma pessoa do banco de dados pelo ID.
        """
        try:
            PersonRepository.delete(person_id)
            logger.info(f"Pessoa com ID {person_id} removida com sucesso.")
            return {"message": "Pessoa removida com sucesso."}
        except NotFoundError as e:
            logger.warning(f"Pessoa não encontrada para exclusão: {person_id}")
            raise e
        except Exception as e:
            logger.error(f"Erro ao excluir pessoa: {e}")
            raise InternalServerError("Erro ao excluir pessoa.")
