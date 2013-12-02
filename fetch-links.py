#! /usr/bin/env python2
#  -*- encoding: utf-8 -*-

import couchdbkit, restkit
import subprocess
import json
import urlparse
import itertools
import ConfigParser

cfg = ConfigParser.ConfigParser()
cfg.read(['settings.ini'])

db_url = cfg.get('database', 'url')
user = cfg.get('database', 'username')
passwd = cfg.get('database', 'password')


couch = couchdbkit.Database(db_url, filters=[restkit.BasicAuth(user, passwd)])

CMD = """casperjs e-nabavki.gov.mk.js --page=%d"""


def run_casper_and_get_page(page=1):
    cmd = (CMD % page).split()
    print "getting page %d" % page
    print cmd
    casper = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = json.load(casper.stdout)

    for link in output['links']:
        Id = urlparse.parse_qs(urlparse.urlparse(link).query)['Id'][0]
        doc = { '_id': Id, 'state': 'pending', 'link': link}
        try:
            couch.save_doc(doc)
        except:
            print "failed at id: %s" % Id
            raise

for page in itertools.count(1):
    run_casper_and_get_page(page)
