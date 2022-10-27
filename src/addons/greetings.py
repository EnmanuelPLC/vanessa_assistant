import random
from datetime import datetime

from assistant import AssistantCore


def start(core: AssistantCore):
    manifest = {
        "name": "Greetings",
        "version": "1.0",
        "require_online": False,

        "commands": {
            "hola|buenos días|buenas tardes": play_greetings,
        }
    }
    return manifest


def play_greetings(core: AssistantCore, phrase: str):
    now: datetime.time = datetime.time(datetime.now())
    if now.hour <= 6:
        greeting = f"Es muy temprano en la mañana {core.user['name']}"
    elif 6 < now.hour <= 12:
        greeting = f"Buenos días {core.user['name']}"
    elif 12 < now.hour < 20:
        greeting = f"Buenas tardes {core.user['name']}"
    elif 20 <= now.hour < 24:
        greeting = f"Buenas noches {core.user['name']}"
    else:
        greeting = f"Buenas {core.user['name']}"
    serv_arr = [f'{greeting}, en que puedo servirle?', f'{greeting}, que puedo hacer por tí?', f'{greeting}, qué hacemos hoy?', f'{greeting}, que quieres hacer?']
    core.say(serv_arr[random.randint(0, len(serv_arr) - 1)])
    core.context_set(core.commands)
