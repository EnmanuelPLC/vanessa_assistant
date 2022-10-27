"""
Addon Engine logic
"""

import importlib
import os
import traceback
from termcolor import cprint

version = "1.0.0"
author = "EnmanuelPLC"


def import_addon(module_name):
    import sys
    importlib.import_module(module_name)
    if module_name in sys.modules:
        return sys.modules[module_name]
    return None


class AddonEngine:
    """
    Addons Engine
    """

    def __init__(self):
        self.addon_manifests = {}
        self.engine_version = version
        self.engine_author = author
        self.addon_engine_root_folder = os.path.dirname(__file__)
        self.addon_options_path = self.addon_engine_root_folder + "\\" + "options"
        self.addon_show_traceback_on_errors = False
        cprint(f"Addon Engine v{version} is Online!", "blue")

    # Initiating addon
    def init_addon(self, modname):
        try:
            addon = import_addon("addons." + modname)
        except Exception as err:
            self.print_error(f"Addon ERROR: {modname} error on load: {str(err)}")
            return False

        try:
            res = addon.start(self)
        except Exception as err:
            self.print_error(f"Addon ERROR: {modname} error on start: {str(err)}")
            return False

        return [modname, res]

    # Addons processing
    def addon_manifest(self, addon_name):
        """
        :param addon_name:
        :return:
        """
        if addon_name in self.addon_manifests:
            return self.addon_manifests[addon_name]
        return {}

    def addon_options(self, addon_name):
        """
        :param addon_name:
        :return:
        """
        manifest = self.addon_manifest(addon_name)
        if "options" in manifest:
            return manifest["options"]
        return None

    def print_error(self, err_txt, _err: Exception | None = None):
        """
        :param _err:
        :param err_txt:
        """
        self.print_red(err_txt)
        traceback.print_exc()

    @staticmethod
    def print_red(txt):
        """
        :param txt:
        """
        cprint(txt, "red")
