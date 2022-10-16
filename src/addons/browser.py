""" Browser addon """
from assistant import AssistantCore
from pywinauto.application import Application
from pywinauto import findwindows, keyboard
from utils.default_app_by_ext import get_default_app_path

global browser_name, browser, browser_window


def start(_core: AssistantCore):
    """ Start """
    manifest = {
        "name": "Control del Navegador",
        "version": "2.0",
        "require_online": True,
        "commands": {
            "navegador|internet": open_browser,
        }
    }
    init_browser()
    return manifest


def init_browser():
    """ Setup """
    global browser, browser_name
    browser = get_default_app_path('url')
    browser_name = browser.split('\\', -1)[-1].split('.')[0]


def get_open_window():
    """ Check if already opened """
    global browser_window
    curr_element = findwindows.find_elements()
    for elem in curr_element:
        if browser_name in elem.name.lower():
            app = Application().connect(handle=elem.handle)
            browser_window = app.window(found_index=0)
            return True
    return False


def open_browser(core: AssistantCore, phrase: str):
    """ Open browser window """
    global browser_window
    already = get_open_window()

    if not core.minimize:
        core.minimize = True
        core.say('Voy a ocultarme para trabajar en el navegador')
    if already:
        set_browser_focus()
        core.say("He detectado que el navegador ya estaba abierto")
    else:
        app = Application(backend="uia").start(browser)
        browser_window = app.window(found_index=0)
        core.say("He iniciado el navegador")

    core.say("Ahora bien, que quieres hacer?")
    core.context_set(control_browser)


def control_browser(core: AssistantCore, phrase: str):
    """ Main browser commands"""
    if not get_browser_focus():
        set_browser_focus()

    if phrase.find("buscar") >= 0 or phrase.find("investigar") >= 0 or phrase.find("estudiar") >= 0:
        # if core.first_use:
        #     core.say("Puedes pedirme a buscar lo que sea, ten en cuenta, que mi buscador predeterminado es google")
        core.say("Bien, que quieres buscar?")
        core.context_set(what_to_search)
    elif phrase.find("iniciar") >= 0 or phrase.find("página") >= 0 or phrase.find("sitio") >= 0:
        core.say("Cual sitio en internet estás buscando?")
        core.context_set(open_site)
    elif phrase.find("nueva pestaña") >= 0:
        keyboard.send_keys('^t')
        core.say("Pestaña creada")
        core.context_set(control_browser)
    elif phrase.find("cerrar pestaña") >= 0:
        keyboard.send_keys('^w')
        core.say("Pestaña cerrada")
        core.context_set(control_browser)
    elif phrase.find("manual de vanessa") >= 0:
        core.say("Abriendo el manual de ayuda en el navegador, estoy al tanto")

    elif phrase.find("cerrar navegador") >= 0:
        keyboard.send_keys("^+w")
        core.say("Navegador cerrado")
        core.context_clear()
    elif phrase.find("salir") >= 0:
        core.focus = True
        core.say('Ok terminamos con el navegador, y ahora que necesitas?')
        core.context_clear()
    else:
        core.say("Comando del navegador no encontrado, para conocer todos los comandos disponibles diga: manual de vanessa")
        core.context_set(control_browser)


def what_to_search(core: AssistantCore, phrase: str):
    """ Searching in browser """
    if not get_browser_focus():
        set_browser_focus()
    keyboard.send_keys('^l')
    default_search_engine = 'www.google.com/search?q='
    typing = phrase.split(' ', -1)
    if phrase.find("video") >= 0 or phrase.find("vídeo") >= 0:
        final_search = default_search_engine + ' {SPACE}'.join(typing) + '&source=lnms&tbm=vid' + '{ENTER}'
    elif phrase.find("fotos") >= 0 or phrase.find("imágenes") >= 0:
        final_search = default_search_engine + ' {SPACE}'.join(typing) + '&source=lnms&tbm=isch' + '{ENTER}'
    elif phrase.find("noticias") >= 0 or phrase.find("eventos") >= 0:
        final_search = default_search_engine + ' {SPACE}'.join(typing) + '&source=lnms&tbm=nws' + '{ENTER}'
    elif phrase.find("libro") >= 0 or phrase.find("literatura") >= 0:
        final_search = default_search_engine + ' {SPACE}'.join(typing) + '&source=lnms&tbm=bks' + '{ENTER}'
    elif phrase.find("mapa") >= 0 or phrase.find("ubicación") >= 0 or phrase.find("localización") >= 0:
        final_search = 'https://www.google.com/maps/search/' + ' {SPACE}'.join(typing) + '{ENTER}'
    else:
        final_search = default_search_engine + ' {SPACE}'.join(typing) + '&source=lnms&hl=es' + '{ENTER}'
    keyboard.send_keys(final_search)
    core.say("Buscando en google " + ' '.join(typing))
    core.context_set(control_browser)


def open_site(core: AssistantCore, phrase):
    """ Opening some sites """
    if not get_browser_focus():
        set_browser_focus()
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
    elif phrase.find("cancelar") >= 0 or phrase.find("salir") >= 0:
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


# Browser windows actions
def set_browser_focus():
    """ Set focus on browser """
    wrapper = browser_window.wrapper_object()
    wrapper.set_focus()


def get_browser_focus():
    """ Get browser focus """
    wrapper = browser_window.wrapper_object()
    return wrapper.has_focus()
