""" Core assistant logic """
import threading
from datetime import datetime
# General import
import random
import traceback
import urllib.request
import time
from threading import Timer
from termcolor import colored, cprint
import pyttsx3
from lingua_franca import load_language, set_default_lang

# Locals imports
from addon_engine import AddonEngine

load_language('es')
set_default_lang('es')

version = "1.0.0"
author = "EnmanuelPLC"


class AssistantCore:
    """ Assistant Core Class """

    def __init__(self):
        self.alive = True
        self.is_online = None
        self.online_check = threading.Thread(target=self.check_internet)
        self.log_policy = 'all'
        self.assistant_listen_names = "vanesa|vanessa|vane".split('|')
        self.addons_req_online = ()
        self.state = ''
        self.user = {
            'name': 'Enmanuel',
            'favorite_app_paths': {
                'music_player': '',
                'video_player': '',
                'text_editor': ''
            }
        }
        self.minimize = self.maximize = self.to_try = self.to_try_off = self.focus = False
        self.on_wind_action = 'focus'
        self.mic_blocked = False
        self.addons_engine = AddonEngine()
        self.activation_error_counter = 3
        self.speaking = False
        self.commands = {}
        self.plugin_commands = {}
        self.cmd_not_found = "Comando no encontrado"
        self.cmd_not_found_in_ctx = "Comando no encontrado en contexto"
        self.cmd_online_reminder = "No tienes conexión a internet, recuerda que este comando necesita internet para algunas funciones"
        self.media_player_path = ""
        self.version = version
        self.tts_engine = pyttsx3.init()
        self.log_policy = "all"
        self.last_say = ""
        self.last_action = ""
        self.context = None
        self.context_timer = None
        self.context_default_duration = 30

    def block_mic(self):
        """ Block mick """
        self.mic_blocked = True

    def check_internet(self, host='https://www.google.com'):
        """ Check connectivity """
        while self.alive:
            try:
                urllib.request.urlopen(host)
                if not self.is_online:
                    self.say('Conexión a internet detectada')
                    self.is_online = True
                    self.update_addon_manifest()
            except ConnectionError as e:
                if self.is_online:
                    self.say('Conexión a internet perdida')
                    self.is_online = False
                    self.update_addon_manifest()
            if self.is_online is None:
                self.is_online = False
            time.sleep(60)

    def commands_ctx(self, command, context):
        """
        :param context:
        :param command:
        :return:
        """
        try:
            for all_keys in context.keys():
                keys = all_keys.split("|")
                for key in keys:
                    if command == key:
                        if key == 'hola':
                            rest_phrase = 'Enmanuel'
                        else:
                            rest_phrase = ""
                        next_context = context[all_keys]
                        if isinstance(next_context, dict) and next_context['warn']:
                            next_context['warn']()
                            next_context = next_context['cmd']
                        self.execute_next(rest_phrase, next_context)
                        return

            for all_keys in context.keys():
                keys = all_keys.split("|")
                for key in keys:
                    if command.find(key) >= 0:
                        rest_phrase = command[(len(key) + 1):]
                        next_context = context[all_keys]
                        self.execute_next(rest_phrase, next_context)
                        return

            if isinstance(self.context, dict):
                self.say(self.cmd_not_found)
                self.context_clear()
            else:
                self.say(self.cmd_not_found_in_ctx)
                if self.context_timer is not None:
                    self.context_set(self.context, self.context_default_duration)
            self.state = 'escuchando . . .'
        except Exception as err:
            print(err)
            print(traceback.format_exc())

    @staticmethod
    def format_print_key_list(key: str, value: list):
        """
        :param key:
        :param value:
        """
        print(colored(key + ": ", "blue") + ", ".join(value))

    def init_with_addons(self):
        """ Initiate load of addons starting with the core """
        self.init_addons()
        self.display_init_info()
        self.setup_assistant_voice()

    def init_addons(self):
        """ Load and setup of all addons """
        from os import listdir
        from os.path import isfile, join
        addon_path = self.addons_engine.addon_engine_root_folder + "/addons"
        files = [f for f in listdir(addon_path) if isfile(join(addon_path, f))]

        for file in files:
            if file.endswith(".py"):
                addon_ready = self.addons_engine.init_addon(file[:-3])
                if not addon_ready:
                    raise Exception('Error loading addon')
                else:
                    mod_name = addon_ready[0]
                    res = addon_ready[1]
                    self.process_addon_manifest(mod_name, res)
                    self.addons_engine.addon_manifests[mod_name] = res
                    cprint(f"Addon: {res['name']} {res['version']} ({mod_name}) started!")

    def update_addon_manifest(self):
        """ Update manifest addons """
        from os import listdir
        from os.path import isfile, join
        addon_path = self.addons_engine.addon_engine_root_folder + "/addons"
        files = [f for f in listdir(addon_path) if isfile(join(addon_path, f))]

        for addon_req_online in self.addons_req_online:
            for file in files:
                if file.endswith(".py") and file[:-3] == addon_req_online:
                    addon_ready = self.addons_engine.init_addon(addon_req_online)
                    if addon_ready:
                        mod_name = addon_ready[0]
                        res = addon_ready[1]
                        self.process_addon_manifest(mod_name, res)
                        self.addons_engine.addon_manifests[mod_name] = res
                        cprint(f"Addon: {res['name']} {res['version']} ({mod_name}) updated!")
                    else:
                        cprint(f"Addon: {addon_req_online} not updated!")

    def process_addon_manifest(self, modname, manifest):
        """
        :param modname:
        :param manifest:
        """
        plugin_req_online = True
        if "require_online" in manifest:
            plugin_req_online = manifest["require_online"]
            if plugin_req_online:
                if modname not in self.addons_req_online:
                    self.addons_req_online += (modname,)

        if "commands" in manifest:
            for cmd in manifest["commands"].keys():
                if not self.is_online and plugin_req_online:
                    self.commands[cmd] = {'cmd': manifest["commands"][cmd], 'warn': self.stub_online_required}
                else:
                    self.commands[cmd] = manifest["commands"][cmd]

                if modname in self.plugin_commands:
                    self.plugin_commands[modname].append(cmd)
                else:
                    self.plugin_commands[modname] = [cmd]

    def stub_online_required(self):
        """ Say need online to proper functionality of addon """
        self.say(self.cmd_online_reminder)

    def print_error(self, err_txt, e: Exception | None = None):
        """
        :param err_txt:
        :param e:
        """
        self.print_red(err_txt)
        traceback.print_exc()

    @staticmethod
    def print_red(txt):
        """
        :param txt:
        """
        cprint(txt, "red")

    def setup_assistant_voice(self):
        """ Setting up assistant voice engine """
        try:
            voices = self.tts_engine.getProperty("voices")
            if isinstance(voices, list):
                for voice in voices:
                    if voice.id.find('SABINA') > 0:
                        self.tts_engine.setProperty("voice", voice.id)

            rate = int(self.tts_engine.getProperty("rate").__str__())
            self.tts_engine.setProperty("rate", rate - 50)
            self.tts_engine.setProperty("volume", 1.0)
        except Exception as e:
            self.print_error("Error setting up TTS (tts_engine)", e)
            from sys import platform
            if platform == "linux" or platform == "linux2":
                cprint("Only windows is supported by now", "red")
            elif platform == "darwin":
                cprint("Only windows is supported by now", "red")
            elif platform == "win32":
                pass

    def say(self, text_to_speech: str):
        """
        :param: text_to_speech:
        """
        if self.tts_engine._inLoop:
            self.tts_engine.endLoop()
        self.last_say = text_to_speech
        self.speaking = True
        self.state = 'hablando'
        self.tts_engine.say(text_to_speech)
        self.tts_engine.startLoop(False)
        self.tts_engine.iterate()
        self.speaking = False

    @staticmethod
    def all_num_to_text(text: str):
        """
        :param text:
        :return:
        """
        from utils.all_num_to_text import all_num_to_text
        return all_num_to_text(text)

    def execute_next(self, command, context):
        """
        :param command:
        :param context:
        :return:
        """
        if context is None:
            if command == 'activation':
                now: datetime.time = datetime.time(datetime.now())
                if now.hour <= 6:
                    greeting = f"Es muy temprano en la mañana {self.user['name']}"
                elif 6 < now.hour <= 12:
                    greeting = f"Buenos días {self.user['name']}"
                elif 12 < now.hour < 20:
                    greeting = f"Buenas tardes {self.user['name']}"
                elif 20 <= now.hour < 24:
                    greeting = f"Buenas noches {self.user['name']}"
                else:
                    greeting = f"Buenas {self.user['name']}"
                serv_arr = [f'{greeting}, en que puedo servirle?', f'{greeting}, que puedo hacer por tí?', f'{greeting}, qué hacemos hoy?']
                self.say(serv_arr[random.randint(0, len(serv_arr) - 1)])
                self.context_set(self.commands, 15)
                return
            elif command == '':
                return
            else:
                context = self.commands

        if not isinstance(context, dict):
            self.context_clear()
            self.call_ext_func_phrase(command, context)
            return

        self.commands_ctx(command, context)

    def call_ext_func(self, func_param):
        """
        :param func_param:
        """
        if isinstance(func_param, tuple):
            func_param[0](self, func_param[1])
        else:
            func_param(self)

    def call_ext_func_phrase(self, phrase, func_param):
        """
        :param phrase:
        :param func_param:
        """
        if isinstance(func_param, tuple):
            func_param[0](self, phrase, func_param[1])
        else:
            func_param(self, phrase)

    def run_input_str(self, voice_input_str, func_before_run_cmd=None):
        """
        :param voice_input_str:
        :param func_before_run_cmd:
        :return:
        """
        have_run = False

        if self.context is None:
            print("Input: ", voice_input_str)
        else:
            if isinstance(self.context, dict):
                print("Input (in commands context): ", voice_input_str)
            else:
                print("Input (in {} context)".format(self.context.__name__), voice_input_str)

        try:
            voice_input = voice_input_str.split(" ")
            have_run = False
            command_options = ''
            if self.context is None:
                if voice_input[0] in self.assistant_listen_names or voice_input[0] == 'hola' and len(voice_input) > 1 and voice_input[1] in self.assistant_listen_names:
                    command_options = 'activation'
                    print("Input (Assistant Activation): ", voice_input_str)
                if func_before_run_cmd is not None:
                    func_before_run_cmd()
                self.execute_next(command_options, None)
                have_run = True
            else:
                if func_before_run_cmd is not None:
                    func_before_run_cmd()
                self.execute_next(voice_input_str, self.context)
                have_run = True
        except Exception as e:
            print(e)
            print(traceback.format_exc())

        return have_run

    def context_set(self, context, duration=None):
        """
        :param context:
        :param duration:
        """
        self.state = 'esperando comando'
        if duration is None:
            duration = self.context_default_duration
        self.context_clear()
        self.context = context
        self.context_timer = Timer(duration, self._context_clear_timer, args=[self.block_mic])
        self.context_timer.start()

    def _context_clear_timer(self, func):
        if func:
            func()
        self.contextTimer = None
        if isinstance(self.context, dict):
            self.say('Si me llamas y no me dices nada, existen 2 opciones, una es que estás indeciso al ver que soy capaz de hacer muchas cosas, o te intriga lo que te pueda decir; a que si')
        elif isinstance(self.context, object):
            self.say('Bueno parece que ya no me necesitas; recuerda que estoy aquí para lo que sea')
        else:
            self.say('He limpiado el contexto de forma rara')
            print(self.context)
            print(type(self.context))
        self.mic_blocked = False
        self.context_clear()

    def context_clear(self):
        """ Clearing current context """
        self.context = None
        if self.context_timer is not None:
            self.context_timer.cancel()
            self.context_timer = None

    def display_init_info(self):
        """ Displays all info """
        cprint("AssistantCore v{0}:".format(version), "blue", end=' ')
        print("Running " + "[ONLINE]" if self.is_online else "[OFFLINE]" + " mode")

        print("TTS engine", self.tts_engine.__str__())
        self.format_print_key_list("Assistant names", self.assistant_listen_names)

        cprint("Commands list: " + "#" * 65, "blue")
        for plugin in self.plugin_commands:
            self.format_print_key_list(plugin, self.plugin_commands[plugin])
        cprint("#" * 80, "blue")
