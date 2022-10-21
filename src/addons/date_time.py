""" Date and time """
from datetime import datetime
from assistant import AssistantCore
from lingua_franca.format import nice_date, nice_time


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
    now = datetime.now()
    txt = f"Hoy es {weekdays[now.weekday()]}; {str(now.day)} del mes {now.month}; del {now.year}"
    core.say(txt)


def play_time(core: AssistantCore, phrase: str):
    now = datetime.time(datetime.now())
    txt = nice_time(now, use_ampm=True)
    core.say(txt)
