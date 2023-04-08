import typing

import apt_pkg as pkg

from app.package_utils import cmp_packages
from app.package_utils import cmp_versions
from app.constants import PACKAGE_STATUS_MAP, PACKAGE_INSTALLED_STATUS


def is_package_installed(
    apt_pkg: pkg, package_name: str, package_version: typing.Optional[str] = None
) -> bool:
    """ Looks for a package among all cached packages."""
    user_package = find_package(apt_pkg, package_name, package_version)

    return _is_package_installed(user_package) if user_package else False


def find_package(
    apt_pkg: pkg,
    package_name: str,
    package_version: typing.Optional[str] = None,
    cache: typing.Optional[pkg.Cache] = None,
) -> typing.Optional[pkg.Package]:
    """ Looks for a package among all cached packages."""
    user_package = {"name": package_name}

    if package_version:
        user_package["version"] = package_version

    if cache is None:
        cache = apt_pkg.Cache()

    for package in cache.packages:
        if cmp_packages(package, user_package) is True:
            return package

    return None


def _is_package_installed(package: pkg.Package) -> bool:
    """ Determines if package is installed."""
    return _is_installed_status(package.current_state)


def _is_installed_status(status_flag: int) -> bool:
    """ Determines if package status is INSTALLED"""
    status_info = _recognize_package_status(status_flag)

    if status_info is PACKAGE_INSTALLED_STATUS:
        return True

    return False


def _recognize_package_status(status_flag: int) -> typing.Optional[str]:
    """ Map number status to descriptive string. """
    for key, value in PACKAGE_STATUS_MAP.items():
        if value == status_flag:
            return key

    return None


def install_package(
    apt_pkg: pkg, package_name: str, package_version: typing.Optional[str] = None
):
    cache = apt_pkg.Cache()
    cache_mg = apt_pkg.DepCache(cache=cache)

    user_package = find_package(apt_pkg, package_name, package_version, cache)

    if not user_package:
        return

    cache_mg.mark_install(user_package)
