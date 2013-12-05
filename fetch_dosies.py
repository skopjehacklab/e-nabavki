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

CMD = """python2 parse-dosie.py %s"""


def run_parse_and_get_dosie(url):
    cmd = (CMD % url).split()
    print "getting dosie at %s" % url
    parser = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    return json.load(parser.stdout)


for view_result in couch.view('dosie/by_state', key='pending'):
    doc = couch.get(view_result['id'])
    new_doc = run_parse_and_get_dosie(doc['link'])
    doc.update(new_doc)
    doc['state'] = 'done'
    couch.save_doc(doc)
