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
            "hoy": play_date,
            "hora": play_time,
        }
    }
    return manifest


def play_date(core: AssistantCore, phrase: str):
    now = datetime.now()
    txt = "Hoy es " + nice_date(now, 'es')
    txt_arr = txt.split(',', -1)
    txt_arr[0] += ","
    txt_arr[1] = txt_arr[1].strip()
    temp2 = txt_arr[1].split(' ', 1)
    temp2.reverse()
    txt_arr[1] = ' de '.join(temp2)
    txt_arr[2] = " del año " + str(now.year)
    core.say(' '.join(txt_arr))


def play_time(core: AssistantCore, phrase: str):
    now = datetime.time(datetime.now())
    txt = nice_time(now, use_ampm=True)
    core.say(txt)
