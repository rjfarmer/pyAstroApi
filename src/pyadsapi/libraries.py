# SPDX-License-Identifier: BSD-3-Clause

from . import articles

from .api import libraries as lib


class libraries(object):
    """
    This is a collection of ADS libraries that supports iteration
    """

    def __init__(self, token):
        self.token = token
        self._data = None

    def __len__(self):
        if self._data is not None:
            return len(self._data)
        else:
            return 0

    def __contains__(self, key):
        if self._data is not None:
            return key in self._data
        else:
            return False

    def __iter__(self):
        for i in self._data:
            yield self.get(i)

    def __dir__(self):
        return self.__dict__.keys() + list(self.keys())

    def __getitem__(self, key):
        if self._data is None:
            self.update()
        if key in self._data.keys():
            return library(self.token, self._data[key]["id"])

    def __getattr__(self, key):
        if self._data is None:
            self.update()
        if key in self._data.keys():
            return library(self.token, self._data[key]["id"])

    def keys(self):
        if self._data is None:
            self.update()
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def get(self, name):
        return library(self.token, self._data[name]["id"])

    def update(self):
        data = lib.list_all(self.token)
        self._data = {}
        for value in data:
            self._data[value["name"]] = value

    def add(self, name, description="", public=False, bibcodes=None):
        lib.new(name, description, public, bibcodes)

    def remove(self, name):
        if name not in self._data.keys():
            raise KeyError("Library does not exit")

        lid = self._data[name]["id"]
        lib.delete(lid, self.token)
        self._data.pop(name, None)


class library(object):
    """
    An instance of a single ADS library
    """

    def __init__(self, token, lid):
        self.token = token
        self.lid = lid
        self._data = {}

    def keys(self):
        if self._data is None:
            self.update()
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        return key in self._data

    def __iter__(self):
        for i in self._data:
            yield self.get(i)

    def __hash__(self):
        return hash(self.lid)

    def __eq__(self, value):
        if isinstance(value, library):
            if value.lid == self.lid:
                return True
        return False
