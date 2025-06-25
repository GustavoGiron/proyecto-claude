from marshmallow import Schema, fields, validate


class LoginRequestSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=6))


class RefreshTokenRequestSchema(Schema):
    refresh_token = fields.Str(required=True)


class UserResponseSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Email()
    nombre = fields.Str()
    apellido = fields.Str()
    is_active = fields.Bool()
    fecha_creacion = fields.DateTime()
    ultima_sesion = fields.DateTime()
    role = fields.Str()


class LoginResponseSchema(Schema):
    access_token = fields.Str()
    refresh_token = fields.Str()
    user = fields.Nested(UserResponseSchema)


class TokenResponseSchema(Schema):
    access_token = fields.Str()


class PermissionsResponseSchema(Schema):
    role = fields.Str()
    modules = fields.List(fields.Dict())
    permissions = fields.List(fields.Dict())


class ChangePasswordSchema(Schema):
    current_password = fields.Str(required=True)
    new_password = fields.Str(required=True, validate=validate.Length(min=6))
    confirm_password = fields.Str(required=True)


class CreateUserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    nombre = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    apellido = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    role_id = fields.Int(required=True)


class UpdateUserSchema(Schema):
    email = fields.Email()
    nombre = fields.Str(validate=validate.Length(min=2, max=100))
    apellido = fields.Str(validate=validate.Length(min=2, max=100))
    role_id = fields.Int()
    is_active = fields.Bool()
    password = fields.Str(validate=validate.Length(min=6))