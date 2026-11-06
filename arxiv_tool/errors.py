class ArxivError(Exception):
    """本项目所有异常的基类"""



class ArxivFetchError(ArxivError):
    """网络层失败：连不上、超时、网关故障、可以等一会再试。"""
    hint = "网络或上游暂时故障，稍后再试：一直失败就检查代理"


class ArxivRateLimitError(ArxivFetchError):
    """
    被限流（429），要等很久。
    限流也属于网络层失败，except ArxivFetchError 应该能一次抓住这两个。
    """
    hint = "请求太频繁，请等几分钟后再试；不要连续重试"


class ArxivDataError(ArxivError):
    """连上了，但返回内容不符合预期：不是xml、缺字段。"""
    hint = "arxiv返回的内容不对，通常是限流或维护页，过几分钟再试"


class ArxivBugError(ArxivError):
    """我们请求了不存在的地址，或者代码假设错了，必须改代码。"""
    hint = "这是代码问题，需要修URL或解析逻辑，不是你的问题"