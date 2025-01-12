# routes/auth_routes.py:
from flask import Blueprint
from controllers.auth_controller import AuthController

# Criação do Blueprint para as rotas de autenticação
auth_routes = Blueprint("auth_routes", __name__, url_prefix="/auth")

# Rota para login
auth_routes.route("/login", methods=["POST"])(AuthController.login)

# Rota para validação de token
auth_routes.route("/validate", methods=["GET"])(AuthController.validate_token)

# Rota para renovação de token
auth_routes.route("/refresh", methods=["POST"])(AuthController.refresh_token)
