# routes/person_routes.py:
from flask import Blueprint
from controllers.person_controller import PersonController
from middlewares.auth_middleware import jwt_required

# Criação do Blueprint para as rotas de Person
person_routes = Blueprint("person_routes", __name__, url_prefix="/persons")

# Rotas públicas
person_routes.route("/", methods=["POST"])(PersonController.create)

# Rotas protegidas por autenticação
person_routes.route("/", methods=["GET"])(jwt_required(PersonController.get_all))
person_routes.route("/<id>", methods=["GET"])(jwt_required(PersonController.get_by_id))
person_routes.route("/<id>", methods=["PUT"])(jwt_required(PersonController.update))
person_routes.route("/<id>", methods=["DELETE"])(jwt_required(PersonController.delete))
