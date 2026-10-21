import json

with open("papers.json", mode='r', encoding="utf-8") as file:
    papers = json.load(file)

print("共", len(papers), "篇论文")

matched = [p for p in papers if p["year"] >= 2025]
print(f"---2025年及以后({len(matched)}篇)---")
for i, p in enumerate(matched, start=1):
    print(f"{i}. {p['title']}")

sorted_papers = sorted(papers, key = lambda x:x["citations"], reverse = True)
print("---引用数top3---")
for i, paper in enumerate(sorted_papers[:3], start=1):
        print(f"{i}.{paper['title']} —{paper['citations']}")

matched_1 = [p for p in papers if "RAG" in p["tags"]]
print(f"---含RAG标签({len(matched_1)}篇)")
for i, p in enumerate(matched_1, start=1):
    print(f"{i}.{p['title']}")


