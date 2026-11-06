class ApiError(Exception):
    """Erro de negócio/validação da API."""

    def __init__(self, mensagem, status_code=400):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.status_code = status_code


class ValidationError(ApiError):
    pass


class NotFoundError(ApiError):
    def __init__(self, mensagem="Registro não encontrado."):
        super().__init__(mensagem, status_code=404)


class BusinessRuleError(ApiError):
    def __init__(self, mensagem):
        super().__init__(mensagem, status_code=409)
