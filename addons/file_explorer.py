import random
from assistant import AssistantCore


def start(core: AssistantCore):
    manifest = {
        "name": "Explorador de archivos",
        "version": "1.0",
        "require_online": False,

        "commands": {
            "abre los archivos": open_file_explorer,
        }
    }
    return manifest


def open_file_explorer(core: AssistantCore, phrase: str):
    print(phrase)
    core.say('Ok')
