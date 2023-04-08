import typing

import apt_pkg as pkg

from app.str_utils import is_in_str
from app.version_utils import cmp_versions
from app.constants import PACKAGE_STATUS_MAP, PACKAGE_INSTALLED_STATUS


def is_package_installed(
    apt_pkg: pkg, package_name: str, package_version: typing.Optional[str] = None
) -> bool:
    """ Looks for a package among all cached packages."""
    cache = apt_pkg.Cache()

    for package in cache.packages:
        if is_in_str(package_name, str(package.name)) and _is_package_installed(
            package
        ):
            print(str(package.current_ver))

            if package_version is None:
                return True

            if cmp_versions(str(package.current_ver), package_version):
                return True

    return False


def _is_package_installed(package: pkg.Package) -> bool:
    """ Determines if package is installed."""
    return _is_installed_status(package.current_state)


def _is_installed_status(status_flag: int) -> bool:
    """ Determines if package state is INSTALLED"""
    status_info = _recognize_package_status(status_flag)

    if status_info is PACKAGE_INSTALLED_STATUS:
        return True

    return False


def _recognize_package_status(status_flag: int) -> typing.Optional[str]:
    """ Map numbers flags to descriptive strings. """
    for key, value in PACKAGE_STATUS_MAP.items():
        if value == status_flag:
            return key

    return None
