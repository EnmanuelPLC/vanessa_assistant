""" xds """
from pystray import Icon, Menu, MenuItem as Item
from PIL import Image, ImageDraw


def create_image():
    return Image.open('systray.ico')


try_icon = Icon('test', create_image(), menu=Menu(
    Item('Mostrar Vanessa', show),
    Item('Cerrar Vanessa', lambda Icon, item: 2)
))

try_icon.run_detached()
