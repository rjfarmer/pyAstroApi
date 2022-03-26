# # SPDX-License-Identifier: BSD-3-Clause

import typing as t

import pyastroapi.articles as articles
import pyastroapi.api.token as token
import pyastroapi.api.libraries as lib
import pyastroapi.api.utils as utils


class libraries(object):
    """
    This is a collection of ADS libraries that supports iteration
    """

    def __init__(self):
        self._data = {}

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        return key in self._data

    def __iter__(self):
        yield from self._data

    def __dir__(self):
        return list(self.keys())

    def __getitem__(self, key):
        return self._data[key]

    def names(self):
        return list(self.keys())

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def new(self, name, description="", public=False, bibcodes=None):
        lib.new(token.get_token(), name, description, public, bibcodes)
        self.update()

    def pop(self, name):
        self.update()
        if name not in self._data.keys():
            raise KeyError("Library does not exit")

        lid = self._data[name].lid
        lib.delete(token.get_token(), lid)
        self.update()

    def update(self):
        all_libs = lib.list_all(token.get_token())

        self._data = {}

        for l in all_libs["libraries"]:
            self._data[l["name"]] = library(l["id"])


class library(object):
    """
    An instance of a single ADS library
    """

    def __init__(self, lid):
        self.lid = lid
        self._data = articles.journal()

    def update_all(self):
        bibcodes = list(lib.get(token.get_token(), self.lid))
        self._data = articles.journal(bibcodes=bibcodes)

    def update_iter(self):
        iter = lib.get(token.get_token(), self.lid)
        for bibcode in iter:
            self._data.add_bibcode(bibcode)

    def get(self, bibcode):
        return self._data[bibcode]

    def keys(self):
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
        yield from self._data

    def __hash__(self):
        return hash(self.lid)

    def __str__(self):
        return self._data["name"]

    def __eq__(self, value):
        if isinstance(value, library):
            if value.lid == self.lid:
                return True
        return False

    def add_bibcode(self, bibcodes):
        bibcodes = utils.ensure_list(bibcodes)
        lib.add(token.get_token(), self.lib, bibcodes)

        self._data.add_bibcode(bibcodes)

    def add_from_bibtex(self, bibtex):
        bibcodes = self._data.add_bibtex(bibtex)
        lib.add(token.get_token(), self.lib, bibcodes)

    def pop(self, bibcodes):
        bibcodes = utils.ensure_list(bibcodes)
        lib.remove(token.get_token(), self.lib, bibcodes)
        self._data.pop(bibcodes)

    def edit(self, name="", description="", public=False):
        raise NotImplementedError
