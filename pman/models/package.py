import versions


class Package:
    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        version: str | versions.Version,
        data: bytes | str,
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
        self.version: versions.Version
        self.data: bytes

        if isinstance(version, str):
            self.version = versions.parse_version(version)
        else:
            self.version = version
        if isinstance(data, str):
            self.data = bytes(data, "utf-8")
        else:
            self.data = data

        self.dir_name = self.name + self.version.to_string()
