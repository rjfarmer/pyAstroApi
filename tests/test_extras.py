# SPDX-License-Identifier: BSD-3-Clause
import pyastroapi.extras.urls as urls

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
class TestUrls:
    def test_ads(self):
        assert urls.parse_url(
            "https://ui.adsabs.harvard.edu/abs/2020ApJ...902L..36F/abstract"
        ) == {"identifier": "2020ApJ...902L..36F"}
        assert urls.parse_url(
            "https://ui.adsabs.harvard.edu/link_gateway/2020ApJ...902L..36F/PUB_PDF"
        ) == {"identifier": "2020ApJ...902L..36F"}
        assert urls.parse_url(
            "https://ui.adsabs.harvard.edu/abs/2020ApJ...902L..36F"
        ) == {"identifier": "2020ApJ...902L..36F"}

    def test_arxiv(self):
        assert urls.parse_url("https://arxiv.org/abs/2006.06678") == {
            "identifier": "2006.06678"
        }
        assert urls.parse_url("https://arxiv.org/pdf/2006.06678") == {
            "identifier": "2006.06678"
        }
        assert urls.parse_url("https://arxiv.org/pdf/2006.06678v1") == {
            "identifier": "2006.06678"
        }
