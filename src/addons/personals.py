""" Personal talking addon """
import os
import random
from assistant import AssistantCore


def start(core: AssistantCore):
    manifest = {
        "name": "Personal Questions",
        "version": "1.0",
        "require_online": False,

        "commands": {
            "como estas|cómo estás|como estás|cómo estas": how_are_you,
            "manual de uso|abre el manual": vanessa_doc,
            "quién eres": i_am
        }
    }
    return manifest


def i_am(core: AssistantCore, phrase: str):
    core.say("Yo soy vanessa, tu asistente personal virtual, que te ayudara en tus tareas diarias")


def how_are_you(core: AssistantCore, phrase: str):
    say = [
        "Yo estoy bien, y tu?",
        "Muy bién, gracias, y tu como estás?"
    ]
    core.say(say[random.randint(0, len(say) - 1)])
    core.context_set(talking)


def vanessa_doc(core: AssistantCore, phrase: str):
    core.say("Abriendo el manual")
    os.startfile('..\\assets\\manual.pdf')


def talking(core: AssistantCore, phrase: str):
    if phrase.find('bien') >= 0:
        core.say('Que bueno escuchar eso, y mejor todavía si estoy aquí para ayudarte, a que si?')
        core.context_clear()
    elif phrase.find('mal') >= 0:
        core.say('Y eso porqué, cuéntame, que te pasa; a lo mejor te puedo ayudar')
        core.context_set(talking_issues)
    else:
        core.say(f'Oye; o estas bien, o estas mal, no me quieras confundir')


def talking_issues(core: AssistantCore, phrase: str):
    if phrase.find('problemas') >= 0:
        core.say('A, pero eso es normal, todo el mundo tiene problemas, que quieres que te diga')
    pass
