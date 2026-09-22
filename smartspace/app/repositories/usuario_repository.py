"""
Camada de acesso a dados (Repository) para a tabela `usuario`.

Isola todo o SQL num só lugar: os services (regras de negócio) não
sabem como os dados são persistidos, só chamam estes métodos. Isso
é o padrão Repository e ajuda a demonstrar "Engenharia de Software"
(um dos conceitos avaliados no projeto) — troca de banco ou de
biblioteca de acesso a dados fica isolada aqui.
"""

from __future__ import annotations

from app.extensions import get_connection
from app.models.usuario import TipoUsuario, Usuario, criar_usuario_por_tipo


class UsuarioRepository:
    """Métodos de leitura e escrita da tabela `usuario`."""

    def buscar_por_email(self, email: str) -> Usuario | None:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM usuario WHERE email = %s AND ativo = TRUE",
                (email,),
            )
            row = cur.fetchone()
            return self._to_usuario(row) if row else None

    def buscar_por_id(self, id_usuario: int) -> Usuario | None:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("SELECT * FROM usuario WHERE id_usuario = %s", (id_usuario,))
            row = cur.fetchone()
            return self._to_usuario(row) if row else None

    def criar(self, nome: str, email: str, senha_hash: str, tipo_usuario: TipoUsuario) -> Usuario:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO usuario (nome, email, senha_hash, tipo_usuario)
                VALUES (%s, %s, %s, %s)
                RETURNING *
                """,
                (nome, email, senha_hash, tipo_usuario.value),
            )
            row = cur.fetchone()
            conn.commit()
            return self._to_usuario(row)

    @staticmethod
    def _to_usuario(row) -> Usuario:
        """Converte uma linha do banco (dict) na subclasse correta (Admin ou Morador)."""
        return criar_usuario_por_tipo(
            tipo=row["tipo_usuario"],
            id_usuario=row["id_usuario"],
            nome=row["nome"],
            email=row["email"],
            senha_hash=row["senha_hash"],
            data_cadastro=row["data_cadastro"],
            ativo=row["ativo"],
        )
