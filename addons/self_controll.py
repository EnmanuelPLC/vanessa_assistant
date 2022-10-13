import random
from assistant import AssistantCore
from kivy.core.window import Window


def start(core: AssistantCore):
    manifest = {
        "name": "Control de ventana propia",
        "version": "1.0",
        "require_online": False,

        "commands": {
            "segundo plano|desaparece": system_try,
            "primer plano|aparece": system_try_off,
            "minimiza": minimize,
            "maximiza": maximize,
            "ventana": focus
        }
    }
    return manifest


def system_try(core: AssistantCore, phrase: str):
    if not core.to_try:
        core.to_try = core.on_wind_action = True
        core.say('Ahora estoy en segundo plano, para volver di, primer plano')
        core.context_set(core.commands)
    else:
        core.say('Papa por dios, ya estoy en segundo plano, que pretendes, volverme loca')


def system_try_off(core: AssistantCore, phrase: str):
    if core.to_try:
        core.to_try = False
        core.to_try_off = core.on_wind_action = True
        core.say('Ya estoy de vuelta contigo, que tienes en mente ahora?')
        core.context_set(core.commands)
    else:
        core.say('Si seras pendejo, pero ya estoy en primer plano, pretendes confundirme o que')


def focus(core: AssistantCore, phrase: str):
    core.focus = True
    core.say('Aqui estoy otra vez')
    core.context_set(core.commands)
    core.focus = core.on_wind_action = not core.focus


def minimize(core: AssistantCore, phrase: str):
    core.minimize = True
    core.say('Minimizandome')
    core.context_set(core.commands)
    core.minimize = core.on_wind_action = not core.minimize


def maximize(core: AssistantCore, phrase: str):
    core.maximize = True
    core.say('Maximizandome')
    core.context_set(core.commands)
    core.maximize = core.on_wind_action = not core.maximize
