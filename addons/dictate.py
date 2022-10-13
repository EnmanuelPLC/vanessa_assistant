import random
from assistant import AssistantCore
from pywinauto import keyboard
from winreg import HKEY_CLASSES_ROOT, HKEY_LOCAL_MACHINE, OpenKey, QueryValueEx, ConnectRegistry
from lingua_franca.parse import extract_numbers


def get_default_doc_app():
    """
    :return:
    """
    registry_default_doc_path = r'.doc'
    launch_path = ""
    with OpenKey(HKEY_CLASSES_ROOT, registry_default_doc_path) as key:
        doc_app_name, _ = QueryValueEx(key, None)

    if len(doc_app_name) > 0:
        with OpenKey(ConnectRegistry(None, HKEY_LOCAL_MACHINE), r"SOFTWARE\Classes\{}\shell\open\command".format(doc_app_name)) as key:
            launch_path, _ = QueryValueEx(key, "")

    return launch_path.split('"', -1)[1]


def start(core: AssistantCore):
    """
    :param core:
    :return:
    """
    manifest = {
        "name": "Dictar",
        "version": "1.0",
        "require_online": False,

        "commands": {
            "dictar|dictado": play_dictate,
        }
    }
    return manifest


def play_dictate(core: AssistantCore, phrase: str):
    """
    :param core:
    :param phrase:
    """
    core.say("Bien, dime donde quieres empezar el dictado?")
    core.say("Puedes elegir entre: archivo de texto; y documento word ")
    core.context_set(choose_dictation)


def choose_dictation(core: AssistantCore, phrase: str):
    """
    :param core:
    :param phrase:
    """
    if phrase == "archivo de texto":
        from pywinauto.application import Application
        app = Application(backend="uia").start('notepad.exe')
    elif phrase == "documento word":
        from pywinauto.application import Application
        path = get_default_doc_app()
        app = Application(backend="uia").start(path)
    else:
        core.say("Iniciando dictado en la ventana actual")
    core.say("Modo dictado activado")
    core.context_set(start_dictate)

sep = ''


def start_dictate(core: AssistantCore, phrase: str):
    """

    :param core:
    :param phrase:
    :return:
    """
    global sep

    if phrase.find("cancelar") < 0:
        if phrase.find("nueva línea") >= 0:
            sep = ''
            keyboard.send_keys('{ENTER}')
        elif phrase.find("escribir números") >= 0:
            core.say("Ok, di el número")
            core.context_set(dictate_number)
            return
        else:
            typing = phrase.split(' ', -1)
            keyboard.send_keys(sep + '{SPACE}'.join(typing))
            sep = '{SPACE}'
        core.context_set(start_dictate)
    else:
        core.say("Modo dictado cancelado")


def dictate_number(core: AssistantCore, phrase: str):
    """

    :param core:
    :param phrase:
    """
    if phrase.find("cancelar") >= 0:
        core.say("De vuelta a dictado de palabras")
        core.context_set(start_dictate)
    elif phrase.find("nueva línea") >= 0:
        keyboard.send_keys('{ENTER}')
        core.context_set(dictate_number)
    else:
        try:
            number = extract_numbers(phrase)
            keyboard.send_keys(str(number[0]))
            print(number)
        except Exception as e:
            print(e)
            core.say("No entendí bien el número, por favor repítemelo")
        finally:
            core.context_set(dictate_number)
