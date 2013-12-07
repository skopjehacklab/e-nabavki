#! /usr/bin/env python2
#  -*- encoding: utf-8 -*-
"""Insert dosie links into couchdb.

If invoked as script with the --initial=pages_path argument it will 
parse all the json files in pages_path and insert them as pending 
in couchdb. Pages_path should be populated with all the pages from the
e-nabavki site with initial_get_all_links.sh

If invoked without arguments it will try to fetch the dosie links directly
from e-nabavki with casperjs and exit at the first error (used for regular
indexing through cron).


Example usage:
 ./index_links --initial=./pages
"""

import couchdbkit, restkit
import json
import itertools, subprocess
import urlparse
import ConfigParser
import os, sys, argparse

def connect_to_couchdb():
    cfg = ConfigParser.ConfigParser()
    cfg.read(['settings.ini'])

    db_url = cfg.get('database', 'url')
    user = cfg.get('database', 'username')
    passwd = cfg.get('database', 'password')

    return couchdbkit.Database(db_url, filters=[restkit.BasicAuth(user, passwd)])

def insert_pending_dosie(link,couch):
    """
        Try to insert dosie in couchdb. If the insert fails 
    we probably already have that dosie.
    """

    Id = urlparse.parse_qs(urlparse.urlparse(link).query)['Id'][0]
    doc = { '_id': Id, 'state': 'pending', 'link': link}
    try:
        couch.save_doc(doc)
    except:
        print "failed insert in couchdb at id: %s" % Id
        raise

def run_casper_and_insert_pending_dosie(couch,page=1):
    """
        Run casper to fetch directly to the e-nabavki site
    and insert dosies as pending in couchdb.
    """

    CMD = """casperjs e-nabavki.gov.mk.js --page=%d"""
    cmd = (CMD % page).split()

    casper = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = json.load(casper.stdout)

    for link in output['links']:
        insert_pending_dosie(link,couch)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--initial", metavar="PAGESPATH", 
                        help="Initial run with path to pages/*.json files to parse")
    args = parser.parse_args()

    couch = connect_to_couchdb()

    if not args.initial:
        #regular run
        for page in itertools.count(1):
            run_casper_and_insert_pending_dosie(couch,page)
    else:
        #initial run
        for dirpath, dirnames, filenames in os.walk(pages_path):
            for filename in filenames:
                if filename.endswith(".json"):
                    full_filename_path = "%s%s" % (pages_path, filename)
                    try:
                        output = json.load(open(full_filename_path))
                    except:
                        print "failed to load json at %s" % full_filename_path
                        continue
                    
                    for link in output['links']:
                        insert_pending_dosie(link,couch)
