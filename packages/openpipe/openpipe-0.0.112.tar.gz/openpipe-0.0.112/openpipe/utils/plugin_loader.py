"""
This module provides the plugin_load function which performs the following:
    - map action names to python module files
    - import the plugin
    - create an instance of the Plugin class
    - validate the Plugin's config schema
    - validate that the user provided config meets the config schema requirements
"""
from sys import stderr, exit
from importlib import import_module
from traceback import format_exc
from .plugin_config_schema import validate_config_schema
from .plugin_config import validate_provided_config


def plugin_load(action_name, action_config, action_label):
    plugin_path = "openpipe plugins "
    plugin_path += action_name
    plugin_path = plugin_path.replace(" ", ".")

    try:
        module = import_module(plugin_path)
    except ModuleNotFoundError:
        print(format_exc(), file=stderr)
        print("Required for action:", plugin_path, file=stderr)
        exit(1)
    except ImportError as error:
        print("Error loading module", plugin_path, file=stderr)
        print(format_exc(), error, file=stderr)
        print("Required for action:", action_label, file=stderr)
        exit(2)
    if not hasattr(module, "Plugin"):
        print("Module {} does not provide a Plugin class!".format(module), file=stderr)
        print("Required for action:", action_label, file=stderr)
        exit(2)
    plugin_class = module.Plugin
    validate_config_schema(plugin_class, action_label)
    action_config = validate_provided_config(plugin_class, action_label, action_config)
    instance = module.Plugin(action_config)
    instance.plugin_label = action_label
    instance.plugin_filename = plugin_path
    return instance
