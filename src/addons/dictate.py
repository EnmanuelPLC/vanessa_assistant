""" Dictation addon"""
from assistant import AssistantCore
from pywinauto import keyboard
from lingua_franca.parse import extract_numbers
from utils.default_app_by_ext import get_default_app_path


def start(_core: AssistantCore):
    """
    :param _core:
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


def play_dictate(core: AssistantCore, _phrase: str):
    """
    :param core:
    :param _phrase:
    """
    core.say("Bien, donde quieres empezar el dictado?")
    core.say("Puedes elegir entre: archivo de texto, documento word; o en la ventana actual ")
    core.context_set(choose_dictation)


def choose_dictation(core: AssistantCore, phrase: str):
    """
    :param core:
    :param phrase:
    """
    if phrase == "archivo de texto":
        from pywinauto.application import Application
        Application(backend="uia").start('notepad.exe')
    elif phrase == "documento word":
        from pywinauto.application import Application
        path = get_default_app_path('doc')
        Application(backend="uia").start(path)
    else:
        core.say("Iniciando dictado en la ventana actual")
    core.say("A partir de ahora, todo lo que digas lo escribiré en esta ventana")
    core.context_set(start_dictate)


def start_dictate(core: AssistantCore, phrase: str):
    """
    :param core:
    :param phrase:
    :return:
    """
    if phrase.find("cancelar") < 0 and phrase.find("salir") < 0:
        if phrase.find("nueva línea") >= 0 or phrase.find("enter") >= 0:
            keyboard.send_keys('{ENTER}')
            core.context_set(start_dictate)
        elif phrase.find("modo números") >= 0 or phrase.find("escribe números") >= 0:
            core.say("Bien, di el número")
            core.context_set(dictate_number)
        elif phrase.find("signos") >= 0 or phrase.find("caracteres especiales") >= 0:
            core.say("Bien, dime el signo")
            core.context_set(dictate_signs)
        elif phrase.find("borrar") >= 0:
            if phrase.find("línea") >= 0:
                keyboard.send_keys('^x')
            else:
                keyboard.send_keys('{BKSP}')
            core.context_set(start_dictate)
        else:
            keyboard.send_keys(phrase + '{SPACE}', with_spaces=True)
            core.context_set(start_dictate)
    else:
        core.say("Modo dictado cancelado")
        core.context_clear()


def dictate_number(core: AssistantCore, phrase: str):
    """
    :param core:
    :param phrase:
    """
    if phrase.find("cancelar") >= 0 or phrase.find("salir") >= 0:
        core.say("De vuelta a dictado de palabras")
        core.context_set(start_dictate)
    elif phrase.find("nueva línea") >= 0 or phrase.find("enter") >= 0:
        keyboard.send_keys('{ENTER}')
        core.context_set(dictate_number)
    else:
        try:
            number = extract_numbers(phrase)
            keyboard.send_keys(str(number[0]))
        except Exception as e:
            print(e)
            core.say("No entendí bien el número, por favor, asegurate de que no existan ruidos, y habla fuerte y claro")
        finally:
            core.context_set(dictate_number)


def dictate_signs(core: AssistantCore, phrase: str):
    """
    :param core:
    :param phrase:
    """
    if phrase.find("cancelar") >= 0 or phrase.find("salir") >= 0:
        core.say("De vuelta a dictado de palabras")
        core.context_set(start_dictate)
        return
    elif phrase.find("espacio") >= 0:
        keyboard.send_keys('{SPACE}')
    elif phrase.find("punto") >= 0:
        if phrase.find("punto y coma") >= 0:
            keyboard.send_keys(';')
        elif phrase.find("dos puntos") >= 0:
            keyboard.send_keys(':')
        else:
            keyboard.send_keys('.')
    elif phrase.find("coma") >= 0:
        keyboard.send_keys(',')
    elif phrase.find("exclamación") >= 0:
        if phrase.find("abrir") >= 0 or phrase.find("abre") >= 0:
            keyboard.send_keys('¡')
        else:
            keyboard.send_keys('!')
    elif phrase.find("interrogación") >= 0:
        if phrase.find("abrir") >= 0 or phrase.find("abre") >= 0:
            keyboard.send_keys('¿')
        else:
            keyboard.send_keys('?')
    elif phrase.find("paréntesis") >= 0:
        if phrase.find("abrir") >= 0 or phrase.find("abre") >= 0:
            keyboard.send_keys('{(}')
        else:
            keyboard.send_keys('{)}')
    elif phrase.find("llave") >= 0:
        if phrase.find("abrir") >= 0 or phrase.find("abre") >= 0:
            keyboard.send_keys('{{}')
        else:
            keyboard.send_keys('{}}')
    elif phrase.find("corchete") >= 0:
        if phrase.find("abrir") >= 0 or phrase.find("abre") >= 0:
            keyboard.send_keys('{[}')
        else:
            keyboard.send_keys('{]}')
    elif phrase.find("asterisco") >= 0 or phrase.find("por") >= 0:
        keyboard.send_keys('*')
    elif phrase.find("numeral") >= 0:
        keyboard.send_keys('#')
    elif phrase.find("peso") >= 0 or phrase.find("dólar") >= 0:
        keyboard.send_keys('$')
    elif phrase.find("arroba") >= 0:
        keyboard.send_keys('@')
    elif phrase.find("por ciento") >= 0:
        keyboard.send_keys('{%}')
    elif phrase.find("y") >= 0 and len(phrase) < 4:
        if phrase.find("inglesa") >= 0:
            keyboard.send_keys('&')
        else:
            keyboard.send_keys('{^}')
    elif phrase.find("igual") >= 0:
        keyboard.send_keys('=')
    elif phrase.find("mayor") >= 0:
        keyboard.send_keys('{>}')
    elif phrase.find("menor") >= 0:
        keyboard.send_keys('<')
    elif phrase.find("más") >= 0:
        keyboard.send_keys('{+}')
    elif phrase.find("menos") >= 0:
        keyboard.send_keys('-')
    elif phrase.find("comilla") >= 0:
        if phrase.find("simple") >= 0:
            keyboard.send_keys("''")
        else:
            keyboard.send_keys('""')
        keyboard.send_keys("{LEFT}")
    elif phrase.find('barra') >= 0:
        if phrase.find('diagonal') >= 0:
            if phrase.find('izquierda') >= 0:
                keyboard.send_keys("\\")
            else:
                keyboard.send_keys('/')
        else:
            keyboard.send_keys('|')
    else:
        core.say('No entendí el signo')
    core.context_set(dictate_signs)
