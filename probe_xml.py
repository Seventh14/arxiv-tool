import requests
import xml.etree.ElementTree as ET

r = requests.get("http://export.arxiv.org/api/query",
                 params={"search_query": "all:agent", "max_results": 1},
                 timeout=20)
r.raise_for_status()

with open("feed_probe.xml", "w", encoding="utf-8") as f:
    f.write(r.text)

root = ET.fromstring(r.text)
for tag in sorted({e.tag for e in root.iter()}):
    print(tag)