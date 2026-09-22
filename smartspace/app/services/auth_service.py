"""
Regras de negócio de autenticação e cadastro.

Atende os requisitos 4 (Validação de Dados) e 7 (Autenticação de
Usuário), e implementa exatamente o fluxo desenhado no fluxograma:
"Já possui conta?" -> Sim (login) / Não (cadastro, sempre como
MORADOR, depois volta para a tela de login).
"""

from __future__ import annotations

from app.models.usuario import TipoUsuario, Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.utils.security import gerar_hash_senha, verificar_senha
from app.utils.validators import validar_email, validar_senha


class AuthService:
    """Casos de uso de autenticação: registrar() e autenticar()."""

    def __init__(self, usuario_repository: UsuarioRepository | None = None):
        self.usuario_repository = usuario_repository or UsuarioRepository()

    def registrar(self, nome: str, email: str, senha: str) -> Usuario:
        """
        Fluxo de 'Criar conta': valida os dados, garante e-mail
        único e sempre cria como MORADOR (decisão tomada no
        fluxograma — só um Admin promove alguém depois, se
        precisar).
        """
        if not nome or not nome.strip():
            raise ValueError("Nome é obrigatório.")
        if not validar_email(email):
            raise ValueError("E-mail inválido.")
        if not validar_senha(senha):
            raise ValueError("Senha deve ter no mínimo 6 caracteres.")
        if self.usuario_repository.buscar_por_email(email):
            raise ValueError("Já existe uma conta com este e-mail.")

        senha_hash = gerar_hash_senha(senha)
        return self.usuario_repository.criar(nome.strip(), email, senha_hash, TipoUsuario.MORADOR)

    def autenticar(self, email: str, senha: str) -> Usuario:
        """Fluxo de 'Login': busca por e-mail e confere o hash da senha."""
        usuario = self.usuario_repository.buscar_por_email(email)
        if usuario is None or not verificar_senha(senha, usuario.senha_hash):
            raise ValueError("E-mail ou senha inválidos.")
        return usuario
