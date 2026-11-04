import argparse
import requests
import xml.etree.ElementTree as ET
import json
import sys
from arxiv_tool.utils import save_papers_csv
import logging
from arxiv_tool.models import Paper
from dataclasses import asdict
import time

logger = logging.getLogger(__name__)


parser = argparse.ArgumentParser()
parser.add_argument("--query", required=True, help="query必填，按照关键词筛选论文")
parser.add_argument("--max-results", type=int, default=10, help="返回的最大结果数量")
parser.add_argument("--out", default="arxiv_papers.json", help="写入的文件名")
parser.add_argument("--export", default=None, help="除了JSON，再存一份CSV")
parser.add_argument("-v", "--verbose", action="store_true", help="打印调试日志")

def main() -> None:
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
    )
    try:
        papers = fetch(args.query, args.max_results)  
    except requests.exceptions.RequestException as exc:
        logger.error("请求失败：%s", exc)
        sys.exit(1)
    except ET.ParseError as exc:
        logger.error("arxiv返回的不是有效XML（可能被限流或维护）：%s", exc)
        sys.exit(1)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump([asdict(p) for p in papers], f, ensure_ascii=False, indent=2)
    if args.export is not None:
        save_papers_csv(papers, args.export)
    print(len(papers))



def fetch(query: str, max_results: int) -> list[Paper]:
    """
    从 arXiv 抓论文，返回 Paper 列表。citations 恒为 None（API 不返回引用数）
    tags是长度为1的列表
    """
    url = "http://export.arxiv.org/api/query"
    params = {"search_query": query, "max_results": max_results}

    for attempt in range(1, 4):
        try:
            logger.debug("请求 %s 参数 %s", url, params)
            r = requests.get(url, params=params, timeout=20)
            r.raise_for_status()
            # 解析原样
            ns = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
            root = ET.fromstring(r.text)
            result = []
            for entry in root.findall("a:entry", ns):
                result.append(Paper(
                    title = " ".join(entry.find("a:title", ns).text.split()),
                    authors = [a.find("a:name", ns).text for a in entry.findall("a:author", ns)],
                    year = int(entry.find("a:published", ns).text[:4]),
                    tags = [entry.find("x:primary_category", ns).get("term")]
                ))
            return result           # 成功立即返回
        except requests.exceptions.ReadTimeout as exc:
            logger.debug("第 %s 次失败：%s", attempt, exc)
            if attempt == 3:
                raise           # 最后一次，原样输出，保留现场
            time.sleep(2 ** (attempt - 1))
        except requests.exceptions.HTTPError as exc:
            logger.debug("第 %s 次失败：%s", attempt, exc)
            if exc.response.status_code not in (502, 503, 504, 429):
                raise
            if attempt == 3:
                raise
            time.sleep(2 ** (attempt - 1))

            

if __name__ == "__main__":
    main()