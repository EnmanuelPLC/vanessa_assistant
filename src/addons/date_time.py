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
    import time
    t = time.strftime("%I:%M %p")
    fir = t.split(":")
    hour = int(fir[0])
    min = int(fir[1].split(' ')[0])
    tz = fir[1].split(' ')[1]
    now = [hour, min, tz]
    txt = ''
    if now[0] > 1:
        if now[0] > 12:
            txt += f'Son las {now[0] % 12} y {now[1]} '
        else:
            txt += f'Son las {now[0]} y {now[1]} '
    else:
        if now[0] == 0:
            txt += f'Son las 12 y {now[1]} '
        else:
            txt += f'Son la una y {now[1]} '
    if now[0] > 1:
        txt += 'minutos '
    else:
        txt += 'minuto '
    if now[2] == 'AM':
        txt += 'de la mañana'
    else:
        if now[0] < 20:
            txt += 'de la tarde'
        else:
            txt += 'de la noche'
    core.say(txt)
