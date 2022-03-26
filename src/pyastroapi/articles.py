# # SPDX-License-Identifier: BSD-3-Clause


# class article(object):
#     """
#     A single article that is given by either a bibcode, arxic id, or doi.
#     Bibcodes are allways the prefered ID as the doi or arxiv id we query  ADS for its bibcode.

#     We defer actually searching the ads untill the user asks for a field.
#     Thus we can make as many article as we want (if we allready know the bibcode)
#     without hitting the ADS api limits.
#     """

#     def __init__(self, adsdata, bibcode=None, data=None):
#         self.adsdata = adsdata
#         self._bibcode = bibcode
#         self._data = None
#         self._citations = None
#         self._references = None
#         self.which_file = None

#         if data is not None:
#             self.data = data
#             self.bibcode = self.data["bibcode"]

#     def search(self, force=False):
#         if self.data is None or force:
#             self.data = self.adsdata.search.bibcode_single(self.bibcode)

#     @property
#     def bibcode(self):
#         return self._bibcode

#     @property.setter
#     def bibcode(self, bibcode):
#         self._bibcode = bibcode

#     @property
#     def data(self):
#         if self._data is None:
#             self.search()

#         return self._data

#     @property.setter
#     def data(self, new_data):
#         self._data = new_data

#     def __gettattr__(self, key):
#         return self.data[key]

#     def __getitem__(self, key):
#         return self.data[key]

#     @property
#     def title(self):
#         return self.data["title"][0]

#     @property
#     def authors(self):
#         return "; ".join(self.data["author"])

#     @property
#     def author(self):
#         return self.authors

#     @property
#     def first_author(self):
#         return self.data["author"][0]

#     @property
#     def journal(self):
#         return self.data["bibstem"][0]

#     def filename(self):
#         return self.bibcode + ".pdf"

#     @property
#     def year(self):
#         return self.data["year"]

#     @property
#     def abstract(self):
#         if "abstract" in self.data:
#             return self.data["abstract"]
#         else:
#             return ""

#     @property
#     def name(self):
#         return self.first_author + " " + self.year

#     @property
#     def ads_url(self):
#         return "https://ui.adsabs.harvard.edu/abs/" + self.bibcode

#     @property
#     def arxiv_url(self):
#         arxiv_id = None
#         for i in self.data["identifier"]:
#             if i.startswith("arXiv:"):
#                 arxiv_id = i.replace("arXiv:", "")

#         if arxiv_id is not None:
#             return "https://arxiv.org/abs/" + arxiv_id
#         else:
#             return ""

#     @property
#     def journal_url(self):
#         doi = None
#         for i in self.data["identifier"]:
#             if i.startswith("10."):
#                 doi = i
#         if doi is not None:
#             return "https://doi.org/" + doi
#         else:
#             return ""

#     @property
#     def citation_count(self):
#         if "citation_count" not in self.data:
#             return 0
#         else:
#             return self.data["citation_count"]

#     @property
#     def reference_count(self):
#         if "reference" not in self.data:
#             return 0
#         else:
#             return len(self.data["reference"])

#     def pdf(self, filename):
#         # There are multiple possible locations for the pdf
#         # Try to avoid the journal links as that usally needs a
#         # vpn working to use a university ip address
#         strs = ["/PUB_PDF", "/EPRINT_PDF", "/ADS_PDF"]

#         if os.path.exists(filename):
#             return

#         got_file = False
#         for i in strs:
#             url = urls.urls["pdfs"] + str(self.bibcode) + i

#             # Pretend to be Firefox otherwise we hit captchas
#             headers = {"user-agent": "Mozilla /5.0 (Windows NT 10.0; Win64; x64)"}
#             try:
#                 r = requests.get(url, allow_redirects=True, headers=headers)
#             except requests.exceptions.RequestException:
#                 continue

#             if r.content.startswith(b"<!DOCTYPE html"):
#                 continue

#             with open(filename, "wb") as f:
#                 f.write(r.content)
#                 self.which_file = i
#                 got_file = True
#                 break

#         if not os.path.exists(filename):
#             raise utils.FileDonwnloadFailed("Couldn't download file")

#     def citations(self):
#         if self._citations is None:
#             self._citations = self.adsdata.search(
#                 'citations(bibcode:"' + self.bibcode + '")'
#             )
#         return self._citations

#     def references(self):
#         if self._references is None:
#             self._references = self.adsdata.search(
#                 'references(bibcode:"' + self.bibcode + '")'
#             )
#         return self._references

#     def bibtex(self):
#         data = {"bibcode": [self.bibcode]}
#         r = requests.post(
#             urls.urls["bibtex"],
#             auth=utils._BearerAuth(self.adsdata.token),
#             headers={"Content-Type": "application/json"},
#             json=data,
#         ).json()

#         if "error" in r:
#             raise ValueError(r["error"])

#         return r["export"]

#     def __str__(self):
#         return self.name

#     def __reduce__(self):
#         return (article, (self.adsdata, self.bibcode))

#     def __hash__(self):
#         return hash(self.bibcode)

#     def __eq__(self, value):
#         if isinstance(value, article):
#             if value.bibcode == self.bibcode:
#                 return True
#         return False

import inspect


import pyastroapi.api.search as search
import pyastroapi.api.token as token
import pyastroapi.api.utils as utils


import pyastroapi.api.export as _export
import pyastroapi.api.metrics as _metrics
import pyastroapi.api.visualization as _visualization
import pyastroapi.api.resolver as _resolve
import pyastroapi.api.http as _http

import typing as t


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

        self.bibcode = bibcode
        links = _resolve.esource(token.get_token(), bibcode)
        self.links = {}
        if "links" not in links:
            raise ValueError("No pdf links available")

        for i in links["links"]["records"]:
            self.links[i["link_type"]] = i["url"]

    def filename(self):
        return f"{self.bibcode}.pdf"

    def _download(self, source, name, filename=None):
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


class article:
    def __init__(self, bibcode: str = None, data: t.Dict = None, bibtex: str = None):
        self.bibcode = None
        self._data = {}

        self._refs = None
        self._cites = None

        if bibcode is not None:
            self.from_bibcode(bibcode)
        elif data is not None:
            self.from_data(data)
        elif bibtex is not None:
            self.from_bibtex(bibtex)

    def from_bibcode(self, bibcode: str):
        self.bibcode = bibcode
        self._data = {}
        self._data["bibcode"] = self.bibcode

    def from_data(self, data: t.Dict):
        self._data = data
        if "bibcode" in self._data:
            self.bibcode = self._data["bibcode"]

    def from_bibtex(self, bibtex: str):
        raise NotImplementedError
        # return self.bibcode

    def add_to_lib(self, libaray: str):
        raise NotImplementedError

    def __getattr__(self, attr: str):
        if attr not in self._data:
            if "bibcode" not in self._data:
                raise ValueError("Bibcode must be set first")

            fields = ""
            if len(self._data) == 1:  # Load basic data
                fields = search._short_fl

            if (
                attr not in self._data and attr not in fields
            ):  # Add field if we dont have it allready
                fields = f"{attr}," + fields

            x = list(
                search.search(
                    token.get_token(),
                    query=f"bibcode:{self.bibcode}",
                    limit=1,
                    fields=fields,
                )
            )[0]

            self._data = {**self._data, **x}

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
        return search._fields

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

    def __reduce__(self):
        return (article, (None, self._data, None))

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

    def as_dict(self):
        return self._data

    def references(self):
        if self._refs is not None:
            return self._refs

        data = search.search(
            token.get_token(),
            query=f"references:({self.bibcode})",
        )

        self._refs = journal()
        for bib in data:
            self._refs.add_data(bib)

        return self._refs

    def citations(self):
        if self._cites is not None:
            return self._cites

        data = search.search(
            token.get_token(),
            query=f"citations({self.bibcode})",
        )

        self._cites = journal()
        for bib in data:
            self._cites.add_data(bib)

        return self._cites


class journal:
    def __init__(
        self, bibcodes: t.List = None, data: t.List = None, bibtex: str = None
    ):
        self._data = {}

        if bibcodes is not None:
            self.from_bibcodes(bibcodes)
        elif data is not None:
            self.from_data(data)
        elif bibtex is not None:
            self.from_bibtex(bibtex)

    def from_bibcodes(self, bibcodes: t.List):
        self._data = {}
        for bib in bibcodes:
            self.add_bibcode(bib)

    def from_data(self, data: t.List):
        self._data = {}
        self.add_data(data)

    def from_bibtex(self, bibtex: str):
        self._data = {}
        raise NotImplementedError

    def add_bibcode(self, bibcode: t.List):
        self._data[bibcode] = article(bibcode=bibcode)

    def add_data(self, data: t.List):
        for data in data:
            d = article(data=data)
            self._data[d.bibcode] = d

    def add_bibtex(self, bibtex: str):
        raise NotImplementedError

    def bibcodes(self):
        return list(self.keys())

    def __getitem__(self, bibcode):
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

    def __reduce__(self):
        return (journal, (None, self._data, None))

    def __dir__(self):
        return list(self.keys()) + list(self.__dict__.keys()) + search._fields

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

    def pop(self, bibcodes):
        bibcodes = utils.ensure_list(bibcodes)
        for bib in bibcodes:
            if bib in self:
                self._data.pop(bib)
