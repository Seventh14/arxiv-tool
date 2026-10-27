import json
import csv

def load_csv(path: str) -> list:
    with open(path, encoding="utf-8", newline="") as f:
        back = list(csv.DictReader(f))
    for row in back:
        row["citations"] = int(row["citations"])    # 字符串->整型
        row["year"] = int(row["year"])              # 字符串->整型
        row["tags"] = row["tags"].split("|")        # 字符串->列表
    return back


def save_papers_csv(papers: list, path: str) -> None:
    # newline=""：Windows 上防止 csv 多写空行
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["title", "authors", "year", "citations", "tags"])
        w.writeheader()
        for paper in papers:
            row = dict(paper)
            row["authors"] = "|".join(paper["authors"])
            row["tags"] = "|".join(paper["tags"])
            w.writerow(row)

def load_papers(path: str) -> list:
    with open(path, encoding='utf-8-sig') as f:
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

def normalize_title(title: str) -> str:
    # 统一标题格式，方便比较：去掉首尾空格、把连续的多个空格压缩成一个、全部转成小写
    return " ".join(title.split()).lower()

def shorten_title(title: str, max_len: int = 30) -> str:
    # 标题太长就截断，并加上省略号。
    # 正文最多max_len个字符
    if len(title) > max_len:
        return title[:max_len] + "……"
    return title

def title_contains(papers: list, keyword: str) -> list:
    # 返回标题里包含关键字的论文列表
    result = []
    for paper in papers:
        if normalize_title(keyword) in normalize_title(paper["title"]):
            result.append(paper)
    return result

def author_initials(name: str) -> str:
    # 边界情况：对于只有名、没有姓的字符串，返回原值
    if len(name.split()) < 2:
        return name
    return ".".join(x[0] for x in name.split()).upper() + "."

def citations_by_tag(papers: list) -> dict:
    # 统计每个标签下论文的总引用数
    result = {}
    for paper in papers:
        for tag in paper["tags"]:
            result[tag] = result.get(tag, 0) + paper["citations"]
    return result

def find_paper(papers: list, title: str) -> dict | None:
    # 按标题找一篇论文，找不到时返回None，不返回{}
    if len(papers) == 0 or title == "":
        return None
    for paper in papers:
        if normalize_title(paper["title"]).find(normalize_title(title)) > -1:
            return paper
    return None

def year_range(papers: list) -> tuple | None:
    # 返回 (最早年份, 最晚年份)，这批数据应该是 (2020, 2025)
    if len(papers) < 1:
        return None
    earliest_year = min(p["year"] for p in papers)
    latest_year = max(p["year"] for p in papers)
    return (earliest_year, latest_year)

def load_papers_safe(path: str) -> list | None:
    # 和已有的 load_papers 一样，但文件不存在或者 JSON 格式坏掉时不要崩溃
    try:
        return load_papers(path)
    except json.decoder.JSONDecodeError as e1:
        return None
    except FileNotFoundError as e2:
        return None
