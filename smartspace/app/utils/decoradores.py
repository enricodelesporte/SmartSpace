from functools import wraps

from flask import flash, g, redirect, session, url_for

from app.services.auth_service import AuthService
from app.utils.excecoes import NaoAutenticadoErro, PermissaoNegadaErro

_auth_service = AuthService()


def login_obrigatorio(funcao):
    @wraps(funcao)
    def interna(*args, **kwargs):
        id_usuario = session.get("id_usuario")
        if id_usuario is None:
            raise NaoAutenticadoErro("Faça login para continuar")
        try:
            g.usuario = _auth_service.buscar_usuario_logado(id_usuario)
        except NaoAutenticadoErro:
            session.clear()
            raise
        return funcao(*args, **kwargs)

    return interna


def admin_obrigatorio(funcao):
    @wraps(funcao)
    @login_obrigatorio
    def interna(*args, **kwargs):
        if not g.usuario.pode_gerenciar_espacos():
            raise PermissaoNegadaErro("Acesso restrito a administradores")
        return funcao(*args, **kwargs)

    return interna


def pagina_login_obrigatoria(funcao):
    @wraps(funcao)
    def interna(*args, **kwargs):
        id_usuario = session.get("id_usuario")
        if id_usuario is None:
            flash("Faça login para continuar.", "error")
            return redirect(url_for("paginas_conta.login"))
        try:
            g.usuario = _auth_service.buscar_usuario_logado(id_usuario)
        except NaoAutenticadoErro as erro:
            session.clear()
            flash(erro.mensagem, "error")
            return redirect(url_for("paginas_conta.login"))
        return funcao(*args, **kwargs)

    return interna


def pagina_admin_obrigatoria(funcao):
    @wraps(funcao)
    @pagina_login_obrigatoria
    def interna(*args, **kwargs):
        if not g.usuario.pode_gerenciar_espacos():
            raise PermissaoNegadaErro("Acesso restrito a administradores")
        return funcao(*args, **kwargs)

    return interna
