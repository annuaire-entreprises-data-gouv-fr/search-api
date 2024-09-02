class InvalidSirenError(Exception):
    """
    Custom exception for invalid SIREN number
    """

    def __init__(self, message="Numéro Siren invalide"):
        self.message = message
        super().__init__(self.message)
