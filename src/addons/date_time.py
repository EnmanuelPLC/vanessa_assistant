""" Date and time """
from datetime import datetime
from assistant import AssistantCore


def start(core: AssistantCore):
    manifest = {
        "name": "Fecha y hora",
        "version": "1.2",
        "require_online": False,

        "commands": {
            "a como estamos hoy|hoy que es|fecha": play_date,
            "hora|el reloj": play_time,
        }
    }
    return manifest


def play_date(core: AssistantCore, phrase: str):
    weekdays = ['Lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    months = ['Enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    now = datetime.now()
    txt = f"Hoy es {weekdays[now.weekday()]}; {str(now.day)} de {months[now.month - 1]}; del {now.year}"
    core.say(txt)


def play_time(core: AssistantCore, phrase: str):
    now = datetime.time(datetime.now())
    txt = ''
    if now.hour > 1:
        if now.hour > 12:
            txt += f'Son las {now.hour % 12} y {now.minute} '
        else:
            txt += f'Son las {now.hour} y {now.minute} '
    else:
        txt += f'Son la {now.hour} y {now.minute} '
    if now.minute > 1:
        txt += 'minutos '
    else:
        txt += 'minuto '
    if now.tzinfo == 'AM':
        txt += 'de la mañana'
    else:
        if now.hour < 20:
            txt += 'de la tarde'
        else:
            txt += 'de la noche'
    core.say(txt)
