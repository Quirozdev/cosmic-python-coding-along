import json
import requests
import duckduckpy
from urllib.request import urlopen
from urllib.parse import urlencode

params = dict(q='Sausages', format='json')
# handle = urlopen('http://api.duckduckgo.com' + '?' + urlencode(params))
# raw_text = handle.read().decode('utf8')
# parsed = json.loads(raw_text)

# parsed = requests.get('http://api.duckduckgo.com/', params=params).json()

# results = parsed['RelatedTopics']
# for r in results:
#     if 'Text' in r:
#         print(r['FirstURL'] + ' - ' + r['Text'])

for r in duckduckpy.query('Sausages')['RelatedTopics']:
    print(r['FirstURL'] + ' - ' + r['Text'])