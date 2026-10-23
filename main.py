from utils import load_papers, count_papers, filter_by_year, sort_by_citations, filter_by_tag, average_citations, group_by_year, top_authors

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
print(group_by_year(papers))

n = 2
top_n_authors = top_authors(papers, n)
print(top_n_authors)
print(f"---作者出现次数前{n}名---")
for name, count in top_n_authors:
    print(f"{name} = {count}")
