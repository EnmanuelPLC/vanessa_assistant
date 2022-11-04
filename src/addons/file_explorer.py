""" File explorer addon """
import os
from assistant import AssistantCore
import subprocess
import locale

global doc_folder, down_folder, images_folder, music_folder, video_folder, movies_folder, series_folder

en_folder = ['Documents', 'Downloads', 'Images', 'Music', 'Videos', 'Movies', 'Series']
es_folder = ['Documentos', 'Descargas', 'Imágenes', 'Música', 'Videos', 'Películas', 'Series']


def init_file_explorer():
    global doc_folder, down_folder, images_folder, music_folder, video_folder, movies_folder, series_folder
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
    movies_folder = user_dir + user_lang_folder[5]
    series_folder = user_dir + user_lang_folder[6]

    if not os.path.isdir(doc_folder):
        os.mkdir(doc_folder)
    if not os.path.isdir(down_folder):
        os.mkdir(down_folder)
    if not os.path.isdir(images_folder):
        os.mkdir(images_folder)
    if not os.path.isdir(music_folder):
        os.mkdir(music_folder)
    if not os.path.isdir(video_folder):
        os.mkdir(video_folder)
    if not os.path.isdir(movies_folder):
        os.mkdir(movies_folder)
    if not os.path.isdir(series_folder):
        os.mkdir(series_folder)


def start(core: AssistantCore):
    manifest = {
        "name": "Explorador de archivos",
        "version": "1.0",
        "require_online": False,

        "commands": {
            "los archivos|las carpetas": open_file_explorer,
            "abre documentos|mis documentos|abre los documentos": open_doc_folder,
            "abre descargas|mis descargas|abre las descargas": open_down_folder,
            "abre imágenes|mis imágenes|abre las imágenes|abre las fotos|mis fotos": open_images_folder,
            "abre música|mi música|abre la música": open_music_folder,
            "abre videos|mis videos|abre los videos": open_video_folder,
            "quiero ver peliculas|quiero ver películas|mis peliculas|mis películas|abre las peliculas|abre las películas": open_movies_folder,
            "quiero ver series|mis series|abre las series": open_video_folder,
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


def open_movies_folder(core: AssistantCore, phrase: str):
    subprocess.Popen(f'explorer.exe {movies_folder}')
    core.say('Abriendo tu carpeta de películas')
    core.context_set(play_random_video)


def open_series_folder(core: AssistantCore, phrase: str):
    subprocess.Popen(f'explorer.exe {series_folder}')
    core.say('Abriendo tu carpeta de series')
    core.context_set(play_random_video)


def play_random_music(core: AssistantCore, phrase: str):
    if phrase.find('si') >= 0 or phrase.find('ok') >= 0 or phrase.find('está bien') >= 0 or phrase.find('afirmativo') >= 0:
        core.say('Seleccionando una canción al azar')
        music = get_random_file(music_folder, 'music')
        os.startfile(music_folder + f'\\{music}')
        core.context_clear()
    elif phrase.find('no') >= 0 or phrase.find('ne') >= 0 or phrase.find('negativo') >= 0:
        core.say('Esta bien, cualquier cosa, aquí estoy a su disposición')
        core.context_clear()
    else:
        core.say('Responde si, o no;')
        core.context_set(play_random_music)


def play_random_video(core: AssistantCore, phrase: str):
    if phrase.find('si') >= 0 or phrase.find('ok') >= 0 or phrase.find('está bien') >= 0 or phrase.find('afirmativo') >= 0:
        core.say('Seleccionando un video al azar')
        video = get_random_file(video_folder, 'video')
        os.startfile(video_folder + f'\\{video}')
        core.context_clear()
    elif phrase.find('no') >= 0 or phrase.find('ne') >= 0 or phrase.find('negativo') >= 0:
        core.say('Esta bien, cualquier cosa, aquí estoy a su disposición')
        core.context_clear()
    else:
        core.say('Responde, si, o no')
        core.context_set(play_random_video)


def get_random_file(path, typ=None):
    from os import listdir
    from os.path import join, isfile
    import random

    if typ == 'video':
        ext = ['m4v', 'mp4', 'mkv', 'mpg', 'mpeg', 'avi', '3gp']
    else:
        ext = ['mp3', 'm4r', 'm4a', 'wav', 'ogg']
    files = [f for f in listdir(path) if isfile(join(path, f)) and join(path, f).split('.')[1] in ext]

    return files[random.randint(0, len(files) - 1)]
