import secrets

from flask import request, session

from app.utils.excecoes import PermissaoNegadaErro

CHAVE_SESSAO = "csrf_token"
CAMPO_FORMULARIO = "csrf_token"


def obter_token_csrf():
    if CHAVE_SESSAO not in session:
        session[CHAVE_SESSAO] = secrets.token_urlsafe(32)
    return session[CHAVE_SESSAO]


def validar_token_csrf():
    esperado = session.get(CHAVE_SESSAO, "")
    enviado = request.form.get(CAMPO_FORMULARIO, "")
    if not esperado or not secrets.compare_digest(
        esperado.encode("utf-8"), enviado.encode("utf-8")
    ):
        raise PermissaoNegadaErro(
            "Formulário expirado. Volte para a página anterior e tente novamente"
        )
