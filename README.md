![Test suite status](https://github.com/rjfarmer/pyAstroApi/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/rjfarmer/pyAstroApi/branch/main/graph/badge.svg?token=4VQNTPZYMZ)](https://codecov.io/gh/rjfarmer/pyAstroApi)
[![Documentation Status](https://readthedocs.org/projects/pyastroapi/badge/?version=latest)](https://pyastroapi.readthedocs.io/en/latest/?badge=latest)

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

````
~/.ads/dev_key
````

### Basic searching

To quickly just search and get a set of papers back from ADS:

````python
import pyastroapi.articles

a = articles.journal(search="^farmer year:2020")
````

The `search` field can be any standard ADS query. The object `a` is now a `journal` which is a dict-like object of `article`.
A `journal` can be accessed either by bibcode key:

````python
paper = a["2020ApJ...902L..36F"]
````

or iterated over like a list (or accessed with an index, e.g., `a[0]`)

````python
for paper in a:
    print(a.title)
````

The object `paper` is an `article` which encapsulates accessing ADS. The initial search will fetch a set of standard fields,
however non-standard fields will require additional fetch's to ADS servers.

Fields can be accessed as properties:

````python
paper.title
paper.author
paper.abstract
````

Some properites are function calls:

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



## Acknowledgements

This project is not affiliated with NASA or ADSABS.

This research has made use of NASA’s Astrophysics Data System Bibliographic Services.

