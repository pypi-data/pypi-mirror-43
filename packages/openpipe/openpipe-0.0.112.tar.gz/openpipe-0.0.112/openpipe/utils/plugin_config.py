from openpipe.utils.yaml import load_yaml
from sys import stderr, exit
from pprint import pformat
from enum import Enum, unique


@unique
class Errors(Enum):
    CONFIG_MUST_BE_DICT = 20
    CONFIG_MISSING_KEY = 21
    CONFIG_UNSUPPORTED_KEY = 22


def validate_required_config(module_plugin, plugin_label, provided_config):
    """ """
    resulting_config = {}
    try:
        required_config_str = getattr(module_plugin, "required_config")
    except AttributeError:
        return resulting_config

    required_config = load_yaml(required_config_str, False)

    # if a non dict config is provided, and a single item is required
    # assume it as the only required item
    if not isinstance(provided_config, dict):
        if len(required_config) == 1:
            required_config_key = next(iter(required_config.keys()))
            return {required_config_key: provided_config}
        else:
            print("Invalid config for", plugin_label, file=stderr)
            print("Got", type(provided_config), pformat(provided_config), file=stderr)
            print("Expected dictionary with fields", required_config_str, file=stderr)
            exit(Errors.CONFIG_MUST_BE_DICT)

    for key in required_config:
        try:
            resulting_config[key] = provided_config[key]
        except KeyError:
            print("Invalid config for", plugin_label, file=stderr)
            print("The required field '%s' is missing" % key, plugin_label, file=stderr)
            print(
                "The following config are required:", required_config_str, file=stderr
            )
            exit(Errors.CONFIG_MISSING_KEY)

    return resulting_config


def validate_optional_config(
    required_config, module_plugin, plugin_label, provided_config
):
    """ validate optional config and return the complete config """

    optional_config_str = getattr(module_plugin, "optional_config", "{}")
    optional_config = load_yaml(optional_config_str, False)

    # config schema accepts a single optional non dict item
    if not isinstance(optional_config, dict):
        if provided_config:
            return provided_config
        else:
            return optional_config
    merged_config = {**required_config, **optional_config}

    # a single input item was provided and required_config is only one
    if not isinstance(provided_config, dict) and len(required_config) == 1:
        return merged_config

    if provided_config:
        for key in provided_config:
            if key not in merged_config:
                print(
                    "The provide field '%s' is not supported" % key,
                    plugin_label,
                    file=stderr,
                )
                print(
                    "Expected dictionary with fields", optional_config_str, file=stderr
                )
                exit(Errors.CONFIG_UNSUPPORTED_KEY)

    final_config = (
        {**merged_config, **provided_config} if provided_config else merged_config
    )
    if len(final_config) == 0 and provided_config is not None:
        print("Unexpected config for", plugin_label, file=stderr)
        print("Got", type(provided_config), pformat(provided_config), file=stderr)
        print("The plugin does not support any kind of configuration", file=stderr)
        exit(20)

    return final_config


def validate_provided_config(module_plugin, plugin_label, provided_config):
    """ Validate that the provided_config is valid per the plugin config schema """

    if hasattr(module_plugin, "required_some_config"):
        if provided_config is None:
            print("Missing config for", plugin_label, file=stderr)
            print("The plugin requires config", file=stderr)
            exit(25)
        else:
            return provided_config

    required_config = validate_required_config(
        module_plugin, plugin_label, provided_config
    )

    if (
        len(required_config) == 1
        and not isinstance(provided_config, dict)
        and not hasattr(module_plugin, "optional_config")
    ):
        return required_config
    config = validate_optional_config(
        required_config, module_plugin, plugin_label, provided_config
    )
    return config
