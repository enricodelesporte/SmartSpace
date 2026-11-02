import re
from datetime import date, datetime

from app.utils.excecoes import ValidacaoErro

PADRAO_EMAIL = re.compile(
    r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,}$"
)
PADRAO_DATA = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PADRAO_HORA = re.compile(r"^\d{2}:\d{2}$")
PADRAO_INTEIRO = re.compile(r"^\d+$", re.ASCII)

TAMANHO_MINIMO_SENHA = 6
TAMANHO_MAXIMO_SENHA_EM_BYTES = 72
TAMANHO_MAXIMO_NOME = 100
TAMANHO_MAXIMO_EMAIL = 150
TAMANHO_MAXIMO_DESCRICAO = 255

ROTULOS_DOS_CAMPOS = {
    "nome": "nome",
    "email": "e-mail",
    "senha": "senha",
    "descricao": "descrição",
    "capacidade_maxima": "capacidade máxima",
    "horario_abertura": "horário de abertura",
    "horario_fechamento": "horário de fechamento",
    "hora_inicio": "hora de início",
    "hora_fim": "hora de fim",
    "data_reserva": "data da reserva",
    "id_espaco": "espaço",
    "data": "data",
}


def rotulo(campo):
    return ROTULOS_DOS_CAMPOS.get(campo, campo)


def validar_nome(valor, campo="nome"):
    if not isinstance(valor, str) or not valor.strip():
        raise ValidacaoErro(f"O campo {rotulo(campo)} é obrigatório")
    texto = valor.strip()
    if len(texto) > TAMANHO_MAXIMO_NOME:
        raise ValidacaoErro(
            f"O campo {rotulo(campo)} deve ter no máximo {TAMANHO_MAXIMO_NOME} caracteres"
        )
    return texto


def validar_email(valor):
    if not isinstance(valor, str) or not valor.strip():
        raise ValidacaoErro("O campo e-mail é obrigatório")
    texto = valor.strip().lower()
    if len(texto) > TAMANHO_MAXIMO_EMAIL or not PADRAO_EMAIL.match(texto):
        raise ValidacaoErro("E-mail em formato inválido")
    return texto


def validar_senha(valor):
    if not isinstance(valor, str):
        raise ValidacaoErro("O campo senha é obrigatório")
    if len(valor) < TAMANHO_MINIMO_SENHA:
        raise ValidacaoErro(
            f"A senha deve ter no mínimo {TAMANHO_MINIMO_SENHA} caracteres"
        )
    if len(valor.encode("utf-8")) > TAMANHO_MAXIMO_SENHA_EM_BYTES:
        raise ValidacaoErro(
            f"A senha deve ter no máximo {TAMANHO_MAXIMO_SENHA_EM_BYTES} bytes"
        )
    return valor


def validar_inteiro_positivo(valor, campo):
    mensagem = f"O campo {rotulo(campo)} deve ser um número inteiro positivo"
    if isinstance(valor, bool):
        raise ValidacaoErro(mensagem)
    if isinstance(valor, int):
        numero = valor
    elif isinstance(valor, str) and PADRAO_INTEIRO.match(valor.strip()):
        numero = int(valor.strip())
    else:
        raise ValidacaoErro(mensagem)
    if numero <= 0:
        raise ValidacaoErro(mensagem)
    return numero


def validar_descricao(valor):
    if valor is None:
        return None
    if not isinstance(valor, str):
        raise ValidacaoErro("O campo descrição deve ser um texto")
    texto = valor.strip()
    if len(texto) > TAMANHO_MAXIMO_DESCRICAO:
        raise ValidacaoErro(
            f"O campo descrição deve ter no máximo {TAMANHO_MAXIMO_DESCRICAO} caracteres"
        )
    return texto or None


def validar_data(valor, campo="data"):
    if not isinstance(valor, str) or not PADRAO_DATA.match(valor.strip()):
        raise ValidacaoErro(f"O campo {rotulo(campo)} deve estar no formato AAAA-MM-DD")
    try:
        return datetime.strptime(valor.strip(), "%Y-%m-%d").date()
    except ValueError:
        raise ValidacaoErro(f"O campo {rotulo(campo)} não é uma data válida")


def validar_hora(valor, campo="hora"):
    if not isinstance(valor, str) or not PADRAO_HORA.match(valor.strip()):
        raise ValidacaoErro(f"O campo {rotulo(campo)} deve estar no formato HH:MM")
    try:
        return datetime.strptime(valor.strip(), "%H:%M").time()
    except ValueError:
        raise ValidacaoErro(f"O campo {rotulo(campo)} não é um horário válido")


def validar_intervalo_horario(
    inicio, fim, mensagem="A hora de fim deve ser maior que a hora de início"
):
    if fim <= inicio:
        raise ValidacaoErro(mensagem)


def validar_data_nao_passada(data, hoje=None):
    referencia = hoje or date.today()
    if data < referencia:
        raise ValidacaoErro("Não é possível reservar em data passada")


def validar_dados_espaco(dados):
    nome = validar_nome(dados.get("nome"))
    descricao = validar_descricao(dados.get("descricao"))
    capacidade = validar_inteiro_positivo(
        dados.get("capacidade_maxima"), "capacidade_maxima"
    )
    abertura = validar_hora(dados.get("horario_abertura"), "horario_abertura")
    fechamento = validar_hora(dados.get("horario_fechamento"), "horario_fechamento")
    validar_intervalo_horario(
        abertura,
        fechamento,
        "O horário de fechamento deve ser maior que o horário de abertura",
    )
    return {
        "nome": nome,
        "descricao": descricao,
        "capacidade_maxima": capacidade,
        "horario_abertura": abertura,
        "horario_fechamento": fechamento,
    }
