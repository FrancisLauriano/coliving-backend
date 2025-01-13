# repositories/person_repository.py:
import logging
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from config.database import db
from models.person_model import Person
from errors.custom_errors import NotFoundError, ConflictError, InternalServerError

logger = logging.getLogger(__name__)

class PersonRepository:
    """Repositório para operações CRUD na entidade Person."""

    @staticmethod
    def get_all():
        """Retorna todas as pessoas no banco de dados."""
        try:
            people = Person.query.all()
            logger.info("Pessoas obtidas com sucesso.")
            return people
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar pessoas: {e}")
            raise InternalServerError("Erro ao buscar pessoas no banco de dados.")

    @staticmethod
    def get_by_id(person_id):
        """Busca uma pessoa pelo ID."""
        try:
            person = Person.query.get(person_id)
            if not person:
                logger.warning(f"Pessoa com ID {person_id} não encontrada.")
                raise NotFoundError(resource="Person", message="Pessoa não encontrada.")
            logger.info(f"Pessoa com ID {person_id} encontrada com sucesso.")
            return person
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar pessoa com ID {person_id}: {e}")
            raise InternalServerError("Erro ao buscar pessoa no banco de dados.")
        
    @staticmethod
    def get_by_email(email):
        """ Busca uma pessoa pelo e-mail."""
        try:
            person = Person.query.filter_by(email=email).first()
            return person
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar pessoa pelo e-mail {email}: {e}")
            raise InternalServerError("Erro ao buscar pessoa no banco de dados.")
    

    @staticmethod
    def create(data):
        """Cria uma nova pessoa no banco de dados."""
        try:
            person = Person(**data)
            db.session.add(person)
            db.session.commit()
            logger.info(f"Pessoa criada com sucesso: {person.id}")
            return person
        except IntegrityError as e:
            db.session.rollback()
            logger.warning(f"Erro de integridade ao criar pessoa: {e}")
            raise ConflictError(resource="Person", message="Email já cadastrado.")
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro ao criar pessoa: {e}")
            raise InternalServerError("Erro ao criar pessoa no banco de dados.")

    @staticmethod
    def update(person):
        """Atualiza uma pessoa no banco de dados."""
        try:
            db.session.commit()
            logger.info(f"Pessoa com ID {person.id} atualizada com sucesso.")
            return person
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar pessoa com ID {person.id}: {e}")
            raise InternalServerError("Erro ao atualizar pessoa no banco de dados.")

    @staticmethod
    def delete(person_id):
        """Remove uma pessoa do banco de dados pelo ID."""
        try:
            person = PersonRepository.get_by_id(person_id)
            db.session.delete(person)
            db.session.commit()
            logger.info(f"Pessoa com ID {person_id} removida com sucesso.")
        except NotFoundError as e:
            logger.warning(f"Tentativa de deletar pessoa não encontrada: ID {person_id}")
            raise e
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Erro ao deletar pessoa com ID {person_id}: {e}")
            raise InternalServerError("Erro ao deletar pessoa no banco de dados.")
