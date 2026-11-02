from app.models.usuario import Admin, Morador, UsuarioFactory
from app.repositories.usuario_repository import UsuarioRepository
from app.utils.excecoes import (
    CredenciaisInvalidasErro,
    EmailDuplicadoErro,
    NaoAutenticadoErro,
    PermissaoNegadaErro,
    ValidacaoErro,
)
from app.utils.seguranca import gerar_hash, verificar_senha
from app.utils.validadores import validar_email, validar_nome, validar_senha


class AuthService:
    def __init__(self, repositorio=None):
        self._usuarios = repositorio or UsuarioRepository()

    def cadastrar_morador(self, dados):
        return self._criar_usuario(
            dados.get("nome"), dados.get("email"), dados.get("senha"), Morador.TIPO
        )

    def criar_admin(self, nome, email, senha):
        return self._criar_usuario(nome, email, senha, Admin.TIPO)

    def _criar_usuario(self, nome, email, senha, tipo_usuario):
        nome_validado = validar_nome(nome)
        email_validado = validar_email(email)
        senha_validada = validar_senha(senha)
        if self._usuarios.buscar_por_email(email_validado) is not None:
            raise EmailDuplicadoErro("E-mail já cadastrado")
        usuario = UsuarioFactory.criar(
            tipo_usuario, nome_validado, email_validado, gerar_hash(senha_validada)
        )
        usuario.id_usuario = self._usuarios.criar(usuario)
        return self._usuarios.buscar_por_id(usuario.id_usuario)

    def autenticar(self, dados):
        email = dados.get("email")
        senha = dados.get("senha")
        if not isinstance(email, str) or not isinstance(senha, str):
            raise ValidacaoErro("Informe email e senha")
        usuario = self._usuarios.buscar_por_email(email.strip().lower())
        if usuario is None or not verificar_senha(senha, usuario.senha_hash):
            raise CredenciaisInvalidasErro("E-mail ou senha inválidos")
        if not usuario.ativo:
            raise PermissaoNegadaErro("Usuário inativo")
        return usuario

    def buscar_usuario_logado(self, id_usuario):
        usuario = self._usuarios.buscar_por_id(id_usuario)
        if usuario is None or not usuario.ativo:
            raise NaoAutenticadoErro("Sessão inválida, faça login novamente")
        return usuario

    def atualizar_perfil(self, usuario, dados):
        if "nome" not in dados and "senha" not in dados:
            raise ValidacaoErro("Informe nome e/ou senha para atualizar")
        novo_nome = validar_nome(dados["nome"]) if "nome" in dados else usuario.nome
        novo_hash = (
            gerar_hash(validar_senha(dados["senha"]))
            if "senha" in dados
            else usuario.senha_hash
        )
        self._usuarios.atualizar_perfil(usuario.id_usuario, novo_nome, novo_hash)
        usuario.alterar_nome(novo_nome)
        usuario.alterar_senha_hash(novo_hash)
        return usuario
