class UnauthorizedException(Exception):
    def __init__(self, errors) -> None:
        super().__init__()
        self.errors = errors