from flask import Blueprint, g, session

from app.services.auth_service import AuthService
from app.utils.decoradores import login_obrigatorio
from app.utils.requisicao import ler_json_obrigatorio, sucesso

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")
auth_service = AuthService()


@auth_bp.post("/cadastro")
def cadastrar():
    usuario = auth_service.cadastrar_morador(ler_json_obrigatorio())
    return sucesso(usuario.para_dicionario(), "Conta criada com sucesso", 201)


@auth_bp.post("/login")
def entrar():
    usuario = auth_service.autenticar(ler_json_obrigatorio())
    session.clear()
    session["id_usuario"] = usuario.id_usuario
    return sucesso(usuario.para_dicionario(), "Login realizado com sucesso")


@auth_bp.post("/logout")
@login_obrigatorio
def sair():
    session.clear()
    return sucesso(mensagem="Sessão encerrada")


@auth_bp.get("/perfil")
@login_obrigatorio
def ver_perfil():
    return sucesso(g.usuario.para_dicionario())


@auth_bp.put("/perfil")
@login_obrigatorio
def editar_perfil():
    usuario = auth_service.atualizar_perfil(g.usuario, ler_json_obrigatorio())
    return sucesso(usuario.para_dicionario(), "Perfil atualizado com sucesso")
