from utils import load_papers, count_papers, filter_by_year, sort_by_citations, filter_by_tag, average_citations, group_by_year, top_authors
from utils import sort_papers_by_year, unique_tags, papers_per_tag, top_papers
from utils import normalize_title, shorten_title, title_contains, author_initials
from utils import citations_by_tag, find_paper, year_range, load_papers_safe

papers = load_papers("papers.json")

print(f"共{count_papers(papers)}篇论文")

matched = filter_by_year(papers, 2025)
print(f"---2025年及以后({count_papers(matched)}篇)---")
for i, p in enumerate(matched, start=1):
    print(f"{i}. {p['title']}")

sorted_papers = sort_by_citations(papers, 3)
print("---引用数top3---")
for i, paper in enumerate(sorted_papers, start=1):
    print(f"{i}.{paper['title']} —{paper['citations']}")

matched_1 = filter_by_tag(papers, "RAG")
print(f"---含RAG标签({count_papers(matched_1)}篇)")
for i, p in enumerate(matched_1, start=1):
    print(f"{i}.{p['title']}")

print(f"---平均引用数：{average_citations(papers):.1f}---")
for year, nums in group_by_year(papers).items():
    print(f"{year}年：{nums}篇")
     

n = 2
print(f"---作者出现次数前{n}名---")
for name, count in top_authors(papers, n):
    print(f"{name} = {count}")

print([p["year"] for p in sort_papers_by_year(papers)])
print(unique_tags(papers))

count_papers_per_tag = papers_per_tag(papers)
for tag, nums in count_papers_per_tag.items():
    print(f"tag：{tag}有{nums}篇")

print([p["citations"] for p in top_papers(papers, 3)])

print("---测试字符串函数---")
test_title = papers[1]["title"]
print(normalize_title(test_title))

print(shorten_title(test_title))

t = "rag"
title_contains_tag = title_contains(papers, t)
print(f"含“{t}”的论文：{count_papers(title_contains_tag)}篇")
for paper in title_contains_tag:
    print(paper["title"])

print("---测试文件和字典函数---")
if not papers:
    print("数据是空的，检查一下 papers.json")

paper_citations_by_tag = citations_by_tag(papers)
for tag, total in paper_citations_by_tag.items():
    print(f"{tag}:共{total}次引用")

found = find_paper(papers, "lost in the middle")
print(f"按标题查找：{found['title'] if found else '没找到'}")
print(year_range(papers))
print(f"安全加载一个不存在的文件：{load_papers_safe('nope.json')}")
