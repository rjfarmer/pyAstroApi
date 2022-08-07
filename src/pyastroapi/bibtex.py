import bibtexparser
from bibtexparser.bparser import BibTexParser

__all__ = ["parse_file", "parse_bibtex"]

_parser = BibTexParser(common_strings=True)


def parse_file(filename):
    with open(filename) as f:
        bd = bibtexparser.load(f, _parser)
    return _extract_from(bd)


def parse_bibtex(bibtex):
    bd = bibtexparser.loads(bibtex, _parser)
    return _extract_from(bd)


def _extract_from(bibtex_db):
    """Get identifier(s) from bibtex data

    Returns a list of adsabs queries
    """

    result = []

    for i in bibtex_db.entries:
        if "ID" in i:
            if len(i["ID"]) == 19:
                result.append(f'identifier:{i["ID"]}')
        elif "doi" in i:
            result.append(f'identifier:{i["doi"]}')
        elif "eprint" in i:
            result.append(f'identifier:{i["eprint"]}')
        else:  # Fallback
            t = i["title"]
            t.replace("}{", "")
            result.append(f'title:"{t}" year:{i["year"]}')

    return result
