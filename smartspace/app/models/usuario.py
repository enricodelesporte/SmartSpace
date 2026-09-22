"""
Modelagem orientada a objetos dos usuários do sistema SmartSpace.

Define a classe base `Usuario` e as subclasses `Admin` e `Morador`,
representando os dois perfis exigidos pelo projeto (requisito 9:
"Perfis de Usuário" com permissões distintas). A diferença de
permissão entre os perfis é resolvida via POLIMORFISMO: o mesmo
método (`pode_gerenciar_espacos`, por exemplo) se comporta de forma
diferente dependendo da subclasse, em vez de espalhar `if tipo ==`
por todo o código.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TipoUsuario(str, Enum):
    """Valores aceitos pelo CHECK constraint da tabela `usuario`."""

    ADMIN = "ADMIN"
    MORADOR = "MORADOR"


@dataclass
class Usuario:
    """
    Classe base para qualquer usuário autenticado.

    Mapeia diretamente a tabela `usuario`. A senha nunca é
    armazenada em texto puro — apenas o hash (ver
    app/utils/security.py) — atendendo ao requisito de
    autenticação segura (item 7 do roteiro).
    """

    id_usuario: int | None
    nome: str
    email: str
    senha_hash: str
    tipo_usuario: TipoUsuario
    data_cadastro: datetime | None = None
    ativo: bool = True

    def pode_gerenciar_espacos(self) -> bool:
        """Permissão padrão (encapsulamento): só é liberada nas subclasses que fizerem sentido."""
        return False

    def pode_gerenciar_qualquer_reserva(self) -> bool:
        """Permissão padrão: só Admin pode mexer em reservas de outras pessoas."""
        return False

    def __str__(self) -> str:  # facilita logs e debug
        return f"{self.nome} ({self.tipo_usuario.value})"


class Admin(Usuario):
    """
    Perfil Administrador (síndico).

    Sobrescreve as permissões da classe base — só ele pode
    cadastrar/editar espaços e mexer em reservas de qualquer morador.
    """

    def __init__(self, *args, **kwargs) -> None:
        kwargs["tipo_usuario"] = TipoUsuario.ADMIN
        super().__init__(*args, **kwargs)

    def pode_gerenciar_espacos(self) -> bool:
        return True

    def pode_gerenciar_qualquer_reserva(self) -> bool:
        return True


class Morador(Usuario):
    """Perfil Morador (usuário comum) — permissões restritas às próprias reservas."""

    def __init__(self, *args, **kwargs) -> None:
        kwargs["tipo_usuario"] = TipoUsuario.MORADOR
        super().__init__(*args, **kwargs)


def criar_usuario_por_tipo(tipo: str | TipoUsuario, **kwargs) -> Usuario:
    """
    Factory que instancia a subclasse correta a partir do valor de
    `tipo_usuario` vindo do banco de dados. Usada pelo repository
    para nunca deixar o resto da aplicação decidir "na mão" qual
    classe usar.
    """
    classes = {
        TipoUsuario.ADMIN: Admin,
        TipoUsuario.MORADOR: Morador,
    }
    tipo_enum = TipoUsuario(tipo)
    classe = classes[tipo_enum]
    kwargs.pop("tipo_usuario", None)
    return classe(**kwargs)
