# SPDX-License-Identifier: BSD-3-Clause

import os
import re
import requests
import datetime
from pathlib import Path

import bibtexparser
from bibtexparser.bparser import BibTexParser

from . import utils


# Default ADS search fields
_fields = ['bibcode','title','author','year','abstract',
            'pubdate','bibstem','alternate_bibcode','citation_count','identifier',
            'reference'
            ]

search_words = '''abs abstract ack aff aff_id alternate_bibcode alternative_title arXiv arxiv_class author author_count
                 bibcode bigroup bibstem body 
                 citation_count copyright 
                 data database pubdate doctype doi
                 full
                 grant
                 identifier inst issue 
                 keyword
                 lang
                 object orcid orcid_user orcid_other
                 page property
                 read_count
                 title
                 vizier volume
                 year
                '''.split()



class journal(object):
    '''
    This is a collection of articles that supports iterating over.

    We defer as much as possible actualy accessing data untill its needed
    '''
    def __init__(self, adsdata, bibcodes, data=None):
        self.adsdata = adsdata
        self._set_bibcodes = set(bibcodes)   
        self._bibcodes = bibcodes    
        self._data = {}

        if data is not None:
            for i in data:
                self._data[i['bibcode']] = article(self.adsdata, i['bibcode'], data=i)

    def __len__(self):
        return len(self._set_bibcodes)

    def __contains__(self, key):
        return key in self._set_bibcodes

    def __getitem__(self, key):
        if key in self._set_bibcodes:
            if key not in self._data:
                self._data[key] = article(self.adsdata,bibcode=key)
            return self._data[key]
        else:
            return self.__getitem__(self._bibcodes[key])

    def __iter__(self):
        for i in self._bibcodes:
            yield self.__getitem__(i)

    def keys(self):
        return self._set_bibcodes

    def bibcodes(self):
        return self.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()


class article(object):
    '''
    A single article that is given by either a bibcode, arxic id, or doi.
    Bibcodes are allways the prefered ID as the doi or arxiv id we query  ADS for its bibcode.

    We defer actually searching the ads untill the user asks for a field.
    Thus we can make as many article as we want (if we allready know the bibcode)
    without hitting the ADS api limits.
    '''

    def __init__(self, adsdata, bibcode=None, data=None):
        self.adsdata = adsdata
        self._bibcode = bibcode
        self._data = None
        self._citations=None
        self._references=None
        self.which_file=None

        if data is not None:
            self._data = data
            self._bibcode = self._data['bibcode']
    
    def search(self,force=False):
        if self._data is None or force:
            self._data = self.adsdata.search.bibcode_single(self.bibcode)
            
    @property
    def bibcode(self):
        return self._bibcode

    def __gettattr__(self, key):
        if self._data is None:
            self.search()

        if self._data is not None:
            if key in self._data:
                return self._data[key]

    def __getitem__(self, key):
        if self._data is None:
            self.search()
    
        if self._data is not None:
            if key in self._data:
                return self._data[key]

    @property
    def title(self):
        if self._data is None:
            self.search()
        return self._data['title'][0]

    @property
    def authors(self):
        if self._data is None:
            self.search()
        return  '; '.join(self._data['author'])

    @property
    def author(self):
        return self.authors

    @property
    def first_author(self):
        if self._data is None:
            self.search()
        return self._data['author'][0]

    @property
    def journal(self):
        if self._data is None:
            self.search()
        return self._data['bibstem'][0]

    def filename(self, full=False):
        if full:
            return os.path.join(utils.read_key_file(utils.settings['PDFFOLDER_FILE']),
                                self.bibcode+'.pdf')
        else:
            return self.bibcode+'.pdf'

    @property
    def year(self):
        if self._data is None:
            self.search()
        return self._data['year']

    @property
    def abstract(self):
        if self._data is None:
            self.search()
        if 'abstract' in self._data:
            return self._data['abstract']
        else:
            return ''

    @property
    def name(self):
        if self._data is None:
            self.search()
        return self.first_author + ' ' + self.year

    @property
    def ads_url(self):
        if self._data is None:
            self.search()
        return 'https://ui.adsabs.harvard.edu/abs/'+self.bibcode

    @property
    def arxiv_url(self):
        if self._data is None:
            self.search()
        arxiv_id = None
        for i in self._data['identifier']:
            if i.startswith('arXiv:'):
                arxiv_id = i.replace('arXiv:','')

        if arxiv_id is not None:
            return 'https://arxiv.org/abs/'+arxiv_id
        else:
            return ''

    @property
    def journal_url(self):
        if self._data is None:
            self.search()
        doi = None
        for i in self._data['identifier']:
            if i.startswith('10.'):
                doi = i
        if doi is not None:
            return  'https://doi.org/'+doi
        else:
            return ''

    @property
    def citation_count(self):
        if self._data is None:
            self.search()
        if 'citation_count' not in self._data:
            return 0
        else:
            return self._data['citation_count']

    @property
    def reference_count(self):
        if self._data is None:
            self.search()
        if 'reference' not in self._data:
            return 0
        else:
            return len(self._data['reference'])
    
    def pdf(self, filename):
        # There are multiple possible locations for the pdf
        # Try to avoid the journal links as that usally needs a 
        # vpn working to use a university ip address
        strs = ['/PUB_PDF','/EPRINT_PDF','/ADS_PDF']

        if os.path.exists(filename):
            return

        got_file=False
        for i in strs:
            url = utils.urls['pdfs']+str(self.bibcode)+i

            # Pretend to be Firefox otherwise we hit captchas
            headers = {'user-agent': 'Mozilla /5.0 (Windows NT 10.0; Win64; x64)'}
            try:
                r = requests.get(url, allow_redirects=True,headers=headers)
            except requests.exceptions.RequestException:
                continue

            if r.content.startswith(b'<!DOCTYPE html'): 
                continue

            with open(filename,'wb') as f:
                f.write(r.content)
                self.which_file = i
                got_file=True
                break

        if not os.path.exists(filename):
            raise utils.FileDonwnloadFailed("Couldn't download file")

    def citations(self):
        if self._citations is None:
            self._citations = self.adsdata.search('citations(bibcode:"'+self._bibcode+'")')
        return self._citations

    def references(self):
        if self._references is None:
            self._references = self.adsdata.search('references(bibcode:"'+self._bibcode+'")')
        return self._references 

    def bibtex(self):
        data = {'bibcode':[self.bibcode]}
        r = requests.post(utils.urls['bibtex'],
                auth=utils.BearerAuth(self.adsdata.token),
                headers={'Content-Type':'application/json'},
                json = data).json()

        if 'error' in r:
            raise ValueError(r['error'])

        return r['export']

    def __str__(self):
        return self.name

    def __reduce__(self):
        return (article, (self.adsdata,self.bibcode))

    def __hash__(self):
        return hash(self.bibcode)

    def __eq__(self, value):
        if isinstance(value, article):
            if value.bibcode == self.bibcode:
                return True
        return False
