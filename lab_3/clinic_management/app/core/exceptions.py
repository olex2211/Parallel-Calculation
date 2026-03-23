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
