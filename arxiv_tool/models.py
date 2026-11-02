from dataclasses import dataclass

@dataclass
class Paper:
    title: str
    authors: list[str]
    year: int
    tags: list[str]
    citations: int | None = None