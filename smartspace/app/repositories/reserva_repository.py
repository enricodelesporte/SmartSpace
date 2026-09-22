"""
Camada de acesso a dados (Repository) para a tabela `reserva`.

Repare que não existe uma tabela separada para "histórico" ou
"agendamentos": tanto a tela do morador ("Minhas Reservas") quanto
a do admin ("Todas as Reservas") consultam esta mesma tabela, só
que com filtros diferentes.
"""

from __future__ import annotations

from datetime import date, time

from app.extensions import get_connection
from app.models.reserva import Reserva, StatusReserva


class ReservaRepository:
    """Métodos de leitura e escrita da tabela `reserva`."""

    def buscar_por_id(self, id_reserva: int) -> Reserva | None:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("SELECT * FROM reserva WHERE id_reserva = %s", (id_reserva,))
            row = cur.fetchone()
            return self._to_reserva(row) if row else None

    def listar_por_espaco_e_data(self, id_espaco: int, data_reserva: date) -> list[Reserva]:
        """Usado pela regra de conflito de horário (ver ReservaService.esta_disponivel)."""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM reserva
                WHERE id_espaco = %s AND data_reserva = %s AND status = 'CONFIRMADA'
                """,
                (id_espaco, data_reserva),
            )
            rows = cur.fetchall()
            return [self._to_reserva(r) for r in rows]

    def listar_por_usuario(self, id_usuario: int) -> list[Reserva]:
        """Tela 'Minhas Reservas' do morador."""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM reserva WHERE id_usuario = %s ORDER BY data_reserva DESC",
                (id_usuario,),
            )
            rows = cur.fetchall()
            return [self._to_reserva(r) for r in rows]

    def listar_todas(self) -> list[Reserva]:
        """Tela 'Todas as Reservas' do admin."""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("SELECT * FROM reserva ORDER BY data_reserva DESC")
            rows = cur.fetchall()
            return [self._to_reserva(r) for r in rows]

    def criar(self, id_usuario: int, id_espaco: int, data_reserva: date, hora_inicio: time, hora_fim: time) -> Reserva:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO reserva (id_usuario, id_espaco, data_reserva, hora_inicio, hora_fim)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *
                """,
                (id_usuario, id_espaco, data_reserva, hora_inicio, hora_fim),
            )
            row = cur.fetchone()
            conn.commit()
            return self._to_reserva(row)

    def cancelar(self, id_reserva: int) -> None:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                "UPDATE reserva SET status = 'CANCELADA' WHERE id_reserva = %s",
                (id_reserva,),
            )
            conn.commit()

    @staticmethod
    def _to_reserva(row) -> Reserva:
        return Reserva(
            id_reserva=row["id_reserva"],
            id_usuario=row["id_usuario"],
            id_espaco=row["id_espaco"],
            data_reserva=row["data_reserva"],
            hora_inicio=row["hora_inicio"],
            hora_fim=row["hora_fim"],
            status=StatusReserva(row["status"]),
            data_criacao=row["data_criacao"],
        )
