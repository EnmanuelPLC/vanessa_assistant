from date_time import datetime
from assistant import AssistantCore
import random


def start(core: AssistantCore):
    """

    :param core:
    :return:
    """
    manifest = {
        "name": "Juego de adivinar",
        "version": "1.0",
        "require_online": False,

        "commands": {
            "jugar": play_game_start,
        }
    }
    return manifest


questNumber = -1
tries = 0


def play_game_start(core: AssistantCore, phrase: str):
    """

    :param core:
    :param phrase:
    """
    core.say("Okey, para jugar, di, reglas del juego")
    core.context_set(play_1)


def play_1(core: AssistantCore, phrase: str):
    """

    :param core:
    :param phrase:
    :return:
    """
    if phrase == "reglas del juego":
        core.say("Yo pienso en un número del 1 al 100, luego dices un número, y yo digo si el número que dijiste, es mayor, o menor al que yo pense; Tienes que adivinar el número en 7 intentos. Di iniciar para comenzar.")
        core.context_set(play_1)
        return
    if phrase == "empezar" or phrase == "iniciar" or phrase == "repetir":
        global questNumber, tries
        questNumber = random.randint(1, 100)
        tries = 0
        core.say("Okey, empieza adivinar!")
        core.context_set(play_2)
        return

    if phrase == "cancelar" or phrase == "salir":
        core.say("Okey, que hacemos ahora?")
        return

    core.say("Di iniciar para comenzar, o cancelar para salir.")
    core.context_set(play_1)


def play_2(core: AssistantCore, phrase: str):
    """

    :param core:
    :param phrase:
    :return:
    """
    from utils.num_to_text_ru import num2text
    for i in range(1, 100):
        numTxt = num2text(i)
        if phrase == numTxt:
            global tries
            tries += 1
            if i == questNumber:
                core.say("Lo has adivinado. ¡Felicitaciones por la victoria!, Di repetir si quieres volver a jugar.")
                core.context_set(play_1)
                return
            else:
                txtsay = ""
                if tries >= 7:
                    txtsay += "Has hecho 7 intentos, lamentablemente has perdido. Yo he salido victoriosa, el número era " + str(questNumber)
                    txtsay += "; Di repetir si quieres volver a jugar, o cancelar si deseas salir."
                    core.say(txtsay)
                    core.context_set(play_1)
                    return
                else:
                    if i < questNumber:
                        txtsay += "El número es mayor. "
                    else:
                        txtsay += "El número es menor. "
                    core.say(txtsay)
                    core.context_set(play_2)
                    return

    core.say("No entendí el número, dímelo de nuevo.!")
    core.context_set(play_2)
