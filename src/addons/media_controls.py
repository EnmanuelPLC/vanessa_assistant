""" Media controls """
import pyautogui
from random import randint
from assistant import AssistantCore

responses = ['ok', 'hecho']


def start(core: AssistantCore):
    """
    :param core:
    :return:
    """
    manifest = {
        "name": "Comandos de control para multimedia",
        "version": "2",
        "require_online": False,

        "commands": {
            "empieza|play|pausa": play_pause,
            "siguiente": play_next,
            "anterior": play_prev,
            "parar|quitar": play_stop,
            "silenciar|apagar sonido": toggle_mute,
            "bajar volumen|reducir volumen": (volume_downX, 5),
            "subir volumen|aumentar volumen": (volume_upX, 5),
            "cerrar vídeo|cerrar video|quitar video| quitar reproducción|cerrar reproductor|cerrar música": close,
            "adelantar": forward,
            "atrasar": backward,
        }
    }

    return manifest


def play_pause(core: AssistantCore, phrase: str):
    """
    :param core:
    :param phrase:
    """
    pyautogui.press("playpause")
    core.say(responses[randint(0, len(responses) - 1)])


def play_stop(core: AssistantCore, phrase: str):
    """
    :param core:
    :param phrase:
    """
    pyautogui.press("stop")
    core.say(responses[randint(0, len(responses) - 1)])


def play_next(core: AssistantCore, phrase: str):
    """
    :param core:
    :param phrase:
    """
    pyautogui.press("nexttrack")
    core.say('Hecho')


def play_prev(core: AssistantCore, phrase: str):
    """
    :param core:
    :param phrase:
    """
    pyautogui.press("prevtrack")
    core.say(responses[randint(0, len(responses) - 1)])


def toggle_mute(core: AssistantCore, phrase: str):
    """
    :param core:
    :param phrase:
    """
    pyautogui.press("volumemute")
    core.say(responses[randint(0, len(responses) - 1)])


def volume_upX(core: AssistantCore, phrase: str, param: int):
    """
    :param core:
    :param phrase:
    :param param:
    """
    for i in range(param):
        pyautogui.press("volumeup")
    core.say(responses[randint(0, len(responses) - 1)])


def volume_downX(core: AssistantCore, phrase: str, param: int):
    """
    :param core:
    :param phrase:
    :param param:
    """
    for i in range(param):
        pyautogui.press("volumedown")
    core.say(responses[randint(0, len(responses) - 1)])


def forward(core: AssistantCore, phrase: str):
    """
    :param core:
    :param phrase:
    """
    pyautogui.press("right")
    core.say(responses[randint(0, len(responses) - 1)])


def backward(core: AssistantCore, phrase: str):
    """
    :param core:
    :param phrase:
    """
    pyautogui.press("left")
    core.say(responses[randint(0, len(responses) - 1)])


def close(core: AssistantCore, phrase: str):
    """
    :param core:
    :param phrase:
    """
    pyautogui.hotkey('alt', 'f4')
    core.say(responses[randint(0, len(responses) - 1)])
