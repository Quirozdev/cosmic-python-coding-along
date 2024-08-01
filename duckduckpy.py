import requests

def query(q: str):
    parsed = requests.get('http://api.duckduckgo.com/', params={"q": q, "format": "json"}).json()
    return parsed