""" File explorer addon """
import os
from assistant import AssistantCore
import subprocess
import locale

global doc_folder, down_folder, images_folder, music_folder, video_folder

en_folder = ['Documents', 'Downloads', 'Images', 'Music', 'Videos']
es_folder = ['Documentos', 'Descargas', 'Imágenes', 'Música', 'Videos']


def init_file_explorer():
    global doc_folder, down_folder, images_folder, music_folder, video_folder
    lang = locale.getdefaultlocale()
    if 'es' in lang[0]:
        user_lang_folder = es_folder
    else:
        user_lang_folder = en_folder
    user_dir = f"C:{os.environ['HOMEPATH']}\\"

    doc_folder = user_dir + user_lang_folder[0]
    down_folder = user_dir + user_lang_folder[1]
    images_folder = user_dir + user_lang_folder[2]
    music_folder = user_dir + user_lang_folder[3]
    video_folder = user_dir + user_lang_folder[4]


def start(core: AssistantCore):
    manifest = {
        "name": "Explorador de archivos",
        "version": "1.0",
        "require_online": False,

        "commands": {
            "los archivos|las carpetas": open_file_explorer,
            "abre documentos|mis documentos|abre los documentos": open_doc_folder,
            "abre descargas|mis descargas|abre las descargas": open_down_folder,
            "abre imágenes|mis imágenes|abre las imágenes": open_images_folder,
            "abre música|mi música|abre la música": open_music_folder,
            "abre videos|mis videos|abre los videos": open_video_folder,
        }
    }
    init_file_explorer()
    return manifest


def open_file_explorer(core: AssistantCore, phrase: str):
    core.say('Abriendo el explorador de archivos')
    subprocess.Popen('explorer.exe')


def open_doc_folder(core: AssistantCore, phrase: str):
    subprocess.Popen(f'explorer.exe {doc_folder}')
    core.say('Abriendo documentos')


def open_down_folder(core: AssistantCore, phrase: str):
    subprocess.Popen(f'explorer.exe {down_folder}')
    core.say('Abriendo las descargas')


def open_images_folder(core: AssistantCore, phrase: str):
    subprocess.Popen(f'explorer.exe {images_folder}')
    core.say('Abriendo las imágenes')


def open_music_folder(core: AssistantCore, phrase: str):
    subprocess.Popen(f'explorer.exe {music_folder}')
    core.say('Abriendo tu carpeta de música')
    core.say('Quieres escuchar una canción?')
    core.context_set(play_random_music)


def open_video_folder(core: AssistantCore, phrase: str):
    subprocess.Popen(f'explorer.exe {video_folder}')
    core.say('Abriendo tu carpeta de videos')
    core.say('Quieres ver un video?')
    core.context_set(play_random_video)


def play_random_music(core: AssistantCore, phrase: str):
    if phrase.find('si') >= 0 or phrase.find('ok') >= 0 or phrase.find('está bien') >= 0 or phrase.find('afirmativo') >= 0:
        core.say('Seleccionando una, al azar, jajajá, o eso es lo que tu crees')
        music = get_random_file(music_folder, 'music')
        os.startfile(music_folder + f'\\{music}')
    elif phrase.find('no') >= 0 or phrase.find('ne') >= 0 or phrase.find('negativo') >= 0:
        core.say('Esta bien, cualquier cosa, aquí estoy a su disposición')
    else:
        core.say('Responde si, o no;')
        core.context_set(play_random_music)


def play_random_video(core: AssistantCore, phrase: str):
    if phrase.find('si') >= 0 or phrase.find('ok') >= 0 or phrase.find('está bien') >= 0 or phrase.find('afirmativo') >= 0:
        core.say('Seleccionando uno, al azar, jajajá, o eso es lo que tu crees')
        video = get_random_file(video_folder, 'video')
        os.startfile(video_folder + f'\\{video}')
    elif phrase.find('no') >= 0 or phrase.find('ne') >= 0 or phrase.find('negativo') >= 0:
        core.say('Esta bien, cualquier cosa, aquí estoy a su disposición')
    else:
        core.say('Responde si, o no;')
        core.context_set(play_random_video)


def get_random_file(path, typ = None):
    from os import listdir
    from os.path import join, isfile
    import random

    if typ == 'video':
        ext = ['m4v', 'mp4', 'mkv', 'mpg', 'mpeg', 'avi', '3gp']
    else:
        ext = ['mp3', 'm4r', 'm4a', 'wav', 'ogg']
    files = [f for f in listdir(path) if isfile(join(path, f)) and join(path, f).split('.')[1] in ext]

    return files[random.randint(0, len(files) - 1)]
