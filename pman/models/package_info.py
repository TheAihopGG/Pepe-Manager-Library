from dataclasses import dataclass


@dataclass
class PackageInfo:
    id: int
    name: str
    description: str
    version: str
    author_name: str
    created_at: int
    updated_at: int
