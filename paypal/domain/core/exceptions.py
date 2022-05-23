from django.core.exceptions import ValidationError


class ObjectDoesNotExistError(ValidationError):
    def __init__(self, type: str, id: str, code=None, params=None):
        message = f"{type} object with id={id} does not exist."
        super().__init__(message=message, code=code, params=params)


class ObjectCannotBeDeletedError(ValidationError):
    def __init__(self, type: str, id: str, code=None, params=None):
        message = f"{type} object with id={id} cannot be deleted: it has linked data!"
        super().__init__(message=message, code=code, params=params)


class ObjectMustBeLinkedError(ValidationError):
    def __init__(self, type: str, link_to: list, code=None, params=None):
        message = f"{type} object must be linked to: {', '.join(link_to)}."
        super().__init__(message=message, code=code, params=params)
