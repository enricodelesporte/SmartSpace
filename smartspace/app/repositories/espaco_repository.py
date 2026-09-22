"""
Camada de acesso a dados (Repository) para a tabela `espaco`.
"""

from __future__ import annotations

from datetime import time

from app.extensions import get_connection
from app.models.espaco import Espaco


class EspacoRepository:
    """Métodos de leitura e escrita da tabela `espaco`."""

    def listar_ativos(self) -> list[Espaco]:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("SELECT * FROM espaco WHERE ativo = TRUE ORDER BY nome")
            rows = cur.fetchall()
            return [self._to_espaco(r) for r in rows]

    def buscar_por_id(self, id_espaco: int) -> Espaco | None:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("SELECT * FROM espaco WHERE id_espaco = %s", (id_espaco,))
            row = cur.fetchone()
            return self._to_espaco(row) if row else None

    def criar(
        self,
        nome: str,
        descricao: str | None,
        capacidade_maxima: int,
        horario_abertura: time,
        horario_fechamento: time,
    ) -> Espaco:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO espaco (nome, descricao, capacidade_maxima, horario_abertura, horario_fechamento)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *
                """,
                (nome, descricao, capacidade_maxima, horario_abertura, horario_fechamento),
            )
            row = cur.fetchone()
            conn.commit()
            return self._to_espaco(row)

    def desativar(self, id_espaco: int) -> None:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("UPDATE espaco SET ativo = FALSE WHERE id_espaco = %s", (id_espaco,))
            conn.commit()

    @staticmethod
    def _to_espaco(row) -> Espaco:
        return Espaco(
            id_espaco=row["id_espaco"],
            nome=row["nome"],
            descricao=row["descricao"],
            capacidade_maxima=row["capacidade_maxima"],
            horario_abertura=row["horario_abertura"],
            horario_fechamento=row["horario_fechamento"],
            ativo=row["ativo"],
        )
