class AppErro(Exception):
    codigo_http = 500

    def __init__(self, mensagem):
        super().__init__(mensagem)
        self.mensagem = mensagem


class ValidacaoErro(AppErro):
    codigo_http = 400


class NaoAutenticadoErro(AppErro):
    codigo_http = 401


class CredenciaisInvalidasErro(NaoAutenticadoErro):
    pass


class PermissaoNegadaErro(AppErro):
    codigo_http = 403


class NaoEncontradoErro(AppErro):
    codigo_http = 404


class ConflitoHorarioErro(AppErro):
    codigo_http = 409


class EmailDuplicadoErro(AppErro):
    codigo_http = 409
