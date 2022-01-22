# SPDX-License-Identifier: BSD-3-Clause
import pyadsapi.api.search as s
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
        res = list(s.search(token, "^farmer,r year:2020"))
        assert len(res) == 2

        expected = set(["2020zndo...3678482F", "2020ApJ...902L..36F"])
        actual = set([i["bibcode"] for i in res])

        assert expected == actual

    def test_fields(self):
        res = list(s.search(token, "^farmer,r year:2020", fields=["page", "volume"]))

        assert len(res) == 2

        for i in res:
            if "page" in i:
                assert i["page"] == ["L36"]
            if "volume" in i:
                assert i["volume"] == "902"
