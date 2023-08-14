from marshmallow import Schema, fields, validate

class UserRegisterSchema(Schema):
    name = fields.Str(
        required=True,
        error_messages={'required': 'É necessário fornecer seu nome para efetuar o cadastro'},
        validate=validate.Length(min=3, max=255, error='O campo nome deve ter entre 3 e 255 caracteres')
    )
    email = fields.Str(
        required=True,
        error_messages={'required': 'É necessário fornecer seu e-mail para efetuar o cadastro'},
        validate=validate.Email(error='O e-mail fornecido é inválido')
    )
    password = fields.Str(
        required=True,
        error_messages={'required': 'É necessário fornecer uma senha para efetuar o cadastro'},
        validate=validate.Length(min=8, max=255, error='Sua senha deve ter entre 8 e 255 caracteres')
    )

class UserLoginSchema(Schema):
    email = fields.Str(
        required=True,
        error_messages={'required': 'É necessário fornecer seu e-mail para efetuar o login'},
        validate=validate.Email(error='O e-mail fornecido é inválido')
    )
    password = fields.Str(
        required=True,
        error_messages={'required': 'É necessário fornecer sua senha para efetuar o login'},
        validate=validate.Length(min=8, max=255, error='Sua senha deve ter entre 8 e 255 caracteres')
    )
    code = fields.Str(
        required=True,
        error_messages={'required': 'É necessário fornecer o código de acesso para efetuar o login'},
        validate=validate.Length(equal=6, error='O código de acesso deve ter 6 caracteres')
    )

class UserGetTokenSchema(Schema):
    email = fields.Str(validate=validate.Email(error='O e-mail fornecido é inválido'))