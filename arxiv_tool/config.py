"""项目配置：接口地址，命名空间，超时与尝试次数。"""

API_URL = "http://export.arxiv.org/api/query"

ATOM_NS = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}

CONNECT_TIMEOUT = 20

MAX_ATTEMPTS = 3