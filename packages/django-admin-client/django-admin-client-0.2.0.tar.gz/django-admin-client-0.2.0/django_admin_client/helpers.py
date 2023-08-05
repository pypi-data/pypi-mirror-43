import os
import sys

from unittest.mock import sentinel

from dotenv import load_dotenv

NotSet = sentinel.NotSet


# https://stackoverflow.com/q/6760685/4911986
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SettingsFunctionality(metaclass=Singleton):
    def __init__(self, exit_if_unset=False):
        load_dotenv()
        self._init_from_env_variables()
        if exit_if_unset:
            self._exit_if_unset_variables()

    def _keys(self):
        for key in dir(self.__class__):
            if key == key.upper():
                yield key

    def _init_from_env_variables(self):
        for key in self._keys():

            value = os.environ.get(key, NotSet)
            if value is NotSet:
                continue

            setattr(self, key, value)

    def _exit_if_unset_variables(self):
        unset_keys = []
        for key in self._keys():
            if getattr(self, key) == NotSet:
                unset_keys.append(key)

        if unset_keys:
            print("Unset settings keys: {}".format(", ".join(unset_keys)), file=sys.stderr)
            sys.exit(1)
