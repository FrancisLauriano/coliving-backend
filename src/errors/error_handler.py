# app/errors/error_handler.py:
import logging
from flask import jsonify
from errors.custom_errors import (
    ValidationError, NotFoundError, UnauthorizedError, ExternalAPIError, ConflictError, InternalServerError, InvalidTokenError
)

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ErrorHandler:
    """Classe para centralizar o tratamento de exceções."""

    @staticmethod
    def handle_validation_error(error: ValidationError):
        logger.warning(f"[ValidationError] Campo: {error.field} - Mensagem: {error.message}")
        return jsonify({"status": "error", "error_type": "ValidationError", "message": error.message}), 400

    @staticmethod
    def handle_not_found_error(error: NotFoundError):
        logger.warning(f"[NotFoundError] Recurso: {error.resource} - Mensagem: {error.message}")
        return jsonify({"status": "error", "error_type": "NotFoundError", "message": error.message}), 404

    @staticmethod
    def handle_unauthorized_error(error: UnauthorizedError):
        logger.error(f"[UnauthorizedError] Ação: {error.action} - Mensagem: {error.message}")
        return jsonify({"status": "error", "error_type": "UnauthorizedError", "message": error.message}), 401
    
    @staticmethod
    def handle_external_api_error(error: ExternalAPIError):
        logger.error(f"[ExternalAPIError] Serviço: {error.service} - Mensagem: {error.message}")
        return jsonify({"status": "error", "error_type": "ExternalAPIError", "message": error.message}), 503

    @staticmethod
    def handle_conflict_error(error: ConflictError):
        logger.info(f"[ConflictError] Recurso: {error.resource} - Mensagem: {error.message}")
        return jsonify({"status": "error", "error_type": "ConflictError", "message": error.message}), 409

    @staticmethod
    def handle_internal_server_error(error: InternalServerError):
        logger.error(f"[InternalServerError] Mensagem: {error.message}", exc_info=True)
        return jsonify({"status": "error", "error_type": "InternalServerError", "message": error.message}), 500
    
    @staticmethod
    def handle_invalid_token_error(error: InvalidTokenError):
        logger.error(f"[InvalidTokenError] Mensagem: {error.message}")
        return jsonify({"status": "error", "error_type": "InvalidTokenError", "message": error.message}), 401

    @staticmethod
    def handle_generic_exception(error: Exception):
        logger.error("[Exception] Erro inesperado", exc_info=error)
        return jsonify({"status": "error", "error_type": "Exception", "message": "Internal server error"}), 500
    
    @staticmethod
    def handle_marshmallow_errors(errors):
        """Converte erros de validação do Marshmallow para o formato personalizado."""
        for field, messages in errors.items():
            raise ValidationError(field=field, message=", ".join(messages))

