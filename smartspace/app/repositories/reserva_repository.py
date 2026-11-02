from app.database import consultar, consultar_um, executar
from app.models.reserva import Reserva

SELECT_COM_NOMES = (
    "SELECT r.*, e.nome AS nome_espaco, u.nome AS nome_usuario "
    "FROM reserva r "
    "JOIN espaco e ON e.id_espaco = r.id_espaco "
    "JOIN usuario u ON u.id_usuario = r.id_usuario "
)


class ReservaRepository:
    def buscar_por_id(self, id_reserva, conexao=None):
        registro = consultar_um(
            SELECT_COM_NOMES + "WHERE r.id_reserva = %s", (id_reserva,), conexao
        )
        return Reserva.a_partir_do_registro(registro) if registro else None

    def listar_confirmadas_do_espaco_na_data(self, id_espaco, data_reserva, conexao=None):
        registros = consultar(
            "SELECT * FROM reserva "
            "WHERE id_espaco = %s AND data_reserva = %s AND status = %s",
            (id_espaco, data_reserva, Reserva.CONFIRMADA),
            conexao,
        )
        return [Reserva.a_partir_do_registro(registro) for registro in registros]

    def listar_do_usuario(self, id_usuario, conexao=None):
        registros = consultar(
            SELECT_COM_NOMES
            + "WHERE r.id_usuario = %s ORDER BY r.data_reserva DESC, r.hora_inicio DESC",
            (id_usuario,),
            conexao,
        )
        return [Reserva.a_partir_do_registro(registro) for registro in registros]

    def listar_todas(self, id_espaco=None, data_reserva=None, conexao=None):
        condicoes = []
        parametros = []
        if id_espaco is not None:
            condicoes.append("r.id_espaco = %s")
            parametros.append(id_espaco)
        if data_reserva is not None:
            condicoes.append("r.data_reserva = %s")
            parametros.append(data_reserva)
        filtro = "WHERE " + " AND ".join(condicoes) + " " if condicoes else ""
        registros = consultar(
            SELECT_COM_NOMES + filtro + "ORDER BY r.data_reserva DESC, r.hora_inicio DESC",
            tuple(parametros),
            conexao,
        )
        return [Reserva.a_partir_do_registro(registro) for registro in registros]

    def criar(self, reserva, conexao=None):
        return executar(
            "INSERT INTO reserva (id_usuario, id_espaco, data_reserva, "
            "hora_inicio, hora_fim, status) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                reserva.id_usuario,
                reserva.id_espaco,
                reserva.data_reserva,
                reserva.hora_inicio,
                reserva.hora_fim,
                reserva.status,
            ),
            conexao,
        )

    def atualizar_status(self, reserva, conexao=None):
        executar(
            "UPDATE reserva SET status = %s WHERE id_reserva = %s",
            (reserva.status, reserva.id_reserva),
            conexao,
        )
