# SPDX-License-Identifier: BSD-3-Clause

import typing as t

# https://ui.adsabs.harvard.edu/help/api/api-docs.html

base_url = "https://api.adsabs.harvard.edu/v1"

urls = {
    "search": {
        "search": "/search/query",
        "bigquery": "/search/bigquery",
    },
    # Stored search
    "stored": {
        "search": "/vault/query",
        "query2svg": "/vault/query2svg",
        "execute_query": "/vault/execute_query",
    },
    # Libraries
    "libraries": {
        "change": "/biblib/documents",  # Add, remove, delete, update
        "view": "/biblib/libraries",  # New, view
        "permission": "/biblib/permissions",
        "operate": "/biblib/libraries/operations/",
        "transfer": "/biblib/transfer",
    },
    # Export
    "export": {
        "ads": "/export/ads",
        "bibtextads": "/export/bibtexabs",
        "bibtex": "/export/bibtex",
        "endnote": "/export/endnote",
        "medlars": "/export/medlars",
        "procite": "/export/procite",
        "refworks": "/export/refworks",
        "ris": "/export/ris",
        "aastex": "/export/aastex",
        "icarus": "/export/icarus",
        "mnras": "/export/mnras",
        "soph": "/export/soph",
        "dcxml": "/export/dcxml",
        "refxml": "/export/refxml",
        "refabsxml": "/export/refabsxml",
        "rss": "/export/rss",
        "votable": "/export/votable",
        "csl": "/export/csl",
        "custom": "/export/custom",
        "ieee": "/export/ieee",
    },
    # Metrics
    "metrics": {
        "detail": "/metrics/detail",
        "metrics": "/metrics",
    },
    # Author
    "authors": {
        "search": "/author-affiliation/search",
        "export": "/author-affiliation/export",
    },
    # Citations
    "citations": {
        "helper": "/citation_helper",
    },
    # Classic
    "classic": {
        "mirrors": "/harbour/mirrors",
        "user": "/harbour/user",
        "auth": "/harbour/auth/classic",
    },
    # Objects
    "objects": {
        "solr": "/objects/query",
        "objects": "/objects",
    },
    # Oracle
    "oracle": {
        "match": "/oracle/matchdoc",
        "read": "/oracle/readhist",
    },
    # Reference
    "ref": {"text": "/reference/text", "xml": "/reference/xml"},
    # Resolver
    "resolve": {
        "search": "/resolver",
    },
    # Notifications
    "notification": {
        "edit": "/vault/notifications",
        "get": "/vault/notification_query",
    },
    # Visualtions
    "visual": {
        "author": "/vis/author-network",
        "paper": "/vis/paper-network",
        "word-cloud": "/vis/word-cloud",
    },
}


def make_url(endpoint: str, *args: str) -> str:
    u = [base_url, endpoint]
    u.extend(args)

    return "/".join(u)
