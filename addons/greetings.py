import random
from assistant import AssistantCore


def start(core: AssistantCore):
    manifest = {
        "name": "Greetings",
        "version": "1.0",
        "require_online": False,

        "commands": {
            "hola|buenas tardes": play_greetings,
        }
    }
    return manifest


def play_greetings(core: AssistantCore, phrase: str):
    greetings = [
        "Hola " + phrase + ", en qué te puedo ayudar?"
    ]
    core.say(greetings[random.randint(0, len(greetings) - 1)])
    core.context_set(core.commands)
