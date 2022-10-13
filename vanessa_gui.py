"""  Vanessa Assistant main GUI """
import os.path
import threading
from kivy.app import App
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.widget import Widget
# from kivy.uix.label import Label
# from kivy.uix.image import Image
# from kivy.uix.button import Button
# from kivy.uix.textinput import TextInput
# from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition
from kivy.clock import Clock, ClockBase
from vanessa_assistant import VanessaAssistant as Vanessa
from kivy.core.window import Window
from kivy.animation import Animation
from KivyOnTop import register_topmost, unregister_topmost
from kivy.config import Config

# import itertools
# import glob
# from sys_tray import SysTrayIcon


from pystray import Icon, Menu, MenuItem as Item
from PIL import Image, ImageDraw

from plyer import notification

global try_icon


def create_image(icon):
    return Image.open(icon)


class VanessaUIManager(ScreenManager):
    """ Manage all screen in our app """
    vanessaThread: threading.Thread = None
    assistant: Vanessa = None
    update_interval: ClockBase = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.assistant_listening = None

    def load_assistant(self, **kwargs):
        """ Loading assistant """
        if not self.assistant:
            self.assistant = Vanessa()
        self.screens[0].ids.main_label.text = 'en línea'
        self.update_interval = Clock.schedule_interval(self.update_interface, 0.25)
        self.assistant.listen()

    def update_interface(self, _exact_timing, **_kwargs):
        """ Update main label """
        # if not self.assistant_listening.is_alive():
        self.screens[0].ids.main_label.text = self.assistant.state
        #     self.update_interval.cancel()
        if self.assistant.minimize and self.assistant.on_wind_action:
            vanessa.minimize()
            self.assistant.on_wind_action = False
        elif self.assistant.maximize and self.assistant.on_wind_action:
            vanessa.maximize()
            self.assistant.on_wind_action = False
        elif self.assistant.to_try and self.assistant.on_wind_action:
            vanessa.to_try()
            self.assistant.on_wind_action = False
        elif self.assistant.to_try_off and self.assistant.on_wind_action:
            vanessa.showing()
            self.assistant.on_wind_action = False
        elif self.assistant.focus and not self.assistant.on_wind_action:
            self.assistant.on_wind_action = True
            vanessa.set_focus()
        elif vanessa.close or not self.assistant.alive:
            vanessa.stop()
        else:
            pass
        if self.assistant.speaking or self.assistant.is_online is None:
            if not self.screens[0].animating:
                self.screens[0].animating = True
                self.screens[0].animate_vanessa_border(self.screens[0].ids.vanessa_img.canvas.before.children[0], True)
        else:
            if self.screens[0].animating:
                self.screens[0].animating = False
                self.screens[0].animate_vanessa_border(self.screens[0].ids.vanessa_img.canvas.before.children[0], False)

    def start_assistant(self):
        """ Start assistant """
        if self.assistant_listening:
            self.assistant_listening.join()
        self.assistant_listening = threading.Thread(target=self.load_assistant)
        self.assistant_listening.start()

    def restart_assistant(self, btn):
        """ xds """
        self.start_assistant()

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
            self.vanessa_border_animation = Animation(
                rgba=(1, 0, 1, 1),
                duration=1.5,
            ) + Animation(rgba=(0, 0, 0, 1), duration=3.5)
        else:
            self.vanessa_border_animation.stop(widget)
            self.vanessa_border_animation = Animation(rgba=(0, 0, 0, 1), duration=.5)
        self.vanessa_border_animation.repeat = repeat
        self.vanessa_border_animation.start(widget)


class VanessaSettingsUI(Screen):
    """ Settings Assistant window """
    video_player_text = ''
    music_player_text = ''

    def __init__(self, **kw):
        super().__init__(**kw)

    def set_player_path(self, root, type):
        if not len(root.ids.file_chooser.selection) > 0:
            return
        if type == 'video':
            self.ids.video_player_cfg_btn.text = root.ids.file_chooser.selection[0]
        else:
            self.ids.music_player_cfg_btn.text = root.ids.file_chooser.selection[0]

    def is_sys_file(self, directory, filename):
        return not filename.endswith('.sys') and not filename.endswith('.tmp') and filename.endswith('.exe')


class VanessaAboutUI(Screen):
    """ Settings Assistant window """

    def __init__(self, **kw):
        super().__init__(**kw)


class VanessaRegisterUI(Screen):
    """ Settings Assistant window """

    def __init__(self, **kw):
        super().__init__(**kw)


class VanessaApp(App):
    """ Main Assistant window """
    Window.clearcolor = (1, 1, 1, 1)
    Window.size = (1024, 720)
    __author__ = 'Enmanuel'
    __name__ = 'Vanessa Assistant'
    __version__ = '1.0.0'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.close = False
        self.menu_opt = Menu(
            Item('Cerrar Vanessa', self.exit)
        )
        self.icon = 'assets/vanessa_image.png'
        self.try_icon = Icon(self.__name__, create_image('assets/vanessa.ico'), menu=self.menu_opt)
        self.try_icon.title = f'{self.__name__}\n\nBy {self.__author__}\n\nVersion: {self.__version__}'
        self.on_try = False

    def restart_icon_try(self):
        if self.try_icon is not None:
            self.try_icon.remove_notification()
            if self.try_icon.visible:
                self.try_icon.stop()
            del self.try_icon
            self.try_icon = Icon(self.__name__, create_image('assets/vanessa.ico'), menu=self.menu_opt)
            self.try_icon.title = f'{self.__name__}\n\nBy {self.__author__}\n\nVersion: {self.__version__}'

    def on_start(self):
        """ On App Load """
        Config.set('kivy', 'desktop', 1)
        Config.set('kivy', 'exit_on_escape', 0)
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
        Config.set('graphics', 'minimum_width', 1024)
        Config.set('graphics', 'minimum_height', 720)
        register_topmost(Window, 'Vanessa')
        Config.write()
        self.root.start_assistant()

    def exit(self, xd, **kwargs):
        self.root.assistant.alive = False
        self.try_icon.stop()
        self.close = True

    def showing(self, **kwargs):
        self.restart_icon_try()
        notification.notify(
            app_name="Vanessa Assistant",
            title="Aviso",
            message="Ya no estoy en segundo plano",
            timeout=1
        )
        self.root_window.show()
        self.on_try = False

    def to_try(self):
        self.root_window.hide()
        notification.notify(
            app_name="Vanessa Assistant",
            title="Aviso",
            message="Ya estoy en segundo plano",
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
        self.restart_icon_try()
        self.root_window.restore()
        if self.on_try:
            self.root_window.restore()
            self.on_try = False


vanessa = VanessaApp()
vanessa.run()
