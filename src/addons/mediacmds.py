import pyautogui
from assistant import AssistantCore


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
            "cerrar vídeo|cerrar música": close,
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
    print("Reproduccion en pausa")
    pyautogui.press("playpause")


def play_stop(core: AssistantCore, phrase: str):
    """
    :param core:
    :param phrase:
    """
    print("Reproduccion detenida")
    pyautogui.press("stop")


def play_next(core: AssistantCore, phrase: str):
    """
    :param core:
    :param phrase:
    """
    print("Reproducir siguiente")
    pyautogui.press("nexttrack")


def play_prev(core: AssistantCore, phrase: str):
    """
    :param core:
    :param phrase:
    """
    print("Reproducir anterior")
    pyautogui.press("prevtrack")


def toggle_mute(core: AssistantCore, phrase: str):
    """
    :param core:
    :param phrase:
    """
    pyautogui.press("volumemute")


def volume_upX(core: AssistantCore, phrase: str, param: int):
    """
    :param core:
    :param phrase:
    :param param:
    """
    for i in range(param):
        pyautogui.press("volumeup")


def volume_downX(core: AssistantCore, phrase: str, param: int):
    """
    :param core:
    :param phrase:
    :param param:
    """
    for i in range(param):
        pyautogui.press("volumedown")


def forward(core: AssistantCore, phrase: str):
    """
    :param core:
    :param phrase:
    """
    print('Adelantando reproduccion')
    pyautogui.press("right")


def backward(core: AssistantCore, phrase: str):
    """
    :param core:
    :param phrase:
    """
    print('Adelantando reproduccion')
    pyautogui.press("left")


def close(core: AssistantCore, phrase: str):
    """
    :param core:
    :param phrase:
    """
    print('Reproduccion cerrada')
