# # SPDX-License-Identifier: BSD-3-Clause

# import bibtexparser
# from bibtexparser.bparser import BibTexParser
# import requests

# from .articles import journal,_fields
# from .api import http as utils
# from .api import urls


# class search(object):
#     def __init__(self, adsdata):
#         self.adsdata = adsdata

#     def search(self, query):
#         if not len(query):
#             return []

#         # Parse search function
#         q = parseSearch(query)

#         bibs, data = self._query(q.query())
#         return journal(self.adsdata, bibs, data=data)

#     def _query(self, query, max_rows=250):

#         start = 0
#         results = []
#         while True:
#             r = self._query_ads(query, start)

#             # Did we get everything?
#             data = r.json()

#             if "response" not in data:
#                 raise SearchError()

#             results.extend(data["response"]["docs"])
#             num_found = int(data["response"]["numFound"])
#             num_got = len(results)

#             if num_got >= num_found:
#                 break

#             if num_got > max_rows:
#                 break

#             start = num_got

#         bibcodes = [i["bibcode"] for i in results]

#         return bibcodes, results

#     def _query_ads(self, query, start=0):
#         r = requests.get(
#             urls.urls["search"],
#             auth=utils._BearerAuth(self.adsdata.token),
#             params={"q": query, "fl": _fields, "rows": 100, "start": start},
#         )
#         # Get rate limits
#         try:
#             _limit = int(r.headers["X-RateLimit-Remaining"])
#             _max_limit = int(r.headers["X-RateLimit-Limit"])
#         except KeyError:
#             pass

#         return r

#     def bibcode_single(self, bibcode):
#         return self.search('bibcode:"' + str(bibcode) + '"')

#     def bibcode_multi(self, bibcodes):
#         return self.chunked_search(bibcodes, "bibcode:")

#     def arxiv_multi(self, arxivids):
#         return self.chunked_search(arxivids, "identifier:")

#     def orcid(self, orcid):
#         return self.search('orcid:"' + str(orcid) + '"')

#     def first_author(self, author):
#         return self.search('author:"^' + author + '"')

#     def chunked_search(self, ids, prefix):
#         # Break up data into chunks to process otherwise we max at 50 entries:
#         query = self.chunked_join(ids, prefix=prefix, joiner=" OR ")
#         alldata = []
#         allbibs = []
#         for i in query:
#             bibs, data = self._query(i)
#             alldata.extend(data)
#             allbibs.extend(bibs)

#         return journal(self.adsdata, bibcodes=allbibs, data=alldata)

#     def chunked_join(self, data, prefix="", joiner="", nmax=20):
#         """
#         Breaks data into chunks of maximum size nmax

#         Each element of the chunked data is prefixed with prefix and joined back together with joiner

#         data = ['1','2','3','4']
#         _chunked_join(data,prefix='bibcode:','joiner=' OR ',nmax=2)

#         ['bibcode:1 OR bibcode:2','bibcode:3 OR bibcode:4']

#         Handy to break up large queries that might exceed search limits (seems to be a max of 50
#         bibcodes or arxiv ids at a time).
#         Where prefix is the ads term ('bibcode:' or 'indentifier:')
#         and joiner is logical or ' OR '

#         """
#         res = []

#         for pos in range(0, len(data), nmax):
#             x = [prefix + j for j in data[pos : pos + nmax]]
#             res.append(joiner.join(x))

#         return res


# class SearchError(Exception):
#     pass


# class parseSearch(object):
#     def __init__(self, query):
#         self._query = query

#     def query(self):
#         for search in dir(self):
#             if search.startswith("search_"):
#                 q = getattr(self, search)()
#                 # print('called',q,search)
#                 if q:
#                     break

#         if not q:
#             q = self._query

#         return q

#     def make_query(self, identifer):
#         q = ""
#         if "bibcode" in identifer:
#             q = "bibcode:" + identifer["bibcode"]
#         elif "arxiv" in identifer:
#             q = "arxiv:" + identifer["arxiv"]
#         elif "doi" in identifer:
#             q = "doi:" + identifer["doi"]

#         return q

#     def search_url(self):
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

#     def search_bibtex(self):
#         res = {}
#         if self._query.startswith("@"):
#             bp = bibtexparser.BibTexParser(interpolate_strings=False)
#             bib = bibtexparser.loads(self._query, filter=bp)
#             bib = bib.entries[0]
#             # What is in the bib?
#             if "adsurl" in bib:
#                 res["bibcode"] = bib["adsurl"].split("/")[-1]
#             elif "eprint" in bib:
#                 res["arxiv"] = bib["eprint"]
#             elif "doi" in bib:
#                 res["doi"] = bib["doi"]
#             else:
#                 raise ValueError("Don't understand this bitex")

#         if len(res):
#             return self.make_query(res)
#         else:
#             return False

#     def search_citation(self):
#         if "et al" in self._query:
#             author, year = self._query.split("et al.")
#             return 'author:"^{}" year:{}'.format(author, year)
#         if "&" in self._query:
#             a1, a2 = self._query.split("&")
#             a2, year = a2.split()
#             return 'author:"^{}" author:"{}" year:{}'.format(a1, a2, year)
#         return False


import pyastroapi.api.search as _search
import pyastroapi.api.token as _token


def first_author(author):
    return _search.search(_token.get_token(), query=f"^{author}")


def author_year(author, year):
    return _search.search(_token.get_token(), query=f"^{author} year:{year}")


def search(query, fields=None):
    return _search.search(_token.get_token(), query=query, fields=fields)
