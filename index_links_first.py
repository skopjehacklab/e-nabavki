#! /usr/bin/env python2
#  -*- encoding: utf-8 -*-

import couchdbkit, restkit
import subprocess
import json
import urlparse
import itertools
import ConfigParser
import os

cfg = ConfigParser.ConfigParser()
cfg.read(['settings.ini'])

db_url = cfg.get('database', 'url')
user = cfg.get('database', 'username')
passwd = cfg.get('database', 'password')


couch = couchdbkit.Database(db_url, filters=[restkit.BasicAuth(user, passwd)])

def run_casper_and_get_page(page=1):
    print "putting page %d" % page
    pagefile = "pages/%d.json" % page
    output = json.load(open(pagefile))
    for link in output['links']:
        Id = urlparse.parse_qs(urlparse.urlparse(link).query)['Id'][0]
        doc = { '_id': Id, 'state': 'pending', 'link': link}
        try:
            couch.save_doc(doc)
        except:
            print "failed at id: %s" % Id	
            #raise

for page in itertools.count(1):
    run_casper_and_get_page(page)
