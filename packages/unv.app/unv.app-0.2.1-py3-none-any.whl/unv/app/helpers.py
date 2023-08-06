import importlib
import pathlib

from .settings import SETTINGS


def get_app_components():
    for component in SETTINGS['components']:
        component = '{}.app'.format(component)
        try:
            yield importlib.import_module(component)
        except ModuleNotFoundError:
            continue


def project_path(*parts):
    return str(pathlib.Path(SETTINGS['root'], *parts))
