import subprocess
from assistant import AssistantCore

multPath = ""
serialPath = ""


def start(core: AssistantCore):
    """

    :param core:
    :return:
    """
    manifest = {
        "name": "Reproductor de videos",
        "version": "2.0",
        "require_online": False,

        "default_options": {
            "multPath": '',
            "serialPath": '',
        },

        "commands": {
            "reproductor de video": run_player,
            "pelicula|película": play_mult,
            "serie": play_serial,
        }
    }
    return manifest


def start_with_options(core: AssistantCore, manifest: dict):
    """

    :param core:
    :param manifest:
    :return:
    """
    global multPath, serialPath

    options = manifest["options"]
    multPath = options["multPath"]
    serialPath = options["serialPath"]
    return manifest


def run_player(core: AssistantCore, phrase: str):
    """

    :param core:
    :param phrase:
    """
    subprocess.Popen([core.mpcHcPath])


def play_mult(core: AssistantCore, phrase: str):
    """

    :param core:
    :param phrase:
    :return:
    """
    if multPath == "":
        core.say("Carpeta de películas no configurada")
        return
    else:
        if phrase == "":
            core.say("Deseas buscarla, o ver una de las tuyas?")

    if phrase.find("buscar") >= 0 or phrase.find("buscarla") >= 0:
        core.say("Dime el nombre de la película")
        core.context_set(search_movie)
    elif phrase.find("localmente") >= 0 or phrase.find("local") >= 0 or phrase.find("pc") >= 0 or phrase.find("archivos") >= 0:
        core.say("Abriendo tu carpeta de películas")
        subprocess.Popen(['explorer.exe', multPath])
        core.context_set(play_local_movie)
    elif phrase.find("no") >= 0 or phrase.find("ninguna") >= 0 or phrase.find("nada") >= 0 or phrase.find("cancelar") >= 0:
        core.say("Bien, que deseas hacer ahora?")
        core.context_set(core.commands_ctx)
    else:
        core.say("Debes elegir entre buscar una internet, reproducir una local o cancelar este comando")
        core.context_set(play_mult)


def search_movie(core: AssistantCore, phrase: str):
    """

    :param core:
    :param phrase:
    """
    if len(phrase) > 0:
        core.say("Buscando la película, " + phrase + ", en internet")
        import webbrowser
        url = "https://www.google.com/search?q=película " + phrase
        webbrowser.get().open(url)


def play_local_movie(core: AssistantCore, phrase: str):
    """

    :param core:
    :param phrase:
    """
    mult_files = mult_list()
    for f in mult_files:
        name = str(f)[:-4].lower().replace(".", "").replace(",", "")
        if name == phrase:
            print("Pelicula ", f)
            subprocess.Popen([core.mpcHcPath, multPath + "\\" + f])


def play_serial(core: AssistantCore, phrase: str):
    """

    :param core:
    :param phrase:
    :return:
    """
    if serialPath == "":
        core.say("Carpeta de series no configurada")
        return

    if phrase == "":
        core.say("Cuál serie deseas ver?")
        core.context_set(play_serial)
        return

    serials = serial_list()
    for serial_name in serials.keys():
        if phrase.startswith(serial_name):
            rest_phrase = phrase[(len(serial_name) + 1):]
            serial_dir = serials[serial_name]

            play_serial_number(core, rest_phrase, serial_dir)
            return

    core.say("No encontré la serie. Repita el título.")
    core.context_set(play_serial)


def play_serial_number(core: AssistantCore, phrase: str, serial_dir: str):
    """

    :param core:
    :param phrase:
    :param serial_dir:
    :return:
    """
    from os import listdir
    from os.path import isfile, join
    serial_path = join(serialPath, serial_dir)
    series = [f for f in listdir(serial_path) if
              (isfile(join(serial_path, f)) and (str(f)[-3:].lower() in ["mkv", "avi", "mp4", "mpg"]))]

    if len(series) == 0:
        core.say("Error: no se encontraron episodios en esta serie")
        return

    print("Serie:", series)

    if phrase == "":
        core.say("cuál capítulo deseas ver?")
        core.context_set((play_serial_number, serial_dir))
        return

    sum = None
    import utils.num_to_text_ru as num_to_text

    if sum is None:
        if phrase == "primero":
            sum = 1
        if phrase == "último":
            sum = len(series)

    if sum is None:
        for i in range(100000, 0, -1):
            str_try = num_to_text.num2text(i)
            if phrase == str_try:
                sum = i
                break

    if sum is None:
        core.say("cuál capítulo deseas ver?")
        core.context_set((play_serial_number, serial_dir))
        return

    if sum > len(series):
        core.say("Este capítulo no existe en la serie. Di otro número")
        core.context_set((play_serial_number, serial_dir))
        return

    core.say("Abriendo")
    print("Serie ", serial_dir, "serie", series[sum - 1])
    subprocess.Popen([core.mpcHcPath, serial_path + "\\" + series[sum - 1]])
    return


def mult_list():
    """

    :return:
    """
    from os import listdir
    from os.path import isfile, join
    files = [f for f in listdir(multPath) if isfile(join(multPath, f))]
    return files


def serial_list():
    """

    :return:
    """
    from os import listdir
    from os.path import isdir, join
    import os

    dirs = [f for f in listdir(serialPath) if isdir(join(serialPath, f))]
    res = {}
    for dir in dirs:
        k1 = str(dir).lower().replace(".", "").replace(",", "")
        res[k1] = dir

        file_irene = join(serialPath, dir, "_irenename.txt")
        if os.path.exists(file_irene):
            with open(file_irene, encoding="utf-8") as file:
                lines = file.readlines()
                lines = [line.rstrip() for line in lines]

            for line in lines:
                res[line] = dir
    return res


if __name__ == "__main__":
    print(serial_list())
