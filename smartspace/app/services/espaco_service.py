from app.models.espaco import Espaco
from app.repositories.espaco_repository import EspacoRepository
from app.utils.excecoes import NaoEncontradoErro, ValidacaoErro
from app.utils.validadores import validar_dados_espaco


class EspacoService:
    def __init__(self, repositorio=None):
        self._espacos = repositorio or EspacoRepository()

    def listar_ativos(self):
        return self._espacos.listar_ativos()

    def buscar(self, id_espaco):
        espaco = self._espacos.buscar_por_id(id_espaco)
        if espaco is None:
            raise NaoEncontradoErro("Espaço não encontrado")
        return espaco

    def cadastrar(self, dados):
        campos = validar_dados_espaco(dados)
        espaco = Espaco(**campos)
        espaco.id_espaco = self._espacos.criar(espaco)
        return self.buscar(espaco.id_espaco)

    def editar(self, id_espaco, dados):
        espaco = self.buscar(id_espaco)
        dados_atuais = espaco.para_dicionario()
        dados_mesclados = {**dados_atuais, **dados}
        campos = validar_dados_espaco(dados_mesclados)
        espaco.atualizar_dados(**campos)
        self._espacos.atualizar(espaco)
        return espaco

    def desativar(self, id_espaco):
        espaco = self.buscar(id_espaco)
        if not espaco.ativo:
            raise ValidacaoErro("Este espaço já está desativado")
        espaco.desativar()
        self._espacos.atualizar(espaco)
        return espaco
