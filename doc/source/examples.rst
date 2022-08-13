Examples
========


Search
~~~~~~

Searching for papers ::

    import pyastroapi.articles as articles
    journal = articles.journal(search="^farmer year:2020")


Accessing a paper, if you know the bibcode already ::

    import pyastroapi.articles
    article = articles.article("2020ApJ...902L..36F")

Or if you have a `journal` already ::

    article = journal["2020ApJ...902L..36F"]


Once you have an `article` you can access the various fields returned by ADS ::

    article.title
    article.authors
    article.abstract


Or to get the reference list ::

    article.references()

or the citation list ::

    article.citations()

Both of these return a `journal`    


Download a PDF
~~~~~~~~~~~~~~

PDF's get be downloaded via an `article` ::

    article.pdf.arxiv()
    article.pdf.journal()
    article.pdf.ads()


Download a Bibtex
~~~~~~~~~~~~~~~~~

Bibtex's are also accessed via an `article` ::

    article.export.bibtex()

Other export formats are available ::

    dir(article.export)


Libraries
~~~~~~~~~

A list of all available libraries can be had with ::

    import pyastroapi.libraries as libraries

    libs - libraries.libraries()

`lib` is now a dict list object that supports both accessing via `keys()` to access via library name or via iteration (list style).

New libraries can be created with ::

    libs.new(name='my library')

Libraries can be deleted via ::

    libs.pop(name='my library')

This will remove the library from ADS. There is no recovery possible.

A single library can be accessed from `libs` ::

    lib = libs["my library"]

Papers can be added to `lib` with ::

    lib.add_bibcode("bibcode")

and removed with ::

    lib.pop("bibcode")

A list of papers in the library can be accessed with ::

    lib.keys()


