""" Opening and handling windows addon """
import os
from pywinauto import Application
from time import sleep
import ctypes
from ctypes import wintypes


def get_current_win_info():
    user32 = ctypes.windll.user32
    h_wnd = user32.GetForegroundWindow()
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(h_wnd, ctypes.byref(pid))
    return [h_wnd, pid.value]


def control_open_file(file):
    os.startfile(file)
    sleep(5)
    curr_wind_info = get_current_win_info()
    app = Application().connect(handle=curr_wind_info[0], process=curr_wind_info[1])
    music_app_window = app.window(found_index=0)
    if music_app_window:
        wrapper = music_app_window.top_level_parent()
        return wrapper
    else:
        return False


print(type(get_current_win_info))
print(isinstance(get_current_win_info, object))
print(os.environ)


#
# file_control = control_open_file(r"C:\Users\enman\Downloads\Django, Curso de Django para Principiantes.mp4")
# if file_control:
#     file_control.maximize()
#     sleep(1)
#     file_control.restore()
#     sleep(1)
#     file_control.minimize()
#     sleep(1)
#     file_control.restore()
#     sleep(1)
#     file_control.close()

path = r'C:\Users\enman\Music'


