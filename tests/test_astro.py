# SPDX-License-Identifier: BSD-3-Clause
from pyastroapi import search

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
