import json

def load_papers(path: str) -> list:
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def count_papers(papers: list) -> int:
    return len(papers)

def filter_by_year(papers: list, min_year: int) -> list:
    return [p for p in papers if p["year"] >= min_year]

def sort_by_citations(papers: list, top_n: int) -> list:
    return sorted(papers, key=lambda x:x["citations"], reverse=True)[:top_n]

def filter_by_tag(papers: list, tag: str) -> list:
    return [p for p in papers if tag in p["tags"]]