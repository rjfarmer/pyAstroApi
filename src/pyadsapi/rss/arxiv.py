import feedparser
from html.parser import HTMLParser


class _getNames(HTMLParser):
    def handle_data(self, data):
        if "names" not in self.__dict__:
            self.names = []

        if "," not in data and data not in self.names:
            self.names.append(data.strip())


class _getAbstract(HTMLParser):
    def handle_data(self, data):
        self.abs = data.replace("\n", " ")


def get_feed(cat):
    entries = feedparser.parse("http://arxiv.org/rss/" + cat)
    data = []

    for entry in entries.entries:
        parserN = _getNames()
        parserN.feed(entry["authors"][0]["name"])

        parserA = _getAbstract()
        parserA.feed(entry["summary"])

        data.append(
            {
                "title": entry["title"],
                "abstract": parserA.abs,
                "arixv_id": entry["id"].split("/")[-1],
                "authors": parserN.names,
                "pubdate": entries["headers"]["date"],
            }
        )

    return data


def astro_ph():
    return get_feed("astro-ph")
