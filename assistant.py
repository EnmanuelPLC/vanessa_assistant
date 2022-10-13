""" Core assistant logic """
import threading
from datetime import datetime
# General import
import os
import random
import traceback
import hashlib
import urllib.request
import time
from threading import Timer
from termcolor import colored, cprint
import pyttsx3
from lingua_franca import load_language, set_default_lang, parse

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
        self.online_check = threading.Thread(target=self.check_internet, args=(self,))
        self.log_policy = 'all'
        self.assistant_listen_names = "vanesa|vanessa|vane".split('|')
        self.state = ''
        self.user = {
            "name": 'Enmanuel',
            'favorite_app_paths': {
                'music_player': '',
                'video_player': '',
                'text_editor': ''
            }
        }
        self.minimize = self.maximize = self.to_try = self.to_try_off = self.focus = self.on_wind_action = False
        self.mic_blocked = False
        self.addons_engine = AddonEngine()
        self.activation_error_counter = 3
        self.speaking = False
        self.commands = {}
        self.plugin_commands = {}
        self.cmd_not_found = "Comando no encontrado"
        self.cmd_not_found_in_ctx = "Comando no encontrado en contexto"
        self.cmd_online_reminder = "Recuerda que este comando para funcionar correctamente necesita internet"
        self.media_player_path = ""
        self.version = version
        self.tts_engine = "pyttsx"
        self.log_policy = "all"
        self.last_say = ""
        self.last_action = ""
        self.context = None
        self.context_timer = None
        self.context_default_duration = 30

    def block_mic(self):
        """ Block mick """
        self.mic_blocked = True

    @staticmethod
    def check_internet(self, host='https://www.google.com'):
        while self.alive:
            try:
                urllib.request.urlopen(host)
                if not self.is_online:
                    self.say('Conexión a internet detectada')
                    self.is_online = True
                    self.update_addons_manifiest()
            except Exception as e:
                if self.is_online:
                    self.say('Conexión a internet perdida')
                    self.is_online = False
                    self.update_addons_manifiest()
            if self.is_online is None:
                self.is_online = False

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
        """ Load addon """
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

    def update_addons_manifiest(self):
        self.init_addons()

    def process_addon_manifest(self, modname, manifest):
        """
        :param modname:
        :param manifest:
        """
        plugin_req_online = True
        if "require_online" in manifest:
            plugin_req_online = manifest["require_online"]

        if "commands" in manifest:
            for cmd in manifest["commands"].keys():
                if not self.is_online and plugin_req_online:
                    self.commands[cmd] = self.stub_online_required
                else:
                    self.commands[cmd] = manifest["commands"][cmd]

                if modname in self.plugin_commands:
                    self.plugin_commands[modname].append(cmd)
                else:
                    self.plugin_commands[modname] = [cmd]

    def stub_online_required(self, core, phrase):
        """
        :param core:
        :param phrase:
        """
        self.say(self.cmd_online_reminder)

    def print_error(self, err_txt, e: Exception|None = None):
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

    # ----------- text-to-speech functions ------
    def setup_assistant_voice(self):
        """
        Setting up assistant voice engine
        """
        try:
            self.tts_engine = pyttsx3.init()
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

    # -------- main function ----------
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

    def call_ext_func(self, funcparam):
        """
        :param funcparam:
        """
        if isinstance(funcparam, tuple):
            funcparam[0](self, funcparam[1])
        else:
            funcparam(self)

    def call_ext_func_phrase(self, phrase, funcparam):
        """
        :param phrase:
        :param funcparam:
        """
        if isinstance(funcparam, tuple):
            funcparam[0](self, phrase, funcparam[1])
        else:
            funcparam(self, phrase)

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
                print("Input (in comands context) - ", voice_input_str)
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
        # if self.context.__name__ == "commands_ctx":
        #     self.say('Si me llamas y no me dices nada, existen 2 opciones, una es que estás indeciso al ver que soy capaz de hacer muchas cosas, o dos, te intriga lo que te pueda decir; a que si')
        self.context_clear()
        print("Contexto limpiado, vanessa vuelve a su estado 'escuchando'")
        self.mic_blocked = False

    def context_clear(self):
        """
        Clearing current context
        """
        self.context = None
        if self.context_timer is not None:
            self.context_timer.cancel()
            self.context_timer = None

    # ----------- display info functions ------
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
        self.online_check.start()
