#!/usr/bin/env python2
#  -*- encoding: utf-8 -*-
"""Parses all the downloaded documents.

It extracts all the import selectors from the dosie.html attachment.
"""

import argparse
import json
from ConfigParser import ConfigParser
from lxml import html
from index_links import connect_to_couchdb

def get_selectors():
    cfg = ConfigParser()
    cfg.optionxform = str
    cfg.read(['settings.ini'])

    return cfg.items('selectors')

def parse(doc):
    """Get the attachment from the document and extract the selectors.
    Returns the doc dictionary"""

    original_html = couch.fetch_attachment(doc,"dosie.html")
    page = html.fromstring(original_html)

    results = {}
    selectors = get_selectors()
    
    for selector in selectors:
        value_id = selector[0]
        name = selector[1]
        
        val = page.get_element_by_id(value_id, None)
        if val is not None:
            results[name] = val.text.encode('utf-8')
    
    doc['state'] = 'parsed'
    
    return dict(doc.items() + results.items())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true",
                        help="Parse all documents even if already parsed")

    args = parser.parse_args()

    couch = connect_to_couchdb()

    for view_result in couch.view('dosie/by_state', key="downloaded"):
        doc = couch.get(view_result['id'])
        print doc['_id']
        couch.save_doc(parse(doc))
    
    if args.all:
        for view_result in couch.view('dosue/by_state', key="done"):
            doc = couch.get(view_result['id'])
            couch.save_doc(parse(doc))


