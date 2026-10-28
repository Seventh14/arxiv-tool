import argparse
import requests
import xml.etree.ElementTree as ET
import json
import sys


parser = argparse.ArgumentParser()
parser.add_argument("--query", required=True, help="query必填，按照关键词筛选论文")
parser.add_argument("--max-results", type=int, default=10, help="返回的最大结果数量")
parser.add_argument("--out", default="arxiv_papers.json", help="写入的文件名")

args = parser.parse_args()


def fetch(query: str, max_results: int) -> list[dict]:
    """
    返回的dict有三个键：title，authors，year
    """
    url = "http://export.arxiv.org/api/query"
    params = {"search_query": query, "max_results": max_results}
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    ns = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
    root = ET.fromstring(r.text)
    result = []
    for entry in root.findall("a:entry", ns):
        result.append({
            "title": " ".join(entry.find("a:title", ns).text.split()),
            "authors": [a.find("a:name", ns).text for a in entry.findall("a:author", ns)],
            "year": int(entry.find("a:published", ns).text[:4])
        })
    return result

try:
    papers = fetch(args.query, args.max_results)
    
except requests.exceptions.RequestException:
    print("Requests异常")
    sys.exit(1)
except ET.ParseError:
    print("arxiv 限流或维护")
    sys.exit(1)

with open(args.out, "w", encoding="utf-8") as f:
    json.dump(papers, f, ensure_ascii=False, indent=2)
    print(len(papers))
