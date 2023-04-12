import typing

import apt_pkg as pkg

from app.apt.apt_utils import is_version_eq
from app.apt_pkg.data_structures import SELECTION_STATUS_MAP


def cmp_packages(os_package: pkg.Package, user_package: dict) -> bool:
    """ False if os package is not compatibile with user's package. """

    is_package_compatibile: bool = False

    is_package_compatibile = str(os_package.name) == user_package["name"]

    if user_package.get("version") is not None and is_package_compatibile is True:
        is_package_compatibile = cmp_versions(
            os_package.version_list, user_package["version"]
        )

    return is_package_compatibile


def cmp_versions(os_verions: typing.List[pkg.Version], user_ver: str) -> bool:
    """ False if os version is not compatibile with user's version. """

    for version in os_verions:
        if is_version_eq(version.ver_str, user_ver):
            return True

    return False


def describe_package_selection_status(package: pkg.Package) -> str:
    package_selection_status = _get_selection_status(package)

    for description, value in SELECTION_STATUS_MAP.items():
        if package_selection_status == value:
            return description

    raise ValueError(f"Unknown package selection status {_get_name(package)!s}")


def _get_selection_status(package: pkg.Package) -> int:
    return package.selected_state


def _get_name(package: pkg.Package) -> str:
    return package.name
