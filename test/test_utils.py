"""utils.py 的单元测试。

跑法（在 arxiv-tool 目录下）：
    .\\.venv\\Scripts\\python.exe -m pytest -v
"""
from arxiv_tool import utils
from arxiv_tool.models import Paper


def test_normalize_collapses_whitespace():
    assert utils.normalize_title("  Lost in the     Middle ") == "lost in the middle"


def test_normalize_eats_tab():
    assert utils.normalize_title("Lost\tin the Middle") == "lost in the middle"


def test_title_contains_matches_at_start():
    p = [Paper(title="RAG 系统", authors=[], year=2020, tags=[])]
    assert len(utils.title_contains(p, "RAG")) == 1


def test_author_initials_handles_double_space():
    assert utils.author_initials("Andrew  Lewis") == "A.L."


def test_find_paper_returns_none_for_empty_keyword():
    p = [
        Paper(title="RAG 系统", authors=[], year=2020, tags=["A"], citations=1),
        Paper(title="PoisonedRAG", authors=[], year=2024, tags=["A", "B"], citations=7)
    ]
    assert utils.find_paper(p, "") is None


def test_year_range_returns_none_for_empty_list():
    p = []
    assert utils.year_range(p) is None

    