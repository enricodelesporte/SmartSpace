"""
Regras de negócio ligadas a espaços compartilhados.

Só o Admin pode cadastrar/desativar espaços — a checagem de
permissão fica aqui (não no repository, que só sabe falar com o
banco, nem na rota, que não deveria conter regra de negócio).
"""

from __future__ import annotations

from datetime import time

from app.models.espaco import Espaco
from app.models.usuario import Usuario
from app.repositories.espaco_repository import EspacoRepository
from app.utils.validators import validar_capacidade, validar_horario


class PermissaoNegadaError(Exception):
    """Levantada quando um usuário sem permissão tenta uma ação restrita."""


class EspacoService:
    """Casos de uso: listar, cadastrar e desativar espaços."""

    def __init__(self, espaco_repository: EspacoRepository | None = None):
        self.espaco_repository = espaco_repository or EspacoRepository()

    def listar_disponiveis(self) -> list[Espaco]:
        """Tela 'Espaços disponíveis' do morador."""
        return self.espaco_repository.listar_ativos()

    def cadastrar(
        self,
        solicitante: Usuario,
        nome: str,
        descricao: str | None,
        capacidade_maxima,
        horario_abertura: time,
        horario_fechamento: time,
    ) -> Espaco:
        if not solicitante.pode_gerenciar_espacos():
            raise PermissaoNegadaError("Apenas administradores podem cadastrar espaços.")
        if not nome or not nome.strip():
            raise ValueError("Nome do espaço é obrigatório.")

        capacidade = validar_capacidade(capacidade_maxima)
        validar_horario(horario_abertura, horario_fechamento)

        return self.espaco_repository.criar(
            nome=nome.strip(),
            descricao=descricao,
            capacidade_maxima=capacidade,
            horario_abertura=horario_abertura,
            horario_fechamento=horario_fechamento,
        )

    def desativar(self, solicitante: Usuario, id_espaco: int) -> None:
        if not solicitante.pode_gerenciar_espacos():
            raise PermissaoNegadaError("Apenas administradores podem desativar espaços.")
        self.espaco_repository.desativar(id_espaco)
