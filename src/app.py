# app.py:

from flask import Flask, jsonify
from config.settings import Config
from config.database import init_db
from middlewares.cors import init_cors
from errors.error_handler import ErrorHandler
import logging
from routes.person_routes import person_routes
from routes.auth_routes import auth_routes  # Importar as rotas de autenticação

# Configurar logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_app():
    """
    Inicializa e configura a aplicação Flask.
    """
    app = Flask(__name__)

    # Configurações da aplicação
    app.config.from_object(Config)

    # Inicializar banco de dados e migrações
    init_db(app)

    init_cors(app)

    # Registrar blueprints
    app.register_blueprint(person_routes)
    app.register_blueprint(auth_routes)  # Registrar as rotas de autenticação

    # Tratamento global de erros
    register_error_handlers(app)

    @app.route("/")
    def home():
        return jsonify({"message": "Bem-vindo à API Coliving!"}), 200

    return app


def register_error_handlers(app):
    """
    Registra manipuladores de erros personalizados na aplicação Flask.
    """
    app.register_error_handler(400, ErrorHandler.handle_validation_error)
    app.register_error_handler(404, ErrorHandler.handle_not_found_error)
    app.register_error_handler(401, ErrorHandler.handle_unauthorized_error)
    app.register_error_handler(503, ErrorHandler.handle_external_api_error)
    app.register_error_handler(409, ErrorHandler.handle_conflict_error)
    app.register_error_handler(500, ErrorHandler.handle_internal_server_error)
    app.register_error_handler(403, ErrorHandler.handle_invalid_token_error)
    app.register_error_handler(Exception, ErrorHandler.handle_generic_exception)



if __name__ == "__main__":
    app = create_app()
    app.run(debug=Config.DEBUG, host="0.0.0.0", port=5000)
