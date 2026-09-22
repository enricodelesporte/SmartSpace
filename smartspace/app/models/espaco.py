"""
Modelagem orientada a objetos do espaço compartilhado (tabela `espaco`).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import time


@dataclass
class Espaco:
    """Representa um espaço reservável do condomínio (salão, churrasqueira etc.)."""

    id_espaco: int | None
    nome: str
    descricao: str | None
    capacidade_maxima: int
    horario_abertura: time
    horario_fechamento: time
    ativo: bool = True

    def dentro_do_horario_de_funcionamento(self, hora_inicio: time, hora_fim: time) -> bool:
        """
        Regra de validação (requisito 4: validação de dados): uma
        reserva não pode começar antes de abrir nem terminar depois
        de fechar.
        """
        return self.horario_abertura <= hora_inicio and hora_fim <= self.horario_fechamento

    def __str__(self) -> str:
        return f"{self.nome} (capacidade: {self.capacidade_maxima})"
