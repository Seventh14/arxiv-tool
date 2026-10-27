import argparse
import sys
import json
from utils import load_papers, filter_by_year, sort_by_citations, filter_by_tag, save_papers_csv

parser = argparse.ArgumentParser(description="按关键词和年份筛选论文")
parser.add_argument("--query", required=True, help="关键词，例如RAG")
parser.add_argument("--min-year", type=int, default=2000, help="最早年份")
parser.add_argument("--top", type=int, default=5, help="返回前N篇")
parser.add_argument("--file", default="papers.json", help="数据文件路径")
parser.add_argument("--export", help="把结果导出到CSV路径，例如out.csv")

args = parser.parse_args()

try:
    papers = load_papers(args.file)
except FileNotFoundError:
    print(f"找不到数据文件：{args.file}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"文件不是合法的JSON：{args.file}")
    sys.exit(1)

hit = filter_by_tag(papers, args.query)
hit = filter_by_year(hit, args.min_year)

result = sort_by_citations(hit, args.top)
if args.export:
    save_papers_csv(result, args.export)

for paper in result:
    print(paper["title"])