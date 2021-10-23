# SPDX-License-Identifier: BSD-3-Clause

import typing as t

from . import articles
from .api import libraries as lib


class libraries(object):
    """
    This is a collection of ADS libraries that supports iteration
    """

    def __init__(self, token):
        self.token = token
        self._data = None

    @property
    def data(self):
        if self._data is None:
            data = lib.list_all(self.token)
            self._data = {}
            for value in data:
                self._data[value["name"]] = value
        return self._data

    def __len__(self):
        return len(self.data)

    def __contains__(self, key):
        return key in self.data

    def __iter__(self):
        for i in self.data:
            yield self.get(i)

    def __dir__(self):
        return list(self.__dict__.keys()) + list(self.keys())

    def __getitem__(self, key):
        if key in self.data.keys():
            return library(self.token, self.data[key]["id"])

    def __getattr__(self, key):
        if key in self.data.keys():
            return library(self.token, self.data[key]["id"])

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

    def items(self):
        return self.data.items()

    def get(self, name):
        return library(self.token, self.data[name]["id"])

    def add(self, name, description="", public=False, bibcodes=None):
        lib.new(name, description, public, bibcodes)

    def remove(self, name):
        if name not in self.data.keys():
            raise KeyError("Library does not exit")

        lid = self.data[name]["id"]
        lib.delete(lid, self.token)
        self.data.pop(name, None)


class library(object):
    """
    An instance of a single ADS library
    """

    def __init__(self, token, lid):
        self.token = token
        self.lid = lid
        self._data = None

    @property
    def data(self):
        if self._data is None:
            self.update()
        return self._data

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

    def items(self):
        return self.data.items()

    def __len__(self):
        return len(self.data)

    def __contains__(self, key):
        return key in self.data

    def __iter__(self):
        for i in self.data:
            yield self.get(i)

    def __hash__(self):
        return hash(self.lid)

    def __eq__(self, value):
        if isinstance(value, library):
            if value.lid == self.lid:
                return True
        return False
