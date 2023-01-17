# SPDX-License-Identifier: BSD-3-Clause
import pyastroapi

import pytest
import pickle
import tempfile
import os


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

        assert a.reference_count() == 99
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

    def test_pickle(self):
        a = pyastroapi.article("2021ApJ...923..214F")

        x = a.title

        tp = tempfile.mktemp(dir="./")
        with open(tp, "wb") as f:
            pickle.dump(a, f)

        with open(tp, "rb") as f:
            b = pickle.load(f)

        assert a.bibcode == b.bibcode
        assert x == b.title
        os.remove(tp)

    def test_pickle_journal(self):
        a = pyastroapi.journal(["2021ApJ...923..214F", "2021ApJ...923..9999"])

        x = a["2021ApJ...923..214F"].title

        tp = tempfile.mktemp(dir="./")
        with open(tp, "wb") as f:
            pickle.dump(a, f)

        with open(tp, "rb") as f:
            b = pickle.load(f)

        assert len(a) == len(b)
        assert x == b["2021ApJ...923..214F"].title
        os.remove(tp)


@pytest.mark.vcr()
class TestJournal:
    def test_bibcodes(self):
        # Bug: https://github.com/rjfarmer/pyAstroApi/issues/1
        journal = pyastroapi.journal(
            bibcodes=["2018araa.book.....P", "2013A&A...557A..84P"]
        )

        titles = [
            "Astrophysical Recipes; The art of AMUSE",
            "The Astrophysical Multipurpose Software Environment",
        ]
        refs = [549, 68]

        for paper, title, ref in zip(journal, titles, refs):
            assert type(paper) == pyastroapi.article
            assert paper.title == title
            assert paper.reference_count() == ref

    def test_citations(self):
        a = pyastroapi.journal(bibcodes=["2015arXiv151102820P", "2017zndo....846305F"])

        z = a.citations()

        assert len(z) > 2
        assert "2016MNRAS.461.3296N" in z
        assert (
            z["2016MNRAS.461.3296N"].title
            == "Multimessenger signals of long-term core-collapse supernova simulations: synergetic observation strategies"
        )

    def test_references(self):
        a = pyastroapi.journal(bibcodes=["2015arXiv151102820P", "2017zndo....846305F"])

        z = a.references()

        assert len(z) > 2
        assert "2011ApJS..192....3P" in z
        assert (
            z["2011ApJS..192....3P"].title
            == "Modules for Experiments in Stellar Astrophysics (MESA)"
        )
