""" Do nothing """
import random
from assistant import AssistantCore


def start(core: AssistantCore):
    manifest = {
        "name": "Do nothing",
        "version": "1.0",
        "require_online": False,

        "commands": {
            "nada|cancela|sal|salir|negativo|no": do_nothing,
        }
    }
    return manifest


def do_nothing(core: AssistantCore, phrase: str):
    if core.context == core.commands:
        nothings = ['Esta bien', 'vale', 'okey', 'recibido']
        core.say(text_to_speech=nothings[random.randint(0, len(nothings) - 1)])
        core.context_clear()
