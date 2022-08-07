# SPDX-License-Identifier: BSD-3-Clause
import pyastroapi

import pyastroapi.urls as urls

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
        res = list(pyastroapi.search("Farmer,r year:2021", fields="title", limit=10))
        assert len(res) == 10

        found = False
        for i in res:
            if i["title"] == [
                "The Cosmic Carbon Footprint of Massive Stars Stripped in Binary Systems"
            ]:
                found = True
                break

        assert found

    def test_citations(self):
        res = list(pyastroapi.citations("2021ApJ...923..214F"))

        assert len(res)

    def test_references(self):
        res = list(pyastroapi.references("2021ApJ...923..214F"))

        assert len(res)


@pytest.mark.vcr()
class TestArticle:
    def test_basic(self):
        a = pyastroapi.article("2021ApJ...923..214F")

        assert a.bibcode == "2021ApJ...923..214F"
        assert a.year == "2021"

    def test_misc(self):
        a = pyastroapi.article("2021ApJ...923..214F")

        assert a.citation_count > 0
        assert len(a.citations())
        assert a.citation_count == len(a.citations())

        assert a.reference_count() == 136
        assert len(a.references())
        assert len(a.references()) == a.reference_count()
        assert a.pdf.filename() == "2021ApJ...923..214F.pdf"

    def test_eq(self):
        a = pyastroapi.article("2021ApJ...923..214F")
        b = pyastroapi.article("2021ApJ...923..9999")
        c = pyastroapi.article("2021ApJ...923..214F")

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

        a = pyastroapi.article(bibtex=bib)

        assert a.bibcode == "2021ApJ...923..214F"


@pytest.mark.vcr()
class TestUrls:
    def test_ads(self):
        assert urls.parse_url(
            "https://ui.adsabs.harvard.edu/abs/2020ApJ...902L..36F/abstract"
        ) == {"bibcode": "2020ApJ...902L..36F"}
        assert urls.parse_url(
            "https://ui.adsabs.harvard.edu/link_gateway/2020ApJ...902L..36F/PUB_PDF"
        ) == {"bibcode": "2020ApJ...902L..36F"}
        assert urls.parse_url(
            "https://ui.adsabs.harvard.edu/abs/2020ApJ...902L..36F"
        ) == {"bibcode": "2020ApJ...902L..36F"}

    def test_arxiv(self):
        assert urls.parse_url("https://arxiv.org/abs/2006.06678") == {
            "arxiv": "2006.06678"
        }
        assert urls.parse_url("https://arxiv.org/pdf/2006.06678") == {
            "arxiv": "2006.06678"
        }
        assert urls.parse_url("https://arxiv.org/pdf/2006.06678v1") == {
            "arxiv": "2006.06678"
        }
