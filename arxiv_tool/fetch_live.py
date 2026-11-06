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
from arxiv_tool.errors import (
    ArxivError, ArxivFetchError, ArxivRateLimitError, ArxivDataError, ArxivBugError
)


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
    except ArxivError as exc:
        logger.error("%s", exc)
        logger.error("提示：%s", exc.hint)
        sys.exit(1)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump([asdict(p) for p in papers], f, ensure_ascii=False, indent=2)
    if args.export is not None:
        save_papers_csv(papers, args.export)
    print(len(papers))


def _backoff(attempt: int) -> None:
    """第 attempt 次失败后等 2**(attempt-1) 秒。"""
    time.sleep(2 ** (attempt - 1))


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

            try:
                root = ET.fromstring(r.text)
            except ET.ParseError as exc:
                raise ArxivDataError(f"返回的不是有效XML，可能是错误页或限流页：{exc}") from exc
            
            result = []
            for entry in root.findall("a:entry", ns):
                title_node = entry.find("a:title", ns)
                if title_node is None:
                    raise ArxivDataError("条目缺少title字段，arxiv返回的数据不完整")
                
                result.append(Paper(
                    title = " ".join(title_node.text.split()),
                    authors = [a.find("a:name", ns).text for a in entry.findall("a:author", ns)],
                    year = int(entry.find("a:published", ns).text[:4]),
                    tags = [entry.find("x:primary_category", ns).get("term")]
                ))
            return result           # 成功立即返回
        except requests.exceptions.ReadTimeout as exc:
            logger.debug("第 %s 次失败：%s", attempt, exc)
            if attempt == 3:
                raise ArxivFetchError(f"读取超时（已重试3次）：{exc}") from exc         
            _backoff(attempt)
        except requests.exceptions.HTTPError as exc:
            code = exc.response.status_code
            logger.debug("第 %s 次失败：%s", attempt, exc)
            if code == 429:
                if attempt == 3:
                    raise ArxivRateLimitError(f"被arxiv限流（429，已重试3次）：{exc}") from exc
            elif code in (502, 503, 504):
                if attempt == 3:
                    raise ArxivFetchError(f"上游网关故障（HTTP{code}，已重试3次）：{exc}") from exc
            else:
                raise ArxivBugError(f"请求被拒绝（HTTP{code}，这不是网络问题，是地址或接口变了）") from exc
            _backoff(attempt)
        except requests.exceptions.ConnectTimeout as exc:
            raise ArxivFetchError(
                f"连接超时，（20s未连上）：{exc}，检查网络或代理是否开着"
                ) from exc

            

if __name__ == "__main__":
    main()