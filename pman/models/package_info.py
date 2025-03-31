import versions


class PackageInfo:
    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        version: str | versions.Version,
        author_name: str,
        created_at: int,
        updated_at: int,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.author_name = author_name
        self.created_at = created_at
        self.updated_at = updated_at
        if isinstance(version, str):
            self.version = versions.parse_version(version)
        else:
            self.version = version
