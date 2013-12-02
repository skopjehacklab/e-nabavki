from lxml import html
import requests

import sys
import json
from ConfigParser import ConfigParser

url = sys.argv[1]

cfg = ConfigParser()
cfg.optionxform = str
cfg.read(['settings.ini'])

page = html.fromstring(requests.get(url).text)

results = {}
selectors = cfg.options('selectors')

for value_id in selectors:
    name = cfg.get('selectors', value_id)
    val = page.get_element_by_id(value_id, None)
    if val is not None:
        results[name] = val.text.encode('utf-8')

print json.dumps(results, ensure_ascii=False, indent=4)

# print select(selectors[0]['name_id'], html)
