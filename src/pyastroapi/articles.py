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
import pyastroapi.extras.bibtex as bib

__all__ = ["article", "journal"]


_t_bibcode = t.Union[str, t.List[str]]


class article:
    def __init__(
        self,
        bibcode: str = None,
        data: t.Dict = None,
        bibtex: str = None,
        search: str = None,
    ):
        """Creates an article

        This is the base class foe interacting with a single paper

        Args:
            bibcode (str, optional): Point to paper given by a bibcode. Defaults to None.
            data (t.Dict, optional): Initialize the article from a dict containing at least a "bibcode" key . Defaults to None.
            bibtex (str, optional): Initialize given a bibtex string. Must contain only one document. Defaults to None.
            search (str, optional): Initialize after performing a query of ADS with the search string. We only return the first result from the search. Defaults to None.
        """

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
        """Set the article to point to the paper given by bibcode

        Args:
            bibcode (str): ADS bibcode
        """
        self.bibcode = bibcode
        self._data["bibcode"] = self.bibcode

    def from_data(self, data: t.Dict):
        """Initialize given a dict containing atleast a bibcode key

        Args:
            data (t.Dict): Dictionary of data
        """
        self._data = data
        if "bibcode" in self._data.keys():
            self.bibcode = self._data["bibcode"]

    def from_bibtex(self, bibtex: str):
        """Initialize given a bibtex fragment

        Args:
            bibtex (str): A bibtex document as a string
        """
        bd = bib.parse_bibtex(bibtex)
        self.from_data(list(pyastroapi.search(bd[0], limit=1))[0])

    def from_search(self, search: str):
        """Perform a search of ADS and return only the first result

        Args:
            search (str): An ADS search query
        """
        self._query = search
        self.from_data(list(pyastroapi.search(search, limit=1))[0])

    def add_to_lib(self, library: str):
        """Add article to the ADS library

        Args:
            library (str): An existing ADS library

        Raises:
            NotImplementedError: _description_
        """
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
        """Return all available fields

        Returns:
            _type_: _description_
        """
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
        """Get a journal of references to this paper.

        Returns:
            _type_: _description_
        """
        if "reference" in self._data:
            if self._data["reference"] is None:
                self._refs = journal()
            if not isinstance(self._refs, journal):
                self._refs = journal(bibcodes=self._data["reference"])
        else:
            data = pyastroapi.references(self.bibcode)
            self._refs = journal(data=data)

        return self._refs

    def reference_count(self) -> int:
        """Get a count of the references to this paper.

        Returns:
            int: _description_
        """
        if "reference" not in self._data:
            return len(self.references())
        else:
            if self._data["reference"] is None:
                return 0
            else:
                return len(self._data["reference"])

    def citations(self):
        """Get the citations to this paper.

        Returns:
            _type_: _description_
        """
        if self._cites is not None:
            return self._cites

        data = pyastroapi.citations(self.bibcode)

        self._cites = journal(data=data)

        return self._cites

    @property
    def first_author(self) -> str:
        """Return the first author of the paper.

        Returns:
            str: _description_
        """
        if "author" not in self._data:
            self.__getattr__("author")
        return self.author[0]

    @property
    def authors(self) -> t.List[str]:
        """Return a list of authors"""
        if "author" not in self._data:
            self.__getattr__("author")
        return self.author

    @property
    def name(self) -> str:
        """Make a pretty name for the paper (First author year)"""
        return f"{self.first_author} {self.year}"

    @property
    def title(self) -> str:
        """Return the paper title.

        Returns:
            str: _description_
        """
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
        """Creates an journal

        This is the base class foe interacting with one or more papers

        The from_ functions will reset the data stored, while add_ adds any new entries.

        Args:
            bibcodes (list, optional): List of bibcodes. Defaults to None.
            data (t.Dict, optional): Initialize the journal from a list of dicts. Each dict must have at least a "bibcode" key. Defaults to None.
            bibtex (str, optional): Initialize given a bibtex string. Must contain only one document. Defaults to None.
            search (str, optional): Initialize after performing a query of ADS with the search string. Defaults to None.
        """

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
        """Initialize from a list of bibcodes

        Args:
            bibcodes (t.List):

        Returns:
            self
        """
        self._data = {}
        for bib in bibcodes:
            self.add_bibcode(bib)
        return self

    def from_data(self, data: t.List):
        """Initialize from a list of dict-like objects

        Each element must have at least a "bibcode" key

        Args:
            data (t.List): List of dict-like objects
        """
        self._data = {}
        self.add_data(data)

    def from_bibtex(self, bibtex: str):
        """Initialize from a bibtex string

        Args:
            bibtex (str): A bibtex string of one or more bibtex's
        """
        self._data = {}
        self.add_bibtex(bibtex)

    def from_search(self, search: str):
        """Initialize from an ADS search

        Args:
            search (str): ADS query string
        """
        self._data = {}
        self.add_data(pyastroapi.search(search))

    def from_articles(self, data: t.List):
        """Initialize from list of articles

        Args:
            data (t.List): List of articles
        """
        self._data = {}
        self.add_articles(data)

    def add_bibcode(self, bibcode: t.List):
        """Add papers given by bibcodes

        Args:
            bibcode (t.List): List of bibcodes
        """
        self._data[bibcode] = article(bibcode=bibcode)

    def add_data(self, data: t.List):
        """Add papers from list of dict-like objects

        Args:
            data (t.List): List of dict-like objects. Each element must have at least "bibcode" as a key
        """
        for dd in data:
            d = article(data=dd)
            self._data[d.bibcode] = d

    def add_articles(self, data: t.List):
        """Add papers from a list of articles

        Args:
            data (t.List): List of articles
        """
        for dd in data:
            if isinstance(dd, article):
                self._data[dd.bibcode] = dd

    def add_bibtex(self, bibtex: str):
        """Add papers from bibtex

        Args:
            bibtex (str): One of more bibtex's
        """
        bd = bib.parse_bibtex(bibtex)
        for b in bd:
            self.add_data(pyastroapi.search(b, limit=1))

    def bibcodes(self):
        """Returns the list of bibcodes in the journal

        Returns:
            bibcodes (list): List of bibcodes
        """
        return list(self.keys())

    def __getitem__(self, bibcode):
        if isinstance(bibcode, int):
            return self._data[list(self.keys())[bibcode]]
        else:
            return self._data[bibcode]

    def __len__(self):
        return len(self._data)

    def keys(self):
        """Return list of keys (bibcodes)"""
        return self._data.keys()

    def items(self):
        """Returns the items (bibcode and article) for each paper."""
        return self._data.items()

    def values(self):
        """Return stored values

        Returns:
            _type_: _description_
        """
        return self._data.values()

    def __contains__(self, key: str):
        return key in self._data

    def __iter__(self):
        yield from self._data

    def __dir__(self):
        return list(self.keys()) + list(self.__dict__.keys()) + list(_search._fields)

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

    def pop(self, bibcodes):
        """Remove one or more bibcodes

        Args:
            bibcodes (str or list[str]): One or more bibcodes to remove
        """
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

    def citations(self):
        """Get the citations to all papers in journal.

        This does not remove duplicates

        Returns:
            _type_: _description_
        """
        data = {}
        for paper in self:
            data[paper.bibcode] = paper.citations

        return data

    def references(self):
        """Get the references to all papers in the journal

        This does not remove duplicates

        Returns:
            _type_: _description_
        """
        data = {}
        for paper in self:
            data[paper.references] = paper.references

        return data

    def citation_count(self, uniq=False) -> int:
        """Return count of citations to all papers in journal

        Args:
            uniq (bool, optional): If true remove duplicated citations. Defaults to False.

        Returns:
            int: Count of all citations
        """
        res = 0
        res_uniq = []
        for paper in self:
            res += paper.citation_count()
            if uniq:
                res_uniq.extend(paper.citations)

        if uniq:
            return len(set(res_uniq))
        else:
            return res

    def reference_count(self, uniq=False) -> int:
        """Return count of references to all papers in journal

        Args:
            uniq (bool, optional): If true remove duplicated references. Defaults to False.

        Returns:
            int: Count of all references
        """
        res = 0
        res_uniq = []
        for paper in self:
            res += paper.reference_count()
            if uniq:
                res_uniq.extend(paper.references)

        if uniq:
            return len(set(res_uniq))
        else:
            return res


class Export:
    """Class handles accessing various citation methods (bibtex, refworks, etc)

    The full list is generated dynamically

    """

    def __init__(self, bibcodes: _t_bibcode):
        self.bibcodes = utils.ensure_list(bibcodes)

    def __getattr__(self, attr: str):
        return getattr(_export, attr)(token.get_token(), self.bibcodes)

    def __dir__(self):
        return dir(_export)


class Metrics:
    """Class handles various metrics (citations per year, etc)"""

    def __init__(self, bibcodes: _t_bibcode):
        self.bibcodes = utils.ensure_list(bibcodes)

    def __getattr__(self, attr: str):
        return getattr(_metrics, attr)(token.get_token(), self.bibcodes)

    def __dir__(self):
        return dir(_metrics)


class Visualization:
    """Class handles visulization of a list of bibcodes"""

    def __init__(self, bibcodes: _t_bibcode):
        self.bibcodes = utils.ensure_list(bibcodes)

    def __getattr__(self, attr: str):
        return getattr(_visualization, attr)(token.get_token(), self.bibcodes)

    def __dir__(self):
        return dir(_visualization)


class PDF:
    """Class handles getting the url for pdf downloads

    Not every bibcode has all possible download options
    """

    def __init__(self, bibcode: str):
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

    def filename(self) -> str:
        """Gets the filename for a bibcode

        Returns:
            str : bibcode.pdf
        """
        return f"{self.bibcode}.pdf"

    def _download(self, source: str, name: str, filename: str = None):
        """Downloads a file

        Args:
            source (str): Which version of the file to download
            name (str): Bibcode
            filename (str, optional): The filename to save to, Defaults to self.filename()

        Raises:
            ValueError: If requested url does not exist for this paper
        """
        if self.links is None:
            self._get()

        if source not in self.links:
            raise ValueError(f"No {name} pdf available for {self.bibcode}")

        if filename is None:
            filename = self.filename()

        print(self.links[source], filename)
        _http.download_file(self.links[source], filename)

    def arxiv(self, filename: str = None) -> str:
        """Try to download from the arxiv

        Args:
            filename (str, optional): Filename to save pdf to. Defaults to self.filename()

        Returns:
            str: Filename used for saving
        """
        self._download("ESOURCE|EPRINT_PDF", "Arxiv", filename)
        return filename

    def publisher(self, filename: str = None) -> str:
        """Try to download from the journal

        Many journals will return a html captcha page instead. So be prepared to handle
        the download failing

        Args:
            filename (str, optional): Filename to save pdf to. Defaults to self.filename()

        Returns:
            str: Filename used for saving
        """
        self._download("ESOURCE|PUB_PDF", "Publisher", filename)
        return filename

    def ads(self, filename: str = None) -> str:
        """Try to download from ADS

        Some (mostly older) papers are stored only with ADS

        Args:
            filename (str, optional): Filename to save pdf to. Defaults to self.filename()

        Returns:
            str: Filename used for saving
        """
        self._download("ESOURCE|ADS_PDF", "ADSABS", filename)
        return filename


class Urls:
    """Class handles accessing the URL's to a paper"""

    def __init__(self, bibcode: str):
        if isinstance(bibcode, list):
            raise TypeError("Can only handle one pdf at a time")

        self.bibcode = bibcode
        links = _resolve.esource(token.get_token(), bibcode)
        self.links = {}
        if "links" not in links:
            raise ValueError("No pdf links available")

        for i in links["links"]["records"]:
            self.links[i["link_type"]] = i["url"]

    def _get(self, source: str, name: str):
        if source not in self.links:
            raise ValueError(f"No {name} html available for {self.bibcode}")

    @property
    def ads(self) -> str:
        """Get the ADSABS URL

        Returns:
            str: ADS URL
        """
        return f"https://ui.adsabs.harvard.edu/abs/{self.bibcode}"

    @property
    def arixv(self) -> str:
        """Get the arxiv URL

        Returns:
            str: _Arxiv URL
        """
        return self._get("ESOURCE|EPRINT_HTML", "Arxiv")

    @property
    def journal(self) -> str:
        """Get the journal URL

        Returns:
            str: Journal URL
        """
        tries = ["ESOURCE", "ESOURCE|HTML", "PUB_HTML", "AUTHOR_HTML"]

        for link in tries:
            if link in self.links:
                return self._get(link, "Journal")
