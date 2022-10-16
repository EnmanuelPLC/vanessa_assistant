#!/usr/bin/env python
"""
# Module          : SysTrayIcon.py
# Synopsis        : Windows System tray icon.
# Programmer   : Simon Brunning - simon@brunningonline.net
# Date               : 11 April 2005
# Notes            : Based on (i.e. ripped off from) Mark Hammond's win32gui_taskbar.py and win32gui_menu.py demos from PyWin32

For now, the demo at the bottom shows how to use it..."""

import os
import sys

import win32api
import win32con
import win32gui_struct

try:
    import winxpgui as win32gui
except ImportError:
    import win32gui


class SysTrayIcon(object):
    QUIT = 'QUIT'
    SPECIAL_ACTIONS = [QUIT, 'Show']

    FIRST_ID = 1023

    def __init__(self, icon, wind, hover_text, menu_options, on_quit=None, default_menu_index=None, window_class_name=None):
        self.wind = wind
        self.icon = icon
        self.hover_text = hover_text
        self.on_quit = on_quit
        menu_options += ('Quit', None, self.QUIT),
        self._next_action_id = self.FIRST_ID
        self.menu_actions_by_id = set()
        self.menu_options = self._add_ids_to_menu_options(list(menu_options))
        self.menu_actions_by_id = dict(self.menu_actions_by_id)
        del self._next_action_id
        self.default_menu_index = (default_menu_index or 0)
        self.window_class_name = window_class_name or "VanessaAssistant"

        message_map = {win32gui.RegisterWindowMessage("TaskbarCreated"): self.restart,
                       win32con.WM_DESTROY: self.destroy,
                       win32con.WM_COMMAND: self.command,
                       win32con.WM_USER + 20: self.notify, }
        # Register the Window class.
        window_class = win32gui.WNDCLASS()
        hinst = window_class.hInstance = win32gui.GetModuleHandle(None)
        window_class.lpszClassName = self.window_class_name
        window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        window_class.hbrBackground = win32con.COLOR_WINDOW
        window_class.lpfnWndProc = message_map  # could also specify a wndproc.
        class_atom = win32gui.RegisterClass(window_class)
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(
            class_atom, self.window_class_name, style, 0, 0, win32con.CW_USEDEFAULT,
            win32con.CW_USEDEFAULT, 0, 0, hinst, None)
        win32gui.UpdateWindow(self.hwnd)
        self.notify_id = None
        self.refresh_icon()
        win32gui.PumpMessages()

    def _add_ids_to_menu_options(self, menu_options):
        result = []
        for menu_option in menu_options:
            option_text, option_icon, option_action = menu_option
            if callable(option_action) or option_action in self.SPECIAL_ACTIONS:
                self.menu_actions_by_id.add((self._next_action_id, option_action))
                result.append(menu_option + (self._next_action_id,))
            elif non_string_iterable(option_action):
                result.append((option_text,
                               option_icon,
                               self._add_ids_to_menu_options(option_action),
                               self._next_action_id))
            else:
                print('Unknown item', option_text, option_icon, option_action)
            self._next_action_id += 1
        return result

    def refresh_icon(self):
        """ Refresh icons """
        hinst = win32gui.GetModuleHandle(None)
        if os.path.isfile(self.icon):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(hinst, self.icon,
                                       win32con.IMAGE_ICON,
                                       0, 0, icon_flags)
        else:
            print("Can't find icon file - using default.")
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        if self.notify_id:
            message = win32gui.NIM_MODIFY
        else:
            message = win32gui.NIM_ADD
        self.notify_id = (self.hwnd,
                          0, win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP,
                          win32con.WM_USER + 20, hicon, self.hover_text)
        win32gui.Shell_NotifyIcon(message, self.notify_id)

    def restart(self, _hwnd, _msg, _wparam, _lparam):
        """
        :param _hwnd:
        :param _msg:
        :param _wparam:
        :param _lparam:
        """
        self.refresh_icon()

    def destroy(self, _hwnd, _msg, _wparam, _lparam):
        """
        :param _hwnd:
        :param _msg:
        :param _wparam:
        :param _lparam:
        """
        if self.on_quit:
            self.on_quit(self)
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)

    def notify(self, _hwnd, _msg, _wparam, lparam):
        """
        :param _hwnd:
        :param _msg:
        :param _wparam:
        :param lparam:
        :return:
        """
        if lparam == win32con.WM_LBUTTONDBLCLK:
            self.execute_menu_option(self.default_menu_index + self.FIRST_ID)
        elif lparam == win32con.WM_RBUTTONUP:
            self.show_menu()
        elif lparam == win32con.WM_LBUTTONUP:
            pass
        return True

    def show_menu(self):
        """ Display menu """
        menu = win32gui.CreatePopupMenu()
        self.create_menu(menu, self.menu_options)

        pos = win32gui.GetCursorPos()

        win32gui.SetForegroundWindow(self.hwnd)
        win32gui.TrackPopupMenu(menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, self.hwnd, None)
        win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)

    def create_menu(self, menu, menu_options):
        """
        :param menu:
        :param menu_options:
        """
        for option_text, option_icon, option_action, option_id in menu_options[::-1]:
            if option_icon:
                option_icon = self.prep_menu_icon(option_icon)

            if option_id in self.menu_actions_by_id:
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                wID=option_id)
                win32gui.InsertMenuItem(menu, 0, 1, item)
            else:
                submenu = win32gui.CreatePopupMenu()
                self.create_menu(submenu, option_action)
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                hSubMenu=submenu)
                win32gui.InsertMenuItem(menu, 0, 1, item)

    @staticmethod
    def prep_menu_icon(icon):
        """
        :param icon:
        :return:
        """
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        hicon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON, ico_x, ico_y, win32con.LR_LOADFROMFILE)

        hdc_bitmap = win32gui.CreateCompatibleDC(0)
        hdc_screen = win32gui.GetDC(0)
        hbm = win32gui.CreateCompatibleBitmap(hdc_screen, ico_x, ico_y)
        hbm_old = win32gui.SelectObject(hdc_bitmap, hbm)
        # Fill the background.
        brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)
        win32gui.FillRect(hdc_bitmap, (0, 0, 16, 16), brush)
        # unclear if brush needs to be feed.  Best clue I can find is:
        # "GetSysColorBrush returns a cached brush instead of allocating a new
        # one." - implies no DeleteObject
        # draw the icon
        win32gui.DrawIconEx(hdc_bitmap, 0, 0, hicon, ico_x, ico_y, 0, 0, win32con.DI_NORMAL)
        win32gui.SelectObject(hdc_bitmap, hbm_old)
        win32gui.DeleteDC(hdc_bitmap)

        return hbm

    def command(self, _hwnd, _msg, wparam, _lparam):
        """
        :param _hwnd:
        :param _msg:
        :param wparam:
        :param _lparam:
        """
        _id = win32gui.LOWORD(wparam)
        self.execute_menu_option(_id)

    def execute_menu_option(self, _id):
        """
        :param _id:
        """
        menu_action = self.menu_actions_by_id[_id]
        if menu_action == self.QUIT:
            win32gui.DestroyWindow(self.hwnd)
        elif menu_action == 'Show':
            self.wind.restore()
            self.wind.show()
        else:
            menu_action(self)


def non_string_iterable(obj):
    """
    :param obj:
    :return:
    """
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return not isinstance(obj, str)


# Minimal self test. You'll need a bunch of ICO files in the current working
# directory in order for this to work...
if __name__ == '__main__':
    import itertools
    import glob

    icons = itertools.cycle(glob.glob('*.ico'))
    hover_txt = "VanessaAssistant"


    def hello(_sys_tray_icon):
        """
        :param _sys_tray_icon:
        """
        print("Hello World.")


    def simon(_sys_tray_icon):
        """
        :param _sys_tray_icon:
        """
        print("Hello Simon.")


    def bye(_sys_tray_icon):
        """
        :param _sys_tray_icon:
        """
        print('Bye, then.')


    def switch_icon(sys_tray_icon):
        """
        :param sys_tray_icon:
        """
        sys_tray_icon.icon = next(icons)
        sys_tray_icon.refresh_icon()


    menu_opt = (
        ('Say Hello', next(icons), hello),
        ('Switch Icon', None, switch_icon),
        ('A sub-menu', next(icons),
         (('Say Hello to Simon', next(icons), simon),
          ('Switch Icon', next(icons), switch_icon))
         ))

    SysTrayIcon(next(icons), hover_txt, menu_opt, on_quit=bye, default_menu_index=1)
