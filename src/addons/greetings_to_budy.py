import random
from assistant import AssistantCore


def start(core: AssistantCore):
    manifest = {
        "name": "Greetings to budy",
        "version": "1.0",
        "require_online": False,

        "commands": {
            "saluda|saludame|di hola": play_greeting,
        }
    }
    return manifest


def play_greeting(core: AssistantCore, phrase: str):
    phrase = phrase.split('a ', -1)
    if len(phrase) > 1:
        phrase = phrase[1]
    else:
        phrase = phrase[0]
    greetings = "hola " + phrase + ";"
    greets_arr = ["como estás?", "dime que me trajiste algo; jajajaj era broma, Enmanuel se pone mongólico y me programa estas boberias", "que me cuentas de nuevo", "dime algo bueno"]
    greetings += greets_arr[random.randint(0, len(greets_arr) - 1)]
    core.say(greetings)
    core.context_set(continue_greeting_on_ctx)


def continue_greeting_on_ctx(core: AssistantCore, phrase: str):
    if phrase.find("bien") >= 0 or phrase.find("bién") >= 0 or phrase.find("regular") >= 0 or phrase.find("más o menos") >= 0:
        core.say("que bueno, me alegro que todo este bien contigo")
        core.say("si tienes algo que decirme o preguntare, metele, ahora es tu momento")
        core.context_set(continue_greeting_on_ctx)
    # elif phrase.find() > 0:
    #     pass
    # elif phrase.find() > 0:
    #     pass
    # elif phrase.find() > 0:
    #     pass
    # elif phrase.find() > 0:
    #     pass
    # elif phrase.find() > 0:
    #     pass
