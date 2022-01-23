# SPDX-License-Identifier: BSD-3-Clause
import pyadsapi.api.search as search
import pyadsapi.api.export as export
import pyadsapi.api.libraries as lib
import pyadsapi.api.metrics as metrics
import pyadsapi.api.author as author
import pyadsapi.api.citation_helper as cites
import pyadsapi.api.solr as solr


import pyadsapi.api.urls as urls
import pyadsapi.api.http as http

import pyadsapi.api.token as t


import pytest

token = t.get_token()


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
        res = list(search.search(token, "^farmer,r year:2020"))
        assert len(res) == 2

        expected = set(["2020zndo...3678482F", "2020ApJ...902L..36F"])
        actual = set([i["bibcode"] for i in res])

        assert expected == actual

    def test_fields(self):
        res = list(search.search(token, "^farmer,r year:2020", fields="page,volume"))

        assert len(res) == 2

        for i in res:
            if "page" in i:
                assert i["page"] == ["L36"]
            if "volume" in i:
                assert i["volume"] == "902"

    def test_bad_field(self):
        with pytest.raises(ValueError):
            res = list(search.search(token, "^farmer,r year:2020", fields="safdsgfdsg"))

    def test_no_results(self):
        res = list(search.search(token, "^farmer,r year:1600"))
        assert len(res) == 0

    def test_limit(self):
        res = list(search.search(token, "^farmer,r year:2020", limit=1))
        assert len(res) == 1

    def test_large(self):
        res = list(search.search(token, "^farmer", fields="bibcode", limit=100))
        assert len(res) == 100

    @pytest.mark.skip(reason="Broken")
    def test_bigquery(self):
        res = list(
            search.bigquery(token, ["2020zndo...3678482F", "2020ApJ...902L..36F"])
        )


@pytest.mark.vcr()
class TestExport:
    def test_ads(self):
        res = export.ads(token, "2020ApJ...902L..36F")

        assert len(res) == 1

    def test_bibtex(self):
        res = export.bibtex(token, "2020ApJ...902L..36F")

        assert len(res) == 1

        assert res[0].startswith("@ARTICLE{2020ApJ...902L..36F")

    def test_bib2(self):
        res = export.bibtex(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])

        assert len(res) == 2

        assert res[0].startswith("@ARTICLE{2020ApJ...902L..36F")
        assert res[1].startswith("@MISC{2020zndo...3678482F")


@pytest.mark.vcr()
class TestLib:
    def test_list_all(self):
        r = lib.list_all(token)
        assert "libraries" in r

        assert len(r["libraries"]) > 0

        assert "id" in r["libraries"][0]

    def test_permissions(self):
        r = lib.get_permissions(token, "qf-C6Zi-Tyad2vqJPS-I4g")

        assert r == [{"robert.j.farmer37@gmail.com": ["owner"]}]

    def test_get(self):
        r = list(lib.get(token, "qf-C6Zi-Tyad2vqJPS-I4g"))

        assert len(r) > 0

        assert len(r[0]) == 19  # Got a bibcode like string

    def test_add_remove(self):
        r = list(lib.get(token, "qf-C6Zi-Tyad2vqJPS-I4g"))

        lib.add(token, "qf-C6Zi-Tyad2vqJPS-I4g", "2021ApJ...923..214F")

        r2 = list(lib.get(token, "qf-C6Zi-Tyad2vqJPS-I4g"))

        assert len(r) == len(r2) - 1  # We added one new bibcode

        lib.remove(token, "qf-C6Zi-Tyad2vqJPS-I4g", "2021ApJ...923..214F")

        r3 = list(lib.get(token, "qf-C6Zi-Tyad2vqJPS-I4g"))

        assert len(r) == len(r3)  # Then we removed it

    def test_make_new_and_del(self):
        r = lib.list_all(token)

        lib_new = lib.new(token, "test_123465789")

        r2 = lib.list_all(token)

        assert len(r2["libraries"]) - 1 == len(r["libraries"])  # Added new library

        # Check its there
        in_lib = False
        check_name = False
        for i in r2["libraries"]:
            if i["id"] == lib_new["id"]:
                in_lib = True
            if i["name"] == "test_123465789":
                check_name = True

        assert in_lib
        assert check_name

        lib.delete(token, lib_new["id"])

        r2 = lib.list_all(token)

        assert len(r2["libraries"]) == len(r["libraries"])  # Removed library


@pytest.mark.vcr()
class TestMetrics:
    def test_basic(self):
        r = metrics.basic(token, "2020ApJ...902L..36F")

        assert len(r["skipped bibcodes"]) == 0

        assert r["basic stats"]["number of papers"] == 1

    def test_citations(self):
        r = metrics.citations(token, "2020ApJ...902L..36F")

        assert len(r["skipped bibcodes"]) == 0

        assert r["citation stats"]["number of citing papers"] > 0

    def test_histograms(self):
        r = metrics.histograms(token, "2020ApJ...902L..36F")

        assert len(r["skipped bibcodes"]) == 0

        assert r["histograms"]["reads"]["all reads"]["1996"] == 0

    def test_skip(self):
        r = metrics.citations(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])

        assert r["skipped bibcodes"][0] == "2020zndo...3678482F"

    def test_multi(self):
        r = metrics.basic(token, ["2020ApJ...902L..36F", "2019ApJ...887...53F"])

        assert r["basic stats"]["number of papers"] == 2


@pytest.mark.vcr()
class TestAuthor:
    def test_one(self):
        r = author.search(token, "2020ApJ...902L..36F")

        assert len(r) == 5

        assert "authorName" in r[0]

    def test_multi(self):
        r = author.search(token, ["2019ApJ...887...53F", "2020ApJ...902L..36F"])

        assert len(r) == 10

        assert "authorName" in r[0]


@pytest.mark.vcr()
class TestCitations:
    def test_one(self):
        with pytest.raises(TypeError):
            r = cites.citations(token, "2019ApJ...887...53F")

    def test_multi(self):
        r = cites.citations(token, ["2019ApJ...887...53F", "2020ApJ...902L..36F"])

        assert len(r) == 10

        assert "bibcode" in r[0]


@pytest.mark.vcr()
class TestSolr:
    def test_query(self):
        r = solr.query(token, "M31")

        assert (
            r
            == "((=abs:M31 OR simbid:1575544 OR nedid:MESSIER_031) database:astronomy)"
        )

    def test_simbad(self):
        r = solr.simbad(token, "1575544")

        assert r == {"1575544": {"canonical": "M  31", "id": "1575544"}}

    def test_objects(self):
        r = solr.objects(token, "M31")

        assert r == {"M31": {"canonical": "M  31", "id": "1575544"}}
