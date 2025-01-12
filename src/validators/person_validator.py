# validators/person_validator.py:

from marshmallow import Schema, fields, validate, validates, ValidationError as MarshmallowValidationError
from errors.custom_errors import ValidationError


class PersonValidator(Schema):
    """
    Validador para a entidade Person.
    Define os campos e validações para os dados da pessoa.
    """
    name = fields.String(
        required=True,
        validate=validate.Length(min=3, max=255),
        error_messages={
            "required": "O campo 'name' é obrigatório.",
            "min": "O nome deve ter pelo menos 3 caracteres.",
            "max": "O nome deve ter no máximo 255 caracteres."
        }
    )
    phone = fields.String(
        required=True,
        validate=validate.Length(min=10, max=20),
        error_messages={
            "required": "O campo 'phone' é obrigatório.",
            "min": "O telefone deve ter pelo menos 10 caracteres.",
            "max": "O telefone deve ter no máximo 20 caracteres."
        }
    )
    email = fields.Email(
        required=True,
        validate=validate.Length(max=255),
        error_messages={
            "required": "O campo 'email' é obrigatório.",
            "invalid": "O e-mail deve ser válido.",
            "max": "O e-mail deve ter no máximo 255 caracteres."
        }
    )
    person_type = fields.String(
        required=True,
        validate=validate.OneOf(["user", "admin"], error="O tipo deve ser 'user' ou 'admin'."),
        error_messages={
            "required": "O campo 'person_type' é obrigatório.",
            "one_of": "O tipo deve ser 'user' ou 'admin'."
        }
    )
    registration_date = fields.Date(
        required=False,  # Permitido ser preenchido automaticamente
        error_messages={
            "invalid": "A data de registro deve estar no formato válido (YYYY-MM-DD)."
        }
    )
    password = fields.String(
        required=True,
        validate=[
            validate.Length(min=6, max=20),
            validate.Regexp(
                r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,20}$',
                error="A senha deve ter entre 6 e 20 caracteres, contendo pelo menos uma letra, um número e um caractere especial."
            )
        ],
        error_messages={
            "required": "O campo 'password' é obrigatório.",
            "min": "A senha deve ter pelo menos 6 caracteres.",
            "max": "A senha deve ter no máximo 20 caracteres."
        }
    )

    @validates("name")
    def validate_name(self, value):
        if not value.isalpha():
            raise MarshmallowValidationError("O nome deve conter apenas letras.")

    def validate_and_load(self, data):
        """
        Método auxiliar para validar os dados e retornar erros no formato personalizado.
        """
        try:
            return self.load(data)
        except MarshmallowValidationError as err:
            for field, messages in err.messages.items():
                raise ValidationError(field=field, message=", ".join(messages))
