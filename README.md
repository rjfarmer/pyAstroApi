![Test suite status](https://github.com/rjfarmer/pyAstroApi/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/rjfarmer/pyAstroApi/branch/main/graph/badge.svg?token=4VQNTPZYMZ)](https://codecov.io/gh/rjfarmer/pyAstroApi)
[![Documentation Status](https://readthedocs.org/projects/pyastroapi/badge/?version=latest)](https://pyastroapi.readthedocs.io/en/latest/?badge=latest)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/rjfarmer/pyAstroApi.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/rjfarmer/pyAstroApi/context:python)

# pyAstroApi


Low level library interfacing with NASA's ADSABS api.

## Installation


### PyPi

pip install pyAstroApi


### From source

Install dependencies:

````bash
pip install -r requirements.txt
````

Build and install software

````bash
pip install .
````


### Testing locally

Install dependencies:

````bash
pip install -r requirements_dev.txt
````

and then to run with one python version

````bash
pytest
````

or use tox to test multiple versions of python

````bash
tox
````

## Getting started

Full documentation can be found at [readthedocs](https://pyastroapi.readthedocs.io/en/latest/).

Here is a quick start guide for the very basics.

### ADS Key

First you will need your own ADS api key: https://ui.adsabs.harvard.edu/user/settings/token

This can be saved to the file:

````bash
~/.ads/dev_key
````

### Basic searching

To quickly just search and get a set of papers back from ADS:

````python
import pyastroapi.articles

a = articles.journal(search="^farmer year:2020")
````

The `search` field can be any standard ADS query. The object `a` is now a `journal` which is a dict-like object of `article`'s.

You can also constrcut a `journal` from a list of bibcodes:

````python
a = articles.journal(bibcodes=["2020ApJ...902L..36F","2021ApJ...923..214F"])
````

A `journal` can be accessed either by specifying the bibcode:

````python
paper = a["2020ApJ...902L..36F"]
````

or iterated over like a list (or accessed with an index, e.g., `a[0]`)

````python
for paper in a:
    print(a.title)
````

The object `paper` is an `article` which encapsulates all the methods needed to access the information ADS has on a paper. The initial search (Either via access through a `journal` or by creating an article with: `articles.article("2020ApJ...902L..36F")`) will fetch a set of standard fields from ADS.
Non-standard fields will require additional fetch's to ADS servers, but this is wrapped so all you need to do is try to access the field and the data will be fetched for you.

Most fields can be accessed as properties:

````python
paper.title
paper.author
paper.abstract
````

Though some fields are function calls:

````python
paper.citations()
paper.references()
````

### Extra information

An `article` also contains wrappers into some of the other ADS features:

````python
paper.url.journal()
````

Get the publisher HTML url

````python
paper.pdf.arxiv()
````

Download the Arxiv pdf to a file given by the papers bibcode (e.g., 2020ApJ...902L..36F.pdf)

````python
paper.export.bibtex()
````

Get the papers BibTex 


````python
paper.metrics.histograms()
````

Return a histogram of the metric data for the paper

````python
paper.visual.author()
````

Return the author network visualization for the paper.

## API

Functions and classes inside the pyastroapi namespace are provided to provide convenient wrappers around the output of ADSABS API. 
Though at this time not ever endpoint has a wrapper.

However, the pyastroapi.api namespace provides a low-level API that handles setting all the arguments necessary for each of the API end points.

List of the [ADSABS API's](https://ui.adsabs.harvard.edu/help/api/api-docs.html#overview) are currently implemented inside the pyastroapi.api namespace

- [X] Search (Including big queries)
- [X] Stored Search
- [X] Libraries (apart from editing an existing library)
- [X] Export 
- [X] Metrics
- [X] Author Affiliation
- [X] Citation Helper
- [X] Classic import (Caveat: I don't have a classic account to test with)
- [X] Objects
- [X] Recommender (Except matchdoc)
- [X] Reference
- [X] Notifications
- [X] Visualizations


## Contributing

Contributions are welcome either as pull requests or as bug reports. If reporting a bug please include the exact code you used and 
if applicable the bibcodes for any paper you where trying to access.

## Acknowledgements

This project is not affiliated with NASA or ADSABS.

This research has made use of NASA’s Astrophysics Data System Bibliographic Services.

