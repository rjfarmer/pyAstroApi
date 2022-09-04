# SPDX-License-Identifier: BSD-3-Clause
import pyastroapi.api.search as search
import pyastroapi.api.export as export
import pyastroapi.api.libraries as lib
import pyastroapi.api.metrics as metrics
import pyastroapi.api.author as author
import pyastroapi.api.citation_helper as cites
import pyastroapi.api.solr as solr
import pyastroapi.api.reference as ref
import pyastroapi.api.resolver as resolve
import pyastroapi.api.visualization as visual
import pyastroapi.api.recommender as recommend
import pyastroapi.api.classic as classic
import pyastroapi.api.stored as stored
import pyastroapi.api.notifications as notif

import pyastroapi.api.urls as urls
import pyastroapi.api.http as http

import pyastroapi.api.token as t
import pyastroapi.api.exceptions as e

import pytest
import tempfile
import os

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
class TestAPISearch:
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
            if "page" in i and i["page"] is not None:
                assert i["page"] == ["L36"]
            if "volume" in i and i["volume"] is not None:
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

    def test_bigquery(self):
        res = search.bigquery(token, ["2020zndo...3678482F", "2020ApJ...902L..36F"])

        docs = res["docs"]

        assert res["numFound"] == 2
        assert (
            "2020zndo...3678482F" == docs[0]["bibcode"]
            or "2020zndo...3678482F" == docs[1]["bibcode"]
        )


@pytest.mark.vcr()
class TestAPIExport:
    def test_ads_1(self):
        res = export.ads(token, "2020ApJ...902L..36F")
        assert len(res) == 1

    def test_ads_2(self):
        res = export.ads(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])
        assert len(res) == 2

    def test_bibtexabs_1(self):
        res = export.bibtexabs(token, "2020ApJ...902L..36F")
        assert len(res) == 1

    def test_bibtexabs_2(self):
        res = export.bibtexabs(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])
        assert len(res) == 2

    def test_bibtex_1(self):
        res = export.bibtex(token, "2020ApJ...902L..36F")
        assert len(res) == 1

    def test_bibtex_2(self):
        res = export.bibtex(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])
        assert len(res) == 2

    def test_endnote_1(self):
        res = export.endnote(token, "2020ApJ...902L..36F")
        assert len(res) == 1

    def test_endnote_2(self):
        res = export.endnote(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])
        assert len(res) == 2

    def test_medlars_1(self):
        res = export.medlars(token, "2020ApJ...902L..36F")
        assert len(res) == 1

    def test_medlars_2(self):
        res = export.medlars(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])
        assert len(res) == 2

    def test_procite_1(self):
        res = export.procite(token, "2020ApJ...902L..36F")
        assert len(res) == 1

    def test_procite_2(self):
        res = export.procite(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])
        assert len(res) == 2

    def test_refworks_1(self):
        res = export.refworks(token, "2020ApJ...902L..36F")
        assert len(res) == 1

    def test_refworks_2(self):
        res = export.refworks(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])
        assert len(res) == 2

    def test_ris_1(self):
        res = export.ris(token, "2020ApJ...902L..36F")
        assert len(res) == 1

    def test_ris_2(self):
        res = export.ris(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])
        assert len(res) == 2

    def test_aastex_1(self):
        res = export.aastex(token, "2020ApJ...902L..36F")
        assert len(res) == 1

    def test_aastex_2(self):
        res = export.aastex(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])
        assert len(res) == 2

    def test_icarus_1(self):
        res = export.icarus(token, "2020ApJ...902L..36F")
        assert len(res) == 1

    def test_icarus_2(self):
        res = export.icarus(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])
        assert len(res) == 2

    def test_mnras_1(self):
        res = export.mnras(token, "2020ApJ...902L..36F")
        assert len(res) == 1

    def test_mnras_2(self):
        res = export.mnras(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])
        assert len(res) == 2

    def test_soph_1(self):
        res = export.soph(token, "2020ApJ...902L..36F")
        assert len(res) == 1

    def test_soph_2(self):
        res = export.soph(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])
        assert len(res) == 2

    def test_dcxml_1(self):
        res = export.dcxml(token, "2020ApJ...902L..36F")
        assert len(res) == 1

    def test_dcxml_2(self):
        res = export.dcxml(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])
        assert len(res) == 1  # Can't split output

    def test_refxml_1(self):
        res = export.refxml(token, "2020ApJ...902L..36F")
        assert len(res) == 1

    def test_refxml_2(self):
        res = export.refxml(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])
        assert len(res) == 1  # Can't split output

    def test_refabsxml_1(self):
        res = export.refabsxml(token, "2020ApJ...902L..36F")
        assert len(res) == 1

    def test_refabsxml_2(self):
        res = export.refabsxml(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])
        assert len(res) == 1  # Can't split output

    def test_rss_1(self):
        res = export.rss(token, "2020ApJ...902L..36F")
        assert len(res) == 1

    def test_rss_2(self):
        res = export.rss(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])
        assert len(res) == 1  # Can't split output

    def test_votable_1(self):
        res = export.votable(token, "2020ApJ...902L..36F")
        assert len(res) == 1

    def test_votable_2(self):
        res = export.votable(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])
        assert len(res) == 1  # Can't split output

    def test_ieee_1(self):
        res = export.ieee(token, "2020ApJ...902L..36F")
        assert len(res) == 1

    def test_ieee_2(self):
        res = export.ieee(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])
        assert len(res) == 2

    def test_csl_1(self):
        res = export.csl(token, "2020ApJ...902L..36F")
        assert len(res) == 1

    def test_csl_2(self):
        res = export.csl(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])
        assert len(res) == 2

    def test_custom(self):
        res = export.custom(
            token, "2020ApJ...902L..36F", format="%l (%Y), %j, %V, %p.\n"
        )

        assert res == [
            "Farmer, R., Renzo, M., de Mink, S. E., Fishbach, M., & Justham, S. (2020), \\apjl, 902, L36."
        ]


@pytest.mark.vcr()
class TestAPILib:
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
class TestAPIMetrics:
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

    def test_timseries(self):
        r = metrics.timeseries(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])

        assert r["skipped bibcodes"] == ["2020zndo...3678482F"]

    def test_indicators(self):
        r = metrics.indicators(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])

        assert r["skipped bibcodes"] == ["2020zndo...3678482F"]

    def test_timseries(self):
        r = metrics.timeseries(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])

        assert r["skipped bibcodes"] == ["2020zndo...3678482F"]

    def test_histogram(self):
        r = metrics.histograms(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])

        assert r["skipped bibcodes"] == ["2020zndo...3678482F"]

        assert "reads" in r["histograms"]

    def test_metrics(self):
        r = metrics.metrics(token, "2020ApJ...902L..36F")

        assert "reads" in r["histograms"]

    def test_detail(self):
        r = metrics.detail(token, ["2020ApJ...902L..36F", "2020zndo...3678482F"])

        assert r["skipped bibcodes"][0] == "2020zndo...3678482F"


@pytest.mark.vcr()
class TestAPIAuthor:
    def test_one(self):
        r = author.search(token, "2020ApJ...902L..36F")

        assert len(r) == 5

        assert "authorName" in r[0]

    def test_multi(self):
        r = author.search(token, ["2019ApJ...887...53F", "2020ApJ...902L..36F"])

        assert len(r) == 10

        assert "authorName" in r[0]


@pytest.mark.vcr()
class TestAPICitations:
    def test_one(self):
        with pytest.raises(TypeError):
            r = cites.citations(token, "2019ApJ...887...53F")

    def test_multi(self):
        r = cites.citations(token, ["2019ApJ...887...53F", "2020ApJ...902L..36F"])

        assert len(r) == 10

        assert "bibcode" in r[0]


@pytest.mark.vcr()
class TestAPISolr:
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


@pytest.mark.vcr()
class TestAPIRef:
    def test_one(self):
        r = ref.resolve(
            token, "Farmer, R., Fields, C. E., Petermann, I., et al. 2016, ApJS,227, 22"
        )

        assert r[0]["score"] == "1.0"

        assert r[0]["bibcode"] == "2016ApJS..227...22F"

    def test_fail(self):
        r = ref.resolve(token, "farmer,r et al 2020")

        assert r[0]["score"] == "0.0"


@pytest.mark.vcr()
class TestAPIResolve:
    def test_one(self):
        r = resolve.resolve(token, "2019ApJ...887...53F")

        assert "links" in r

        assert r["links"]["count"] == 17

    def test_multi(self):
        with pytest.raises(TypeError):
            r = resolve.resolve(token, ["2019ApJ...887...53F", "2020ApJ...902L..36F"])

    def test_esource(self):
        r = resolve.esource(token, "2020ApJ...902L..36F")

        assert "links" in r
        assert "count" in r["links"]
        assert r["links"]["count"] == 4

    def test_abstract(self):
        res = resolve.abstract(token, "2020ApJ...902L..36F")
        assert "link_type" in res

    def test_associated(self):
        with pytest.raises(e.AdsApiError):
            res = resolve.associated(token, "2020ApJ...902L..36F")

    def test_citations(self):
        res = resolve.citations(token, "2020ApJ...902L..36F")
        assert "link_type" in res

    def test_coreads(self):
        res = resolve.coreads(token, "2020ApJ...902L..36F")
        assert "link_type" in res

    def test_data(self):
        res = resolve.data(token, "2020ApJ...902L..36F")
        assert "link_type" in res

    def test_graphics(self):
        res = resolve.graphics(token, "2020ApJ...902L..36F")
        assert "link_type" in res

    def test_inspire(self):
        with pytest.raises(e.AdsApiError):
            res = resolve.inspire(token, "2020ApJ...902L..36F")

    def test_librarycatalog(self):
        with pytest.raises(e.AdsApiError):
            res = resolve.librarycatalog(token, "2020ApJ...902L..36F")

    def test_metrics(self):
        res = resolve.metrics(token, "2020ApJ...902L..36F")
        assert "link_type" in res

    def test_openurl(self):
        res = resolve.openurl(token, "2020ApJ...902L..36F")
        assert "link_type" in res

    def test_presentation(self):
        with pytest.raises(e.AdsApiError):
            res = resolve.presentation(token, "2020ApJ...902L..36F")

    def test_references(self):
        res = resolve.references(token, "2020ApJ...902L..36F")
        assert "link_type" in res

    def test_resolve(self):
        res = resolve.resolve(token, "2020ApJ...902L..36F")
        assert "action" in res

    def test_toc(self):
        with pytest.raises(e.AdsApiError):
            res = resolve.toc(token, "2020ApJ...902L..36F")


@pytest.mark.vcr()
class TestAPIVisual:
    def test_author(self):
        r = visual.author(token, ["2020ApJ...902L..36F", "2019ApJ...887...53F"])

        assert "data" in r
        assert len(r["data"]["fullGraph"]["nodes"]) == 6

    def test_paper(self):
        r = visual.paper(token, ["2020ApJ...902L..36F", "2019ApJ...887...53F"])

        assert "data" in r

        assert len(r["data"]["fullGraph"]["nodes"]) == 2

    def test_word_cloud(self):
        r = visual.word_cloud(token, query='author:"huchra, john"', rows=1)

        assert "available" in r
        assert "record_count" in r["available"]


@pytest.mark.vcr()
class TestAPIRecommend:
    @pytest.mark.skip(reason="Broken")
    def test_matchdoc(self):

        r = recommend.matchdoc(
            token,
            abstract="The nucleus of our nearest, large galactic neighbour, M31, contains an eccentric nuclear disc - a disc of stars on eccentric, apsidally aligned orbits around a supermassive black hole (SMBH). Previous studies of eccentric nuclear discs considered only an isolated disc, and did not study their dynamics under galaxy mergers (particularly a perturbing SMBH). Here, we present the first study of how eccentric discs are affected by a galactic merger. We perform N-body simulations to study the disc under a range of different possible SMBH initial conditions. A second SMBH in the disc always disrupts it, but more distant SMBHs can shut off differential precession and stabilize the disc. This results in a more aligned disc, nearly uniform eccentricity profile, and suppression of tidal disruption events compared to the isolated disc. We also discuss implications of our work for the presence of a secondary SMBH in M31.",
            title="Galactic merger implications for eccentric nuclear discs: a mechanism for disc alignment",
            year=2021,
            author="Rodriguez, Alexander; Generozov, Aleksey; Madigan, Ann-Marie",
            doctype="article",
        )

        assert r == [
            {
                "bibcode": "2021MNRAS.503.2713R",
                "confidence": 1,
                "scores": {"abstract": 1.0, "title": 1.0, "author": 1, "year": 1},
            }
        ]

        r = recommend.matchdoc(
            token,
            abstract="The nucleus of our nearest, large galactic neighbour, M31, contains an eccentric nuclear disc - a disc of stars on eccentric, apsidally aligned orbits around a supermassive black hole (SMBH). Previous studies of eccentric nuclear discs considered only an isolated disc, and did not study their dynamics under galaxy mergers (particularly a perturbing SMBH). Here, we present the first study of how eccentric discs are affected by a galactic merger. We perform N-body simulations to study the disc under a range of different possible SMBH initial conditions. A second SMBH in the disc always disrupts it, but more distant SMBHs can shut off differential precession and stabilize the disc. This results in a more aligned disc, nearly uniform eccentricity profile, and suppression of tidal disruption events compared to the isolated disc. We also discuss implications of our work for the presence of a secondary SMBH in M31.",
            title="Galactic merger implications for eccentric nuclear discs: a mechanism for disc alignment",
            year=2019,  # Wrong year
            author="Rodriguez, Alexander; Generozov, Aleksey; Madigan, Ann-Marie",
            doctype="article",
        )

        assert r == [
            {
                "bibcode": "2021MNRAS.503.2713R",
                "confidence": 1,
                "scores": {"abstract": 1.0, "title": 1.0, "author": 1, "year": 0.75},
            }
        ]

    # Somehow i never seem to trigger the logged in and active requirement for these to work
    def test_reviews(self):
        res = recommend.reviews(token, num_docs=10)

        assert len(res) == 0

    def test_similar(self):
        res = recommend.similar(token, num_docs=10)

        assert len(res) == 0

    def test_trending(self):
        res = recommend.trending(token, num_docs=10)

        assert len(res) == 0

    def test_useful(self):
        res = recommend.useful(token, num_docs=10)

        assert len(res) == 0


@pytest.mark.vcr()
class TestAPIClassic:
    def test_mirrors(self):
        res = classic.mirrors(token)

        assert "adsabs.harvard.edu" in res

    def test_user(self):
        with pytest.raises(e.AdsApiError):
            res = classic.user(token)


class TestAPIToken:
    def test_token(self):
        t2 = "AAAA"

        tp = tempfile.mktemp(dir="./")
        t.save_token(t2, tp)
        t3 = t.get_token(tp)
        os.remove(tp)

        assert t3 == t2

    def test_orcid(self):
        t2 = "AAAA"

        tp = tempfile.mktemp(dir="./")
        t.save_orcid(t2, tp)
        t3 = t.get_orcid(tp)
        os.remove(tp)

        assert t3 == t2


@pytest.mark.vcr()
class TestAPIStored:
    def test_all(self):
        # Run as one large test as we need to do several steps in one go

        res = stored.save(token, query="^farmer year:2020", fields="bibcode,title")

        assert "qid" in res

        qid = res["qid"]

        res = stored.query(token, qid)

        assert "query" in res
        assert "numfound" in res

        res = stored.query2svg(token, qid)
        assert "<svg xmlns" in res

        res = stored.search(token, qid)

        assert "numFound" in res
        assert "docs" in res


@pytest.mark.vcr()
class TestAPINotifications:
    def test_template(self):
        res = notif.create_template(token, name="test")

        assert "id" in res

        id = res["id"]

        res = notif.view_all(token)

        assert len(res) > 0
        assert "id" in res[0]

        res = notif.view(token, id)

        assert len(res) > 0
        assert "id" in res[0]
        assert res[0]["id"] == id

        res = notif.delete(token, id)
