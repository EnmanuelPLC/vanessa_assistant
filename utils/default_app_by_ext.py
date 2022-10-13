from winreg import HKEY_LOCAL_MACHINE, HKEY_CURRENT_USER, OpenKey, QueryValueEx, ConnectRegistry


video_ext = ['m4v', 'mp4', 'mkv', 'mpg', 'mpeg', 'avi', '3gp']
music_ext = ['mp3', 'm4r', 'm4a', 'wav', 'ogg']
browser_ext = ['url', 'http', 'https']


def get_default_app_path(ext):
    launch_path = ""
    if ext in video_ext:
        key = HKEY_CURRENT_USER
        registry_default_path = r'Software\Classes\.'+ext
        value = None
    elif ext in music_ext:
        key = HKEY_LOCAL_MACHINE
        registry_default_path = r'Software\Classes\.'+ext
        value = None
    elif ext in browser_ext:
        key = HKEY_CURRENT_USER
        registry_default_path = r'Software\Microsoft\Windows\Shell\Associations\UrlAssociations\https\UserChoice'
        value = 'ProgId'
    else:
        return Exception("Extension de archivo no soportada")

    with OpenKey(key, registry_default_path) as key:
        app_n, _ = QueryValueEx(key, value)

    if len(app_n) > 0:
        with OpenKey(ConnectRegistry(None, HKEY_LOCAL_MACHINE), r"SOFTWARE\Classes\{}\shell\open\command".format(app_n)) as key:
            launch_path, _ = QueryValueEx(key, "")

    return launch_path.split('"', -1)[1]
