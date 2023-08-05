import os
import configparser
from . import paths as path_helpers


def _parse_config(path):
    """
    Helper method to parse a configuration from a file path.

    :param path {str}: The path to the configuration file
    :return {config.configparser.ConfigParser|NoneType}:
        Returns None if the file cannot be found or if there is an error
        in parsing the configuration file. Otherwise the full configuration
        object is return after performing a `read` on the file.
    """
    try:
        if not os.path.isfile(path):
            return None

        configuration = configparser.ConfigParser(allow_no_value=True)
        configuration.read(path)

        return configuration
    except Exception as e:
        print(str(e))
        return None


def init():
    global setup_calls
    global pipe_dev_null
    global paths
    global standard_env_path
    global odoo_env_path
    global config
    global odoo_env_config

    setup_calls = {}
    pipe_dev_null = path_helpers.pipe_dev_null
    paths = path_helpers.Paths()
    standard_env_path = paths.base('.env')
    odoo_env_path = paths.base('.container/env/odoo/odoo.env')
    config = load_standard_config(standard_env_path)
    odoo_env_config = load_odoo_env_config(odoo_env_path)


def setup_called():
    global setup_calls
    pid = os.getpid()
    ppid = os.getppid()

    setup_calls[ppid] = setup_calls[ppid] + 1 if ppid in setup_calls else 1
    setup_calls[pid] = setup_calls[pid] + 1 if pid in setup_calls else 1


def can_setup():
    global setup_calls
    pid = os.getpid()
    ppid = os.getppid()

    return ppid not in setup_calls and pid not in setup_calls


def load_standard_config(env_path):
    """
    Used to load a standard configuration.

    :param env_path {str}: Path to the configuration file
    :return {config.configparser.ConfigParser|NoneType}:
        Returns None if the file cannot be found or if there is an error
        in parsing the configuration file. Otherwise the full configuration
        object is return after performing a `read` on the file.
    """
    return _parse_config(env_path)


def load_odoo_env_config(env_path):
    """
    Used to load an odoo specific configuration.

    :param env_path {str}: Path to the configuration file
    :return {config.configparser.ConfigParser|NoneType}:
        Returns None if the file cannot be found or if there is an error
        in parsing the configuration file. Otherwise the full configuration
        object is return after performing a `read` on the file.
    """
    return _parse_config(env_path)
