import json

def load_papers(path: str) -> list:
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def count_papers(papers: list) -> int:
    return len(papers)

def filter_by_year(papers: list, min_year: int) -> list:
    return [p for p in papers if p["year"] >= min_year]

def sort_by_citations(papers: list, top_n: int) -> list:
    return top_papers(papers, top_n)

def filter_by_tag(papers: list, tag: str) -> list:
    return [p for p in papers if tag in p["tags"]]

def average_citations(papers: list) -> float:
    total = 0
    for paper in papers:
        total += paper["citations"]
    return total / len(papers)

def group_by_year(papers: list) -> dict:
    result = {}
    for paper in papers:
        result[paper["year"]] = result.get(paper["year"], 0) + 1
    return dict(sorted(result.items(), reverse=True))

def top_authors(papers: list, n: int) -> list[tuple]:
    result = []
    authors = {}
    for paper in papers:
        for author in paper["authors"]:
            authors[author] = authors.get(author, 0) + 1
    for author_num in sorted(authors.items(),key=lambda x:x[1], reverse=True)[:n]:
        result.append(author_num)
    return result

def sort_papers_by_year(papers: list, descending=False) -> list:
    return sorted(papers, key=lambda x:x["year"], reverse=descending)

def unique_tags(papers: list) -> list:
    return sorted({tag for paper in papers for tag in paper["tags"]})

def papers_per_tag(papers: list) -> dict:
    result = {}
    for paper in papers:
        for tag in paper["tags"]:
            result[tag] = result.get(tag, 0) + 1
    return result

def top_papers(papers: list, n: int, by: str = "citations") -> list:
    return sorted(papers, key=lambda x:x[by], reverse=True)[:n]