from dataclasses import dataclass


@dataclass
class Package:
    id: int
    name: str
    description: str
    version: str
    author_name: str
    data: str
    created_at: int
    updated_at: int
