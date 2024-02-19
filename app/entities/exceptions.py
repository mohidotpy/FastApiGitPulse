class InvalidDataException(Exception):
    def __init__(self, message="Invalid data"):
        self.message = message
        super().__init__(self.message)