"""  Vanessa Assistant main GUI """
import threading

from kivy import Config
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock, ClockBase
from vanessa_assistant import VanessaAssistant as Vanessa
from kivy.core.window import Window
from kivy.animation import Animation
from KivyOnTop import register_topmost
from pystray import Icon, Menu, MenuItem as Item
from PIL import Image
from plyer import notification


def create_image(icon):
    return Image.open(icon)


class VanessaUIManager(ScreenManager):
    """ Manage all screen in our app """
    vanessaThread: threading.Thread = None
    assistant: Vanessa = None
    update_interval: ClockBase = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.load_cfg = False
        self.current_sc = None
        self.assistant_listening = None
        self.start_assistant()

    def load_assistant(self, **kwargs):
        """ Loading assistant """
        if not self.assistant:
            self.assistant = Vanessa()
        self.screens[0].ids.main_label.text = 'en línea'
        self.update_interval = Clock.schedule_interval(self.update_interface, 0.25)
        if self.assistant.first_use:
            self.first_time_used()
        self.assistant.listen()

    def update_interface(self, _exact_timing, **_kwargs):
        """ Update main label """
        if self.current == 'settings' and not self.load_cfg:
            if self.screens[1].ids.user_name_input.text != self.assistant.user['name']:
                self.screens[1].ids.user_name_input.text = self.assistant.user['name']
                self.load_cfg = True

        if self.current == 'main_screen':
            self.screens[0].ids.main_label.text = self.assistant.state
            if self.assistant.speaking or self.assistant.is_online is None:
                if not self.screens[0].animating:
                    self.screens[0].animating = True
                    self.screens[0].animate_vanessa_border(self.screens[0].ids.vanessa_img.canvas.before.children[0], True)
            else:
                if self.screens[0].animating:
                    self.screens[0].animating = False
                    self.screens[0].animate_vanessa_border(self.screens[0].ids.vanessa_img.canvas.before.children[0], False)
        if self.assistant.minimize:
            vanessa.minimize()
            self.assistant.on_wind_action = 'minimize'
            self.assistant.minimize = False
        elif self.assistant.maximize:
            vanessa.maximize()
            self.assistant.on_wind_action = 'maximize'
            self.assistant.maximize = False
        elif self.assistant.to_try:
            vanessa.to_try()
            self.assistant.on_wind_action = 'to_try'
            self.assistant.to_try = False
        elif self.assistant.to_try_off:
            vanessa.showing()
            self.assistant.on_wind_action = 'to_try_off'
            self.assistant.to_try_off = False
        elif self.assistant.focus:
            vanessa.set_focus()
            self.assistant.on_wind_action = 'focus'
            self.assistant.focus = False
        elif vanessa.close or not self.assistant.alive:
            vanessa.stop()
        else:
            pass

        if self.current_sc == 'settings':
            self.current = 'settings'
            self.current_sc = None

    def first_time_used(self):
        """ Setup assistant instance """
        self.assistant.say('Hola, yo soy vanessa, tu asistente de voz personal que te ayudará en la interacción con los dispositivos de cómputo')
        self.assistant.say('Para empezar solo necesito saber tu nombre')
        self.current_sc = 'settings'

        # self.start_assistant()

    def start_assistant(self):
        """ Start assistant """
        if self.assistant_listening:
            self.assistant_listening.join()
        self.assistant_listening = threading.Thread(target=self.load_assistant)
        self.assistant_listening.start()

    def stop_assistant(self, btn=None):
        """ Stop assistant """
        self.assistant.alive = False


class VanessaMainUI(Screen):
    """ MAIN GUI CLASS """

    def __init__(self, **kw):
        super().__init__(**kw)
        self.vanessa_border_animation = None
        self.animating = False

    def animate_vanessa_border(self, widget, repeat):
        if repeat:
            self.vanessa_border_animation = Animation(rgba=(1, 0, 1, 1), duration=.5)
        else:
            self.vanessa_border_animation.stop(widget)
            self.vanessa_border_animation = Animation(rgba=(0, 0, 0, 1), duration=.5)
        self.vanessa_border_animation.repeat = repeat
        self.vanessa_border_animation.start(widget)

    def effect_off_btn(self, typ='on', *args):
        img = args[0][0]
        if typ == 'on':
            anim = Animation(opacity=.5, duration=.25)
        else:
            anim = Animation(opacity=1, duration=.25)
        anim.start(img)


class VanessaSettingsUI(Screen):
    """ Settings Assistant window """
    video_player_text = ''
    music_player_text = ''

    def __init__(self, **kw):
        super().__init__(**kw)

    def save_user_name(self, name, *_arg):
        self.parent.assistant.config.save('user', 'name', name)
        self.parent.assistant.first_use = False
    # def set_player_path(self, root, type):
    #     if len(root.ids.file_chooser.selection) > 0:
    #         if type == 'video':
    #             vanessa.root.assistant.user['favorite_app_paths']['video_player'] = root.ids.file_chooser.selection[0]
    #         elif type == 'music':
    #             vanessa.root.assistant.user['favorite_app_paths']['music_player'] = root.ids.file_chooser.selection[0]
    #         else:
    #             vanessa.root.assistant.user['favorite_app_paths']['text_editor'] = root.ids.file_chooser.selection[0]
    #
    # def is_exe_and_not_sys_file(self, directory, filename):
    #     return not filename.endswith('.sys') and not filename.endswith('.tmp') and filename.endswith('.exe')
    #
    # def update_file_list_entry(self, args):
    #     file_text_1 = args[1].children[0]
    #     file_text_2 = args[1].children[1]
    #     file_text_1.color = file_text_2.color = (0, 0, 0, 1)


class VanessaAboutUI(Screen):
    """ Settings Assistant window """

    def __init__(self, **kw):
        super().__init__(**kw)


class VanessaRegisterUI(Screen):
    """ Settings Assistant window """

    def __init__(self, **kw):
        super().__init__(**kw)


class VanessaApp(App):
    """ Vanessa Assistant App """
    Window.clearcolor = (1, 1, 1, 1)
    Window.size = (512, 700)
    __author__ = 'Enmanuel'
    __name__ = 'Vanessa Assistant'
    __version__ = '1.0.0'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.close = False
        self.menu_opt = Menu(Item('Cerrar Vanessa', self.exit))
        self.icon = 'assets/images/vanessa_image.png'
        self.try_icon = Icon(self.__name__, create_image('assets/icons/vanessa.ico'), menu=self.menu_opt)
        self.try_icon.title = f'{self.__name__}\n\nBy {self.__author__}\n\nVersion: {self.__version__}'
        self.on_try = False

    def restart_icon_try(self):
        if self.try_icon is not None:
            self.try_icon.remove_notification()
            if self.try_icon.visible:
                self.try_icon.stop()
            del self.try_icon
            self.try_icon = Icon(self.__name__, create_image('assets/icons/vanessa.ico'), menu=self.menu_opt)
            self.try_icon.title = f'{self.__name__}\n\nBy {self.__author__}\n\nVersion: {self.__version__}'

    def on_start(self):
        """ On App Load """
        Config.set('kivy', 'desktop', 1)
        Config.set('kivy', 'exit_on_escape', 0)
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
        Config.set('graphics', 'minimum_width', 512)
        Config.set('graphics', 'minimum_height', 700)
        Config.write()
        register_topmost(Window, 'Vanessa')

    def exit(self, _xd=None, **kwargs):
        self.root.assistant.alive = False
        if _xd:
            self.try_icon.stop()
        self.close = True

    def showing(self, **kwargs):
        self.restart_icon_try()
        notification.notify(
            app_name="Vanessa Assistant",
            title="Aviso",
            message="Estoy devuelta contigo",
            timeout=1
        )
        self.root_window.show()
        self.on_try = False

    def to_try(self):
        self.root_window.hide()
        notification.notify(
            app_name="Vanessa Assistant",
            title="Aviso",
            message="Ahora estoy en segundo plano",
            timeout=1
        )
        self.on_try = True
        self.root_window.hide()
        self.try_icon.run_detached()

    def minimize(self):
        self.restart_icon_try()
        self.root_window.minimize()
        if self.on_try:
            self.root_window.minimize()
            self.on_try = False

    def maximize(self):
        self.restart_icon_try()
        self.root_window.maximize()
        if self.on_try:
            self.root_window.maximize()
            self.on_try = False

    def set_focus(self):
        if not self.try_icon:
            self.restart_icon_try()
        self.root_window.restore()
        if self.on_try:
            self.root_window.restore()
            self.on_try = False


vanessa = VanessaApp()
vanessa.run()
