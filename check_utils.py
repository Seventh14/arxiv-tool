"""用真实数据把 utils.py 的每个函数跑一遍，看输出对不对。

用法（在 arxiv-tool 目录下）：
    ./.venv/Scripts/python.exe check_utils.py

这只是个排查脚本，不是正式测试框架。W3 会讲 try/except，到时候可以升级。
"""
from pathlib import Path
import tempfile

from arxiv_tool import utils

papers = utils.load_papers(str(Path(__file__).parent / "papers.json"))


def show(label, fn):
    """跑一个用例，出错就打印异常类型——不要自己 try 掉，报错本身就是信息。"""
    try:
        print(f"{label} -> {fn()!r}")
    except Exception as e:
        print(f"{label} -> RAISED {type(e).__name__}: {e}")


def make_bad_file(content: str) -> str:
    """在系统临时目录现造一个文件，返回路径。

    测试夹具不进仓库：每次跑脚本时生成，跑完由系统回收临时目录。
    """
    path = Path(tempfile.gettempdir()) / "check_bad.json"
    path.write_text(content, encoding="utf-8")
    return str(path)

def check_save_keeps_input():
    # ① 准备：最小数据。5 个字段一个不能少，
    # 因为 save_papers_csv 的 fieldnames 写死了这 5 列
    p = [{"title": "T", "authors": ["A", "B"], "year": 2020,
          "citations": 1, "tags": ["RAG"]}]
    # ② 动作：写到临时目录（和你 make_bad_file 一个思路，别写进仓库）
    path = Path(tempfile.gettempdir()) / "check_out.csv"
    utils.save_papers_csv(p, str(path))
    # ③ 判据：入参还是不是原来的形状
    return type(p[0]["tags"]).__name__, p[0]["tags"]

show("1  normalize 多空格", lambda: utils.normalize_title("  Lost in  the   Middle "))
show("1b normalize 含 tab", lambda: utils.normalize_title("Lost\tin the Middle"))
show("2  shorten 边界", lambda: (utils.shorten_title("a" * 40, 10), len(utils.shorten_title("a" * 40, 10))))
show("3  title_contains('rag')", lambda: utils.title_contains(papers, "rag"))
show("3b title_contains 开头匹配", lambda: utils.title_contains([{"title": "RAG 系统"}], "RAG"))
show("4  initials 正常", lambda: utils.author_initials("Andrew Lewis"))
show("4b initials 双空格", lambda: utils.author_initials("Andrew  Lewis"))
show("4c initials 只有名", lambda: utils.author_initials("Lewis"))
show("5  citations_by_tag", lambda: utils.citations_by_tag(papers))
show("6  find_paper 全小写", lambda: (utils.find_paper(papers, "lost in the middle") or {}).get("title"))
show("6b find_paper 空串", lambda: (utils.find_paper(papers, "") or {}).get("title"))
show("7  year_range", lambda: utils.year_range(papers))
show("7b year_range 空列表", lambda: utils.year_range([]))
show("8  safe 文件不存在", lambda: utils.load_papers_safe("nope.json"))
show("8b safe JSON 坏掉", lambda: utils.load_papers_safe(make_bad_file('{"title": "坏掉的",,}')))
show("8c safe 空文件", lambda: utils.load_papers_safe(make_bad_file("")))
show("9  save 不改入参", check_save_keeps_input)


def check_load_csv_bom():
    """带 BOM 的 CSV 也要读得回来。

    先让 save_papers_csv 写一份正常的（无 BOM），再用 utf-8-sig 重写一遍，
    模拟"被记事本/Excel 保存过"的文件——这一步必须经过磁盘，内存里造不出来。
    若 load_csv 用 utf-8 读，第一个列名会变成 "\ufefftitle"，取值就 KeyError。
    """
    p = [{"title": "带BOM", "authors": ["A"], "year": 2021,
          "citations": 7, "tags": ["RAG", "security"]}]
    path = Path(tempfile.gettempdir()) / "check_bom.csv"
    utils.save_papers_csv(p, str(path))
    text = path.read_text(encoding="utf-8")
    path.write_text(text, encoding="utf-8-sig")      # 重写成带 BOM
    back = utils.load_csv(str(path))
    return back[0]["citations"], back[0]["tags"]


show("10 load_csv 带 BOM", check_load_csv_bom)