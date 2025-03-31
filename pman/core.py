import aiohttp
import versions
import tarfile
import os
from typing import Final, Callable
from .errors import Errors
from .urls import Urls
from .models import (
    Package,
    PackageInfo,
)

API_DOMAIN: Final = "http://localhost:8000/"
UPGRADE: Final = "upgrade"


class ClientSession(aiohttp.ClientSession):
    def __init__(self, api_domain: str = API_DOMAIN):
        super().__init__()
        self.api_domain = api_domain

    def format_url(self, url: str) -> str:
        return self.api_domain + url

    async def get_package_by_id(self, package_id: int) -> None | Package:
        async with self.get(
            self.format_url(Urls.GET_PACKAGE),
            json={
                "package_id": package_id,
            },
        ) as response:
            match response.status:
                case 200:
                    return Package(**(await response.json()))
                case 404:
                    return None
                case 500:
                    raise Errors.ServerError()
                case _:
                    raise Errors.UnidentifiedError()

    async def get_package_info_by_id(self, package_id: int) -> None | PackageInfo:
        async with self.get(
            self.format_url(Urls.GET_PACKAGE_INFO),
            json={
                "package_id": package_id,
            },
        ) as response:
            match response.status:
                case 200:
                    return PackageInfo(**(await response.json()))
                case 404:
                    return None
                case 500:
                    raise Errors.ServerError()
                case _:
                    raise Errors.UnidentifiedError()

    async def get_packages_info_by_name(
        self,
        package_name: str,
    ) -> None | list[PackageInfo]:
        async with self.get(
            self.format_url(Urls.GET_PACKAGES_INFO),
            json={
                "package_name": package_name,
            },
        ) as response:
            match response.status:
                case 200:
                    response_json = await response.json()
                    if "packages" in response_json:
                        return [
                            PackageInfo(**package_info)
                            for package_info in response_json["packages"]
                        ]
                    else:
                        raise Errors.ServerError()
                case 404:
                    return None
                case 500:
                    raise Errors.ServerError()
                case _:
                    raise Errors.UnidentifiedError()

    async def get_package(
        self,
        package_name: str,
        package_version: versions.Version | str | None = None,
        upgrade: bool = True,
        ge: bool = False,
        gt: bool = False,
        le: bool = False,
        lt: bool = False,
    ) -> Package | None:
        if isinstance(package_version, str):
            package_version = versions.parse_version(package_version)

        if packages_info := await self.get_packages_info_by_name(package_name):
            returned_package_info = packages_info.pop(0)
            for package_info in packages_info:
                if upgrade:
                    if returned_package_info.version < package_info.version:
                        returned_package_info = package_info
                elif package_version:
                    if ge:
                        if package_info.version >= package_version:
                            returned_package_info = package_info
                    elif gt:
                        if package_info.version > package_version:
                            returned_package_info = package_info
                    elif le:
                        if package_info.version <= package_version:
                            returned_package_info = package_info
                    elif lt:
                        if package_info.version < package_version:
                            returned_package_info = package_info
                    else:
                        if package_info.version == package_version:
                            returned_package_info = package_info
                else:
                    raise Errors.VersionIsRequiredError()

            return await self.get_package_by_id(returned_package_info.id)
        else:
            return None

    async def install_package(
        self,
        package_name: str,
        dir_path: str,
        package_version: versions.Version | str | None = None,
        upgrade: bool = True,
        ge: bool = False,
        gt: bool = False,
        le: bool = False,
        lt: bool = False,
    ) -> Package | None:
        if os.path.isdir(dir_path):
            if package := await self.get_package(
                package_name=package_name,
                package_version=package_version,
                upgrade=upgrade,
                ge=ge,
                gt=gt,
                le=le,
                lt=lt,
            ):
                package_dir_path = f"{dir_path + package.dir_name}.tar.gz"
                with open(package_dir_path, "wb") as package_tar_gz_file:
                    package_tar_gz_file.write(package.data)
                    try:
                        with tarfile.TarFile(
                            fileobj=package_tar_gz_file
                        ) as package_tar_gz:
                            package_tar_gz.extractall(dir_path + package.dir_name)
                    except tarfile.TarError as err:
                        os.remove(package_dir_path)
                        raise Errors.TarError(
                            f"Package extraction failed, this is most often due to the fact that the package is corrupted or has an invalid format. Original error: {err}"
                        )

            return package
        else:
            raise Errors.PathError()
