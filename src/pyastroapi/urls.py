# # SPDX-License-Identifier: BSD-3-Clause

import urllib.parse as parse
import typing as t

__all__ = ["parse_url"]

_headers = {"user-agent": "Mozilla /5.0 (Windows NT 10.0; Win64; x64)"}


def parse_url(url: str) -> t.Dict[str, str]:
    """Attempt to determine what article is referenced by url

    Currently handles:
        ADS, Arxiv, IOP journals

    Args:
        url (_type_): URL to article

    Raises:
        ValueError: Raised if URL can't be matched

    Returns:
        t.Dict[str,str]: Dict containing either and identifier or other identifying information
                         that can be feed into a search() query
    """

    purl = parse.urlparse(url)

    if purl.netloc == "ui.adsabs.harvard.edu":
        r = _parse_ads(purl)
    elif purl.netloc == "arxiv.org":
        r = _parse_arxiv(purl)
    elif purl.netloc == "iopscience.iop.org":
        r = _parse_iop(purl)
    elif purl.netloc == "academic.oup.com":
        r = _parse_mnras(purl)
    elif purl.netloc == "www.aanda.org":
        r = _parse_aa(purl)
    else:
        raise ValueError(f"Can't match {url}")

    return r


def _parse_ads(purl):
    for i in purl.path.split("/"):
        if len(i) == 19:
            return {"identifier": i}


def _parse_arxiv(purl):
    for i in purl.path.split("/"):
        try:
            x = float(i.split("v")[0])
            return {"identifier": str(x)}
        except ValueError:
            pass


def _parse_iop(purl):
    doi = purl.path.partition("article/")[-1].replace("/meta", "")
    return {"identifier": doi}


def _parse_mnras(purl):
    raise NotImplementedError


def _parse_aa(purl):
    raise NotImplementedError


#         """
#         Given an URL attempts to work out the bibcode, arxiv id, or doi for it
#         """
#         url = self._query

#         res = {}
#         headers = {"user-agent": "Mozilla /5.0 (Windows NT 10.0; Win64; x64)"}

#         if "adsabs.harvard.edu" in url:  # ADSABS
#             q = url.split("/")
#             if len(q[-1]) == 19:
#                 res["bibcode"] = q[-1]
#             elif len(q[-2]) == 19:
#                 res["bibcode"] = q[-2]
#             else:
#                 res["bibcode"] = None
#         elif "arxiv.org/" in url:  # ARXIV
#             res["arxiv"] = url.split("/")[-1].split("v")[0]
#         elif "iopscience.iop.org" in url:  # ApJ, ApJS
#             # http://iopscience.iop.org/article/10.3847/1538-4365/227/2/22/meta
#             res["doi"] = url.partition("article/")[-1].replace("/meta", "")
#         elif "academic.oup.com/mnras" in url:  # MNRAS
#             # https://academic.oup.com/mnras/article/433/2/1133/1747991
#             r = requests.get(url, headers=headers)
#             for i in r.text.split():
#                 if "doi.org" in i and ">" in i:
#                     break  # Many matches but we want the line which has a href=url>
#             res["doi"] = i.split(">")[1].split("<")[0].split("doi.org/")[1]
#         elif "aanda.org" in url:  # A&A:
#             # https://www.aanda.org/articles/aa/abs/2017/07/aa30698-17/aa30698-17.html
#             # Resort to downloading webpage as the url is useless
#             r = requests.get(url, headers=headers)
#             for line in r.text.split(">"):
#                 if "citation_bibcode" in line:
#                     # bibcodes are 19 characters, but the & in A&A gets converted to %26
#                     res["bibcode"] = line.split("=")[-1].replace("%26", "&")
#                     break
#         elif "nature.com" in url:  # nature
#             # https://www.nature.com/articles/s41550-018-0442-z #plus junk after this
#             if "?" in url:
#                 url = url[: url.index("?")]
#             r = requests.get(url + ".ris", headers=headers)
#             for i in r.text.split():
#                 if "doi.org" in i:
#                     res["doi"] = "/".join(i.split("/")[-2:])
#                     break
#         elif "sciencemag.org" in url:  # science
#             # http://science.sciencemag.org/content/305/5690/1582
#             r = requests.get(url, headers=headers)
#             for line in r.text.split(">"):
#                 if 'meta name="citation_doi"' in line:
#                     res["doi"] = (
#                         line.split("=")[-1].replace('"', "").removesuffix("/").strip()
#                     )
#         elif "PhysRevLett" in url:  # Phys Review Letter
#             # https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.116.241103
#             doi = "/".join(url.split("/")[-2:])
#             res["doi"] = doi

#         if len(res):
#             return self.make_query(res)
#         else:
#             return False
