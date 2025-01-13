# controllers/person_controller:
import logging
from flask import request, jsonify
from services.person_service import PersonService
from errors.error_handler import ErrorHandler
from errors.custom_errors import NotFoundError, ValidationError, ConflictError

logger = logging.getLogger(__name__)

class PersonController:
    @staticmethod
    def get_all():
        """
        Retorna todas as pessoas registradas.
        """
        try:
            pessoas = PersonService().get_all()
            logger.info("Pessoas listadas com sucesso.")
            return jsonify([pessoa.to_dict() for pessoa in pessoas]), 200
        except Exception as e:
            logger.error("Erro inesperado ao listar pessoas.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def get_by_id(id):
        """
        Retorna os detalhes de uma pessoa pelo ID.
        """
        try:
            if not id:
                return ErrorHandler.handle_validation_error(
                    ValidationError(field="id", message="ID inválido.")
                )

            pessoa = PersonService().get_by_id(str(id))
            logger.info(f"Pessoa {id} encontrada.")
            return jsonify(pessoa.to_dict()), 200
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar pessoa {id}.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def create():
        """
        Cria uma nova pessoa no sistema.
        """
        try:
            data = request.get_json()
            if not data or not isinstance(data, dict):
                raise ValidationError(field="data", message="Dados de entrada inválidos.")
            
            pessoa = PersonService().create(data)
            logger.info("Pessoa criada com sucesso.")
            return jsonify(pessoa.to_dict()), 201
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except ConflictError as e:
            return ErrorHandler.handle_conflict_error(e)
        except Exception as e:
            logger.error("Erro inesperado ao criar pessoa.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def update(id):
        """
        Atualiza os dados de uma pessoa pelo ID.
        """
        try:
            if not id:
                return ErrorHandler.handle_validation_error(
                    ValidationError(field="id", message="ID inválido.")
                )
            data = request.get_json()
            if not data or not isinstance(data, dict):
                raise ValidationError(field="data", message="Dados de entrada inválidos.")

            pessoa = PersonService().update(str(id), data)
            logger.info(f"Pessoa {id} atualizada com sucesso.")
            return jsonify(pessoa.to_dict()), 200
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except ConflictError as e:
            return ErrorHandler.handle_conflict_error(e)
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar pessoa {id}.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)

    @staticmethod
    def delete(id):
        """
        Remove uma pessoa do sistema pelo ID.
        """
        try:
            if not id:
                return ErrorHandler.handle_validation_error(
                    ValidationError(field="id", message="ID inválido.")
                )

            PersonService().delete(str(id))
            logger.info(f"Pessoa {id} removida com sucesso.")
            return '', 204
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except NotFoundError as e:
            return ErrorHandler.handle_not_found_error(e)
        except Exception as e:
            logger.error(f"Erro inesperado ao deletar pessoa {id}.", exc_info=True)
            return ErrorHandler.handle_generic_exception(e)
