from datetime import time, timedelta


def para_time(valor):
    if isinstance(valor, time):
        return valor
    if isinstance(valor, timedelta):
        total_segundos = int(valor.total_seconds())
        return time(
            (total_segundos // 3600) % 24,
            (total_segundos % 3600) // 60,
            total_segundos % 60,
        )
    return time.fromisoformat(str(valor))


def formatar_hora(valor):
    return valor.strftime("%H:%M")
