""" Vanessa Assistant """
import random
import sys
import json
import queue
import traceback
import sounddevice as sd
import vosk

from assistant import AssistantCore as Assistant
from config import AssistantConf


class VanessaAssistant(Assistant):
    """ Vanessa Wrapper Class """
    __name__ = 'Vanessa'
    __version__ = '1.0.0'
    __author__ = 'EnmanuelPLC'
    q = queue.Queue()
    model = 'model'
    vosk_model = None
    samplerate = None
    dev = True

    def __init__(self):
        super().__init__()
        self.device = sd.query_devices(kind='input')
        self.samplerate = int(self.device['default_samplerate'])
        if self.dev:
            self.model = 'model_es_small'
        self.vosk_model = vosk.Model(self.model)
        self.voice_recognition = vosk.KaldiRecognizer(self.vosk_model, self.samplerate)
        self.config = AssistantConf()
        self.first_use = self.config.first_use
        if not self.first_use:
            self.user['name'] = self.config.read('user', 'name')
        self.init_with_addons()
        print('#' * 25)
        print('Asistente en línea!!')
        print('#' * 25)

    def listen(self):
        """ Listen method """
        try:
            with sd.RawInputStream(samplerate=self.samplerate, blocksize=4096, dtype='int16', channels=1, callback=self.callback):
                init_say = ['Estoy en línea, y entonces, que tienes en mente?', 'Es un placer estar aquí para ti',
                            'Estoy lista para la acción, solo di mi nombre', 'Que gusto volver a estar contigo, que vamos hacer ahora?',
                            'Aquí estoy de nuevo, que tienes pensado para hoy?']
                self.say(init_say[random.randint(0, len(init_say) - 1)])
                self.state = 'escuchando . . .'
                self.online_check.start()
                while self.alive:
                    data = self.q.get()
                    if self.voice_recognition.AcceptWaveform(bytes(data)):
                        recognized_data = self.voice_recognition.Result()
                        recognized_data = json.loads(recognized_data)
                        voice_input_str = recognized_data["text"]

                        if voice_input_str and voice_input_str != "":
                            self.run_input_str(voice_input_str, self.block_mic)
                            self.mic_blocked = False
                    else:
                        pass
                    if not self.first_use and self.user['name'] != self.config.read('user', 'name'):
                        self.user['name'] = self.config.read('user', 'name')
            print('Vanessa Terminated')
            exit(0)

        except KeyboardInterrupt:
            print('\nDone')
            sys.exit(0)
        except Exception as err:
            print(traceback.format_exc())
            print(type(err).__name__ + ': ' + str(err))
            sys.exit(-1)

    def callback(self, indata, _frames, _time, status):
        """
        :param indata:
        :param _frames:
        :param _time:
        :param status:
        """
        if status:
            print(status, file=sys.stderr)
        if not self.mic_blocked:
            self.q.put(indata)
