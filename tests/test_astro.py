# SPDX-License-Identifier: BSD-3-Clause
from pyastroapi import search, articles

import pytest


@pytest.fixture(scope="module")
def vcr_config():
    def scrub_header(string, repl=""):
        """Remove secrets from stored vcr cassettes"""

        def before_record_response(response):
            response["headers"][string] = repl
            return response

        return before_record_response

    return {
        # Replace the Authorization request header with "DUMMY" in cassettes
        "filter_headers": [("authorization", "DUMMY")],
        "before_record_response": scrub_header("Set-Cookie", "DUMMY"),
    }


@pytest.mark.vcr()
class TestSearch:
    def test_basic(self):
        res = list(search.search("Farmer,r year:2021", fields="title"))
        assert len(res) == 10

        found = False
        for i in res:
            if i["title"] == ["rjfarmer/mesaplot: Release v1.1.0"]:
                found = True
                break

        assert found

    def test_citations(self):
        res = list(search.citations("2021ApJ...923..214F"))

        assert len(res)

    def test_references(self):
        res = list(search.references("2021ApJ...923..214F"))

        assert len(res)


@pytest.mark.vcr()
class TestArticle:
    def test_basic(self):
        a = articles.article("2021ApJ...923..214F")

        assert a.bibcode == "2021ApJ...923..214F"
        assert a.year == "2021"

    def test_misc(self):
        a = articles.article("2021ApJ...923..214F")

        assert len(a.citations())
        assert len(a.references())
        assert a.pdf.filename() == "2021ApJ...923..214F.pdf"

    def test_eq(self):
        a = articles.article("2021ApJ...923..214F")
        b = articles.article("2021ApJ...923..9999")
        c = articles.article("2021ApJ...923..214F")

        assert a != b
        assert a == c

    def test_bib(self):
        bib = """
        @ARTICLE{2021ApJ...923..214F,
       author = {{Farmer}, R. and {Laplace}, E. and {de Mink}, S.~E. and {Justham}, S.},
        title = "{The Cosmic Carbon Footprint of Massive Stars Stripped in Binary Systems}",
      journal = {\apj},
         year = 2021,
       volume = {923},
          doi = {10.3847/1538-4357/ac2f44},
       eprint = {2110.04131},
        }"""

        a = articles.article(bibtex=bib)

        assert a.bibcode == "2021ApJ...923..214F"
