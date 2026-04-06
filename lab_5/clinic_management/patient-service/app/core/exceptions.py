class EntityNotFoundException(Exception):
    def __init__(self, entity_name: str, entity_id: int):
        self.entity_name = entity_name
        self.entity_id = entity_id
        super().__init__(f"{entity_name} with id={entity_id} not found")


class BusinessRuleException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ConflictException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ServiceUnavailableException(Exception):
    def __init__(self, service_name: str, detail: str = ""):
        self.service_name = service_name
        self.detail = detail
        msg = f"{service_name} is unavailable"
        if detail:
            msg += f": {detail}"
        super().__init__(msg)
