"""  Exit by voice addon """
import random
from assistant import AssistantCore


def start(core: AssistantCore):
    manifest = {
        "name": "Despedida",
        "version": "1.0",
        "require_online": False,

        "commands": {
            "a dios|adiós|Adiós|hasta luego|hasta pronto": play_despedida,
        }
    }
    return manifest


def play_despedida(core: AssistantCore, phrase: str):
    greetings = ['Mi deber ha terminado, un placer haberle servido', 'Ha sido un placer ayudarlo, hasta la próxima', 'Espero que te hallas sentido a gusto conmigo']
    core.say(text_to_speech=greetings[random.randint(0, len(greetings) - 1)])
    core.alive = False
