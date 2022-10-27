"""  Direct search on Google """
import random

from addons.browser import what_to_search
from assistant import AssistantCore


def start(core: AssistantCore):
    manifest = {
        "name": "Direct Search",
        "version": "1.0",
        "require_online": False,

        "commands": {
            "buscar|búsqueda|búscame|busca": direct_search,
        }
    }
    return manifest


def direct_search(core: AssistantCore, phrase: str):
    core.say("Bien")
    what_to_search(core, phrase)
