import random
from assistant import AssistantCore
import webbrowser
from winreg import HKEY_LOCAL_MACHINE, HKEY_CURRENT_USER, OpenKey, QueryValueEx, ConnectRegistry
from pywinauto.application import Application
from pywinauto import findwindows, keyboard
from utils.default_app_by_ext import get_default_app_path


def start(core: AssistantCore):
    manifest = {
        "name": "Control del Navegador",
        "version": "1.0",
        "require_online": True,
        "commands": {
            "navegador|internet": open_browser,
        }
    }
    init_browser()
    return manifest


def init_browser():
    global browser_name, browser
    browser = get_default_app_path('url')
    browser_name = browser.split('\\', -1)[-1].split('.')[0]


def open_browser(core: AssistantCore, phrase: str):
    global browser_name, app
    already = False
    curr_element = findwindows.find_elements()
    for element in curr_element:
        if element.name.find(browser_name) > 0 or element.name.find(browser_name.capitalize()) > 0:
            already = True
            curr_element = element
            break

    if already:
        app = Application().connect(handle=curr_element._handle)
        win = app.window()
        win.backend.dialog_class.set_focus(win)
        core.say("He detectado que el navegador ya estaba abierto")
    else:
        app = Application(backend="uia").start(browser)
        core.say("He iniciado el navegador")

    core.say("Bien, ahora dime, que deseas hacer en él?")
    core.context_set(control_browser)


def control_browser(core: AssistantCore, phrase: str):
    if phrase.find("buscar") >= 0:
        core.say("Dime lo que deseas buscar, y dónde lo quieres buscar")
        core.say("Ejemplo: los partidos de football mas emocionantes de este año, en google")
        core.context_set(what_to_search)
    elif phrase.find("iniciar web") >= 0:
        core.say("Cual web estás buscando?")
        core.context_set(open_site)
    elif phrase.find("nueva pestaña") >= 0:
        keyboard.send_keys('^t')
        core.say("Pestaña creada")
        core.context_set(control_browser)
    elif phrase.find("cerrar pestaña") >= 0:
        keyboard.send_keys('^w')
        core.say("Pestaña cerrada")
        core.context_set(control_browser)
    elif phrase.find("comandos del navegador") >= 0:
        core.say("Actualmente los comandos son: buscar; nueva pestaña; cerrar pestaña; cerrar navegador; salir; iniciar web")
        core.context_set(control_browser)
    elif phrase.find("cerrar navegador") >= 0:
        keyboard.send_keys("^+w")
        core.say("Navegador cerrado")
        core.context_clear()
    elif phrase.find("salir") >= 0:
        core.say("Bien, cuando necesites mi ayuda solo di mi nombre")
        core.context_clear()
    else:
        core.say("Comando del navegador no encontrado, para conocer los comandos disponibles diga: comandos del navegador")
        core.context_set(control_browser)


def what_to_search(core: AssistantCore, phrase: str):
    keyboard.send_keys('^l')
    if phrase.find("en google") > 0:
        search = phrase.split('google', -1)[1]
        if len(search) == 0:
            search = phrase.split('en google', -1)[0]
        typing = search.split(' ', -1)
        keyboard.send_keys('{SPACE}'.join(typing))
        keyboard.send_keys('{ENTER}')
        core.say("Buscando en google " + search)
    elif phrase.find("en youtube") > 0:
        search = phrase.split('en youtube', -1)[1]
        if len(search) == 0:
            search = phrase.split('en youtube')[0]
        typing = search.split(' ', -1)
        keyboard.send_keys('www.youtube.com/results?search_query='+'{SPACE}'.join(typing))
        keyboard.send_keys('{ENTER}')
        core.say("Buscando en youtube " + search)
    elif phrase.find("cancelar") >= 0:
        core.say("Búsqueda cancelada, volviendo a comandos del navegador")
        core.context_set(control_browser)
    else:
        core.say("Debes buscar algo en los sitios soportados, hasta ahora son, google y youtube")
        core.context_set(what_to_search)


def open_site(core: AssistantCore, phrase):
    keyboard.send_keys('^l')
    if phrase.find("facebook") >= 0:
        keyboard.send_keys('www.facebook.com')
        core.say("Abriendo facebook")
    elif phrase.find("whatsapp") >= 0:
        keyboard.send_keys('web.whatsapp.com')
        core.say("Abriendo whatsapp")
    elif phrase.find("correo uci") >= 0:
        keyboard.send_keys('correo.estudiantes.uci.cu')
        core.say("Abriendo correo uci")
    elif phrase.find("twitter") >= 0:
        keyboard.send_keys('www.twitter.com')
        core.say("Abriendo twitter")
    elif phrase.find("correo") >= 0:
        keyboard.send_keys('www.gmail.com')
        core.say("Abriendo correo gmail")
    elif phrase.find("cancelar") >= 0:
        core.say("Abrir sitios cancelados")
        core.context_set(control_browser)
        return
    else:
        if phrase.find("punto com") > 0 or phrase.find("en cuba") > 0:
            web = phrase.find("punto com") > 0
            arr_doms = {"punto com": ".com", "en cuba": ".cu"}
            if web < 0:
                find = ''
            else:
                find = "punto com"
            while not web:
                find = phrase.find("punto com")
                if find < 0:
                    find = "en cuba"
                else:
                    find = "punto com"

            web = phrase.split(find)[0]
            keyboard.send_keys(web + arr_doms[find])
            core.say("Abriendo web")
        else:
            core.say("Sitio no configurado")
            core.context_set(open_site)
            return

    keyboard.send_keys('{ENTER}')
    core.context_set(open_site)
