MARCADOR_DE_TEXTO_CORROMPIDO = "\u251c"
CODIFICACAO_DO_PROMPT_WINDOWS = "cp850"


def corrigir_texto_corrompido(texto):
    if not texto or MARCADOR_DE_TEXTO_CORROMPIDO not in texto:
        return texto
    try:
        return texto.encode(CODIFICACAO_DO_PROMPT_WINDOWS).decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return texto
