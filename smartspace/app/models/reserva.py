"""
Modelagem orientada a objetos da reserva (tabela `reserva`) e da
regra de negócio central do sistema: verificação de conflito de
horário. Esse é o ponto do projeto que mais demonstra lógica de
programação "de verdade" — vale qualquer integrante do grupo saber
explicar este arquivo na avaliação individual.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time
from enum import Enum


class StatusReserva(str, Enum):
    """Valores aceitos pelo CHECK constraint da tabela `reserva`."""

    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"


@dataclass
class Reserva:
    """Representa uma reserva de um morador em um espaço, numa data/horário."""

    id_reserva: int | None
    id_usuario: int
    id_espaco: int
    data_reserva: date
    hora_inicio: time
    hora_fim: time
    status: StatusReserva = StatusReserva.CONFIRMADA
    data_criacao: datetime | None = None

    def sobrepoe(self, outra: "Reserva") -> bool:
        """
        Verifica se este intervalo de horário se sobrepõe ao de
        `outra` reserva, considerando apenas reservas do MESMO
        espaço, na MESMA data, e que ainda estejam CONFIRMADAs.

        Esta é a regra citada no comentário do script SQL do banco:
        "duas reservas não podem se sobrepor no mesmo espaço/data" —
        não dá para garantir só com constraint de banco (exige
        comparar vários registros), por isso vive aqui no domínio.
        """
        if self.id_espaco != outra.id_espaco or self.data_reserva != outra.data_reserva:
            return False
        if outra.status == StatusReserva.CANCELADA:
            return False
        # Dois intervalos [a, b) e [c, d) se sobrepõem se a < d e c < b.
        return self.hora_inicio < outra.hora_fim and outra.hora_inicio < self.hora_fim

    def cancelar(self) -> None:
        self.status = StatusReserva.CANCELADA

    def __str__(self) -> str:
        return f"Reserva #{self.id_reserva} - Espaço {self.id_espaco} em {self.data_reserva}"
