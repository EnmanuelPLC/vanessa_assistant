"""
Addon Engine logic
"""

import importlib
import json
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


def load_options(options_file=None, py_file=None, default_options=None):
    if options_file is None and py_file is None:
        raise Exception('ADE: Options or PY file is not defined, cant calc options filename')
    if default_options is None:
        default_options = {}
    options_file = py_file[:-3] + '.json'

    saved_options = {}
    try:
        with open(options_file, 'r', encoding="utf-8") as f:
            s = f.read()
        saved_options = json.loads(s)
    except Exception as err:
        print(err)
        pass

    final_options = {**default_options, **saved_options}

    import hashlib
    hash_w = hashlib.md5((json.dumps(default_options, sort_keys=True)).encode('utf-8')).hexdigest()

    if len(saved_options) == 0 or not ("hash" in saved_options.keys()) or saved_options["hash"] != hash_w:
        final_options["hash"] = hash_w
        str_options = json.dumps(final_options, sort_keys=True, indent=4, ensure_ascii=False)
        with open(options_file, 'w', encoding="utf-8") as f:
            f.write(str_options)
            f.close()

    return final_options


class AddonEngine:
    """
    Addons Engine
    """

    def __init__(self):
        self.addon_manifests = {}
        self.engine_version = version
        self.engine_author = author
        self.addons_prefix = "addon_"
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

        # if addon has an options
        if "default_options" in res:
            try:
                saved_options = {}
                try:
                    with open(self.addon_options_path + '/' + modname + '.json', 'r', encoding="utf-8") as f:
                        s = f.read()
                    saved_options = json.loads(s)
                except Exception as err:
                    print(err)

                res["default_options"]["v"] = res["version"]
                final_options = {**res["default_options"], **saved_options}

                if len(saved_options) == 0 or saved_options["v"] != res["version"]:
                    final_options["v"] = res["version"]
                    self.save_addon_options(modname, final_options)
                res["options"] = final_options

                try:
                    res2 = addon.start_with_options(self, res)
                    if res2 is not None:
                        res = res2
                except Exception as err:
                    self.print_error(f"Addon ERROR: {modname} error on start_with_options processing: {str(err)}")
                    return False

            except Exception as err:
                self.print_error(f"Addon ERROR: {modname} error on options processing: {str(err)}")
                return False

        return [modname, res]

    # Addons processing
    def save_addon_options(self, modname, options):
        """
        :param modname:
        :param options:
        """
        if not os.path.exists(self.addon_options_path):
            os.makedirs(self.addon_options_path)

        str_options = json.dumps(options, sort_keys=True, indent=4, ensure_ascii=False)
        with open(self.addon_options_path + '/' + modname + '.json', 'w', encoding="utf-8") as f:
            f.write(str_options)
            f.close()

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
