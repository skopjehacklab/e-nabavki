#! /usr/bin/env python2
#  -*- encoding: utf-8 -*-
"""Fetch dosies and upload the full html in couchdb.

Multiprocessing is done through external xargs. Sample usage for multiprocessing should be:

./fetch_dosies.py --print-state pending | xargs -n1 -P 10 ./fetch_dosies.py --dosie
"""

import couchdbkit, restkit
import ConfigParser
import requests
import argparse

from index_links import connect_to_couchdb

def fetch_dosie(id,couch):
    doc = couch.get(id)
    r = requests.get(doc['link'])
    if r.status_code == 200:
        doc['state'] = 'downloaded'
        couch.save_doc(doc)
        couch.put_attachment(doc,r.text,"dosie.html",r.headers['content-type'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--print-state", choices=["pending","downloaded","parsed"],
                        help="Print all dosie ids")
    group.add_argument("--dosie", metavar="DOSIEID",
                        help="Fetch one dosie from link")
    group.add_argument("--stats",action="store_true",
                        help="Prints stats from the db on pending, downloaded and parsed dosies")

    args = parser.parse_args()

    couch = connect_to_couchdb()

    if args.print_state:
        for view_result in couch.view('dosie/by_state', key=args.print_state):
            print couch.get(view_result['id'])['_id'],

    if args.dosie:
        fetch_dosie(args.dosie,couch)

    if args.stats:
        downloaded = couch.view('dosie/by_state',key='downloaded').count()
        pending = couch.view('dosie/by_state',key='pending').count()
        parsed = couch.view('dosie/by_state',key='parsed').count()

        print "Downloaded %d, pending %d, Fully parsed %d" % (downloaded, pending, parsed)
