from lxml import etree
from lxml.cssselect import CSSSelector
import requests as r
import sys
import json
from pprint import pprint

url = sys.argv[1]
selectors = json.load(open('selectors.json'))

res = r.get(url)
html = etree.HTML(res.text)

def select(selector, html):
	sel = CSSSelector(selector)
	return sel(html)[0].text.strip()

def contents(selectors, html):
	res = {}
	for s in selectors:
		name = select(s['name_id'], html)
		val = select(s['value_id'], html)
		res[name] = val
	return res

print json.dumps(contents(selectors, html), ensure_ascii=False, indent=4).encode('utf8')

# print select(selectors[0]['name_id'], html)
