# SPDX-License-Identifier: BSD-3-Clause
import pyadsapi.api.search as search
import pyadsapi.api.export as export
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
