from infrastructure.exception.infrastructure_exception import InfrastructureException


class HttpException(InfrastructureException):
    def __init__(self, status_code: int, message: str):
        super().__init__(message)
        self.status_code: int = status_code
