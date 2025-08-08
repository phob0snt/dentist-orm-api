class TokenNotFoundError(Exception):
    def __init__(self, message: str = "Пользователь не авторизован"):
        self.message = message
        super().__init__(self.message)