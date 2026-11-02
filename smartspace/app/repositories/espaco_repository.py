from app.database import consultar, consultar_um, executar
from app.models.espaco import Espaco


class EspacoRepository:
    def buscar_por_id(self, id_espaco, conexao=None, bloquear=False):
        sql = "SELECT * FROM espaco WHERE id_espaco = %s"
        if bloquear:
            sql += " FOR UPDATE"
        registro = consultar_um(sql, (id_espaco,), conexao)
        return Espaco.a_partir_do_registro(registro) if registro else None

    def listar_ativos(self, conexao=None):
        registros = consultar(
            "SELECT * FROM espaco WHERE ativo = TRUE ORDER BY nome", (), conexao
        )
        return [Espaco.a_partir_do_registro(registro) for registro in registros]

    def criar(self, espaco, conexao=None):
        return executar(
            "INSERT INTO espaco (nome, descricao, capacidade_maxima, "
            "horario_abertura, horario_fechamento, ativo) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (
                espaco.nome,
                espaco.descricao,
                espaco.capacidade_maxima,
                espaco.horario_abertura,
                espaco.horario_fechamento,
                espaco.ativo,
            ),
            conexao,
        )

    def atualizar(self, espaco, conexao=None):
        executar(
            "UPDATE espaco SET nome = %s, descricao = %s, capacidade_maxima = %s, "
            "horario_abertura = %s, horario_fechamento = %s, ativo = %s "
            "WHERE id_espaco = %s",
            (
                espaco.nome,
                espaco.descricao,
                espaco.capacidade_maxima,
                espaco.horario_abertura,
                espaco.horario_fechamento,
                espaco.ativo,
                espaco.id_espaco,
            ),
            conexao,
        )
