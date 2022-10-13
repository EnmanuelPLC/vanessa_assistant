from datetime import datetime
from utils.num_to_text_ru import num2text
from assistant import AssistantCore
import os
from lingua_franca.format import nice_date, nice_date_time, nice_time

modname = os.path.basename(__file__)[:-3]  # calculating modname


def start(core: AssistantCore):
    manifest = {
        "name": "Fecha y hora",
        "version": "1.2",
        "require_online": False,

        "default_options": {
            "sayNoon": False,
            "skipUnits": False,
            "unitsSeparator": ", ",
            "skipMinutesWhenZero": True,
        },

        "commands": {
            "hoy": play_date,
            "hora": play_time,
        }
    }
    return manifest


def start_with_options(core: AssistantCore, manifest: dict):
    pass


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
