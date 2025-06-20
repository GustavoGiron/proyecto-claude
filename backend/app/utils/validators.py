class ValidationError(Exception):
    def __init__(self, message: str, code: int):
        super().__init__(message)
        self.code = code
        self.message = message

def validate_telefono(telefono: str):
    if telefono and not telefono.replace('-', '').isdigit():
        raise ValidationError("El teléfono debe contener solo dígitos y guiones", code=1001)
    return True
