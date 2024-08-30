from fastapi import status


class SearchApiError(Exception):
    """Base exception class"""

    def __init__(
        self,
        message: str = "Service is unavailable",
        name: str = "API Recherche des entreprises",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        self.message = message
        self.name = name
        self.status_code = status_code
        super().__init__(self.message, self.name)


class InvalidSirenError(SearchApiError):
    """Custom exception for invalid SIREN number"""

    def __init__(self):
        super().__init__(
            message="Numéro Siren invalide.",
            name="",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class InvalidParamError(SearchApiError):
    """Invalid parameters in request"""

    def __init__(self, message):
        super().__init__(
            message=message,
            name="",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class InternalError(SearchApiError):
    """Internal service error"""

    def __init__(self, message):
        super().__init__(
            message=message,
            name="",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
