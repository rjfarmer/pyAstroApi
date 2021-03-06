# # SPDX-License-Identifier: BSD-3-Clause

import pyastroapi.api.token as token
import pyastroapi.api.utils as utils
import pyastroapi.api.search as _search
import pyastroapi.api.export as _export
import pyastroapi.api.metrics as _metrics
import pyastroapi.api.visualization as _visualization
import pyastroapi.api.resolver as _resolve
import pyastroapi.api.http as _http
import pyastroapi.api.exceptions as _e

import typing as t

import pyastroapi
import pyastroapi.bibtex as bib

__all__ = ["article", "journal"]


class Export:
    def __init__(self, bibcodes):
        self.bibcodes = utils.ensure_list(bibcodes)

    def __getattr__(self, attr):
        return getattr(_export, attr)(token.get_token(), self.bibcodes)

    def __dir__(self):
        return dir(_export)


class Metrics:
    def __init__(self, bibcodes):
        self.bibcodes = utils.ensure_list(bibcodes)

    def __getattr__(self, attr):
        return getattr(_metrics, attr)(token.get_token(), self.bibcodes)

    def __dir__(self):
        return dir(_metrics)


class Visualization:
    def __init__(self, bibcodes):
        self.bibcodes = utils.ensure_list(bibcodes)

    def __getattr__(self, attr):
        return getattr(_visualization, attr)(token.get_token(), self.bibcodes)

    def __dir__(self):
        return dir(_visualization)


class PDF:
    def __init__(self, bibcode):
        if isinstance(bibcode, list):
            raise TypeError("Can only handle one pdf at a time")

        self.links = None

        self.bibcode = bibcode

    def _get(self):
        try:
            links = _resolve.esource(token.get_token(), self.bibcode)
        except _e.NoRecordsFound:
            raise ValueError("No pdf links available")

        if "links" not in links:
            raise ValueError("No pdf links available")

        for i in links["links"]["records"]:
            self.links[i["link_type"]] = i["url"]

    def filename(self):
        return f"{self.bibcode}.pdf"

    def _download(self, source, name, filename=None):
        if self.links is None:
            self._get()

        if source not in self.links:
            raise ValueError(f"No {name} pdf available for {self.bibcode}")

        if filename is None:
            filename = self.filename()

        print(self.links[source], filename)
        _http.download_file(self.links[source], filename)

    def arxiv(self, filename=None):
        self._download("ESOURCE|EPRINT_PDF", "Arxiv", filename)
        return filename

    def publisher(self, filename=None):
        self._download("ESOURCE|PUB_PDF", "Publisher", filename)
        return filename

    def ads(self, filename=None):
        self._download("ESOURCE|ADS_PDF", "ADSABS", filename)
        return filename


class Urls:
    def __init__(self, bibcode):
        if isinstance(bibcode, list):
            raise TypeError("Can only handle one pdf at a time")

        self.bibcode = bibcode
        links = _resolve.esource(token.get_token(), bibcode)
        self.links = {}
        if "links" not in links:
            raise ValueError("No pdf links available")

        for i in links["links"]["records"]:
            self.links[i["link_type"]] = i["url"]

    def _get(self, source, name):
        if source not in self.links:
            raise ValueError(f"No {name} html available for {self.bibcode}")

        if filename is None:
            filename = self.filename()

    @property
    def ads(self):
        return f"https://ui.adsabs.harvard.edu/abs/{self.bibcode}"

    @property
    def arixv(self):
        return self._get("ESOURCE|EPRINT_HTML", "Arxiv")

    @property
    def journal(self):
        tries = ["ESOURCE", "ESOURCE|HTML", "PUB_HTML", "AUTHOR_HTML"]

        for link in tries:
            if link in self.links:
                return self._get(link, "Journal")


class article:
    def __init__(
        self,
        bibcode: str = None,
        data: t.Dict = None,
        bibtex: str = None,
        search: str = None,
    ):
        self.bibcode = None
        self._data = {}
        self._query = None
        self._refs = None
        self._cites = None

        if bibcode is not None:
            self.from_bibcode(bibcode)
        elif data is not None:
            self.from_data(data)
        elif bibtex is not None:
            self.from_bibtex(bibtex)
        elif search is not None:
            self.from_search(search)

    def from_bibcode(self, bibcode: str):
        self.bibcode = bibcode
        self._data["bibcode"] = self.bibcode

    def from_data(self, data: t.Dict):
        self._data = data
        if "bibcode" in self._data.keys():
            self.bibcode = self._data["bibcode"]

    def from_bibtex(self, bibtex: str):
        bd = bib.parse_bibtex(bibtex)
        self.from_data(list(pyastroapi.search(bd[0], limit=1))[0])

    def from_search(self, search: str):
        self._query = search
        self.from_data(list(pyastroapi.search(search, limit=1))[0])

    def add_to_lib(self, libaray: str):
        raise NotImplementedError

    def __getattr__(self, attr: str):
        if attr not in self._data:
            if "bibcode" not in self._data:
                raise ValueError("Bibcode must be set first")

            else:
                fields = ""
                if len(self._data) == 1:  # Load basic data
                    fields = _search._short_fl

                if (
                    attr not in self._data and attr not in fields
                ):  # Add field if we dont have it allready
                    fields = f"{attr}," + fields

                x = list(
                    pyastroapi.search(
                        query=f"bibcode:{self.bibcode}",
                        limit=1,
                        fields=fields,
                    )
                )[0]

            self._data.update(x)

        return self._data[attr]

    def _identifer(self):
        if self.bibcode is not None:
            return f"identifier:{self.bibcode}"

        if "indentifier" in self._data:
            return f"identifier:{self.self._data['indentifier']}"

        if "alternate_bibcode" in self._data:
            return f"identifier:{self.self._data['alternate_bibcode']}"

        if "doi" in self._data:
            return f"identifier:{self.self._data['doi']}"

        if "arxiv" in self._data:
            return f"identifier:{self.self._data['arXiv']}"

        if "author" in self._data and "year" in self._data:
            return f'author:^{self._data["author"][0]} year:{self._data["year"]}'

    def keys(self):
        return _search._fields

    def items(self):
        return self._data.items()

    def values(self):
        return self._data.values()

    def __hash__(self):
        return hash(self.bibcode)

    def __eq__(self, value):
        if isinstance(value, article):
            if value.bibcode == self.bibcode:
                return True
        return False

    def __str__(self):
        return self.bibcode

    def __repr__(self):
        return self.bibcode

    def __dir__(self):
        return (
            list(self.keys())
            + list(self.__dict__.keys())
            + ["export", "metrics", "visual", "pdf"]
        )

    @property
    def export(self):
        return Export(self.bibcode)

    @property
    def metrics(self):
        return Metrics(self.bibcode)

    @property
    def visual(self):
        return Visualization(self.bibcode)

    @property
    def pdf(self):
        return PDF(self.bibcode)

    @property
    def url(self):
        return Urls(self.bibcode)

    def as_dict(self):
        return self._data

    def references(self):
        if "reference" in self._data:
            if self._data["reference"] is None:
                self._refs = journal()
            if not isinstance(self._refs, journal):
                self._refs = journal(bibcodes=self._data["reference"])
        else:
            data = pyastroapi.references(self.bibcode)
            self._refs = journal(data=data)

        return self._refs

    def reference_count(self):
        if "reference" not in self._data:
            return len(self.references())
        else:
            if self._data["reference"] is None:
                return 0
            else:
                return len(self._data["reference"])

    def citations(self):
        if self._cites is not None:
            return self._cites

        data = pyastroapi.citations(self.bibcode)

        self._cites = journal(data=data)

        return self._cites

    @property
    def first_author(self):
        if "author" not in self._data:
            self.__getattr__("author")
        return self.author[0]

    @property
    def authors(self):
        if "author" not in self._data:
            self.__getattr__("author")
        return self.author

    @property
    def name(self):
        return f"{self.first_author} {self.year}"

    @property
    def title(self):
        if "title" not in self._data:
            self.__getattr__("title")
        return self._data["title"][0]

    def __getstate__(self):
        return self.__dict__.copy()

    def __setstate__(self, state):
        self.__dict__.update(state)


class journal:
    def __init__(
        self,
        bibcodes: t.List = None,
        data: t.List = None,
        bibtex: str = None,
        search: str = None,
    ):
        self._data = {}

        if bibcodes is not None:
            self.from_bibcodes(bibcodes)
        elif data is not None:
            self.from_data(data)
        elif bibtex is not None:
            self.from_bibtex(bibtex)
        elif search is not None:
            self.from_search(search)

    def from_bibcodes(self, bibcodes: t.List):
        self._data = {}
        for bib in bibcodes:
            self.add_bibcode(bib)
        return self

    def from_data(self, data: t.List):
        self._data = {}
        self.add_data(data)

    def from_bibtex(self, bibtex: str):
        self._data = {}
        bd = bib.parse_bibtex(bibtex)
        for b in bd:
            self.add_data(pyastroapi.search(b, limit=1))

    def from_search(self, search: str):
        self._data = {}
        self.add_data(pyastroapi.search(search))

    def from_articles(self, data: t.List):
        self._data = {}
        self.add_articles(data)

    def add_bibcode(self, bibcode: t.List):
        self._data[bibcode] = article(bibcode=bibcode)

    def add_data(self, data: t.List):
        for dd in data:
            d = article(data=dd)
            self._data[d.bibcode] = d

    def add_articles(self, data: t.List):
        for dd in data:
            if isinstance(dd, article):
                self._data[dd.bibcode] = dd

    def add_bibtex(self, bibtex: str):
        raise NotImplementedError

    def bibcodes(self):
        return list(self.keys())

    def __getitem__(self, bibcode):
        if isinstance(bibcode, int):
            return self._data[list(self.keys())[bibcode]]
        else:
            return self._data[bibcode]

    def __len__(self):
        return len(self._data)

    def keys(self):
        return self._data.keys()

    def items(self):
        return self._data.items()

    def values(self):
        return self._data.values()

    def __contains__(self, key: str):
        return key in self._data

    def __iter__(self):
        yield from self._data

    def __dir__(self):
        return list(self.keys()) + list(self.__dict__.keys()) + _search._fields

    def __getattr__(self, attr):
        res = {}
        for bibcode in self.bibcodes():
            res[bibcode] = getattr(self._data[bibcode], attr)
        return res

    @property
    def export(self):
        return Export(self.bibcodes())

    @property
    def metrics(self):
        return Metrics(self.bibcodes())

    @property
    def visual(self):
        return Visualization(self.bibcodes())

    @property
    def pdf(self):
        return PDF(self.bibcodes())

    @property
    def url(self):
        return Urls(self.bibcodes())

    def pop(self, bibcodes):
        bibcodes = utils.ensure_list(bibcodes)
        for bib in bibcodes:
            if bib in self:
                self._data.pop(bib)

    def __str__(self):
        return f"Journal with {len(self.keys())} articles"

    def __getstate__(self):
        state = self.__dict__.copy()

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
