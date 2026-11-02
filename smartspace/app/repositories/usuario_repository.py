import pymysql

from app.database import consultar_um, executar
from app.models.usuario import UsuarioFactory
from app.utils.excecoes import EmailDuplicadoErro


class UsuarioRepository:
    def buscar_por_id(self, id_usuario, conexao=None):
        registro = consultar_um(
            "SELECT * FROM usuario WHERE id_usuario = %s", (id_usuario,), conexao
        )
        return UsuarioFactory.a_partir_do_registro(registro) if registro else None

    def buscar_por_email(self, email, conexao=None):
        registro = consultar_um(
            "SELECT * FROM usuario WHERE email = %s", (email,), conexao
        )
        return UsuarioFactory.a_partir_do_registro(registro) if registro else None

    def criar(self, usuario, conexao=None):
        try:
            return executar(
                "INSERT INTO usuario (nome, email, senha_hash, tipo_usuario) "
                "VALUES (%s, %s, %s, %s)",
                (usuario.nome, usuario.email, usuario.senha_hash, usuario.tipo_usuario),
                conexao,
            )
        except pymysql.err.IntegrityError:
            raise EmailDuplicadoErro("E-mail já cadastrado")

    def atualizar_perfil(self, id_usuario, nome, senha_hash, conexao=None):
        executar(
            "UPDATE usuario SET nome = %s, senha_hash = %s WHERE id_usuario = %s",
            (nome, senha_hash, id_usuario),
            conexao,
        )
