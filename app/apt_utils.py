import typing

import apt

from app.package_utils import cmp_packages
from app.package_utils import cmp_versions
from app.package_utils import is_version_eq


def is_package_installed(
    package_name: str,
    package_version: typing.Optional[str] = None,
    cache: typing.Optional[apt.Cache] = None,
) -> bool:
    """ Looks for a package among all cached packages."""
    user_package = find_package(package_name, package_version, cache)

    return (
        _is_package_installed(user_package, package_version) if user_package else False
    )


def find_package(
    package_name: str,
    package_version: typing.Optional[str] = None,
    cache: typing.Optional[apt.Cache] = None,
) -> typing.Optional[apt.Package]:
    """ Looks for a package among all cached packages."""
    user_package = {"name": package_name}

    if package_version:
        user_package["version"] = package_version

    if cache is None:
        cache = apt.Cache()

    for os_package_name in cache.keys():

        package = cache[os_package_name]

        if cmp_packages(package, user_package) is True:
            return package

    return None


def _is_package_installed(
    package: apt.Package, package_version: typing.Optional[str] = None
) -> bool:
    """ Determines if package is installed."""
    result = package.installed is not None

    if package_version is not None:
        result = is_version_eq(package.installed, package_version)

    return result


# def _is_installed_status(status_flag: int) -> bool:
#     """ Determines if package status is INSTALLED"""
#     status_info = _recognize_package_status(status_flag)

#     if status_info is PACKAGE_INSTALLED_STATUS:
#         return True

#     return False


# def _recognize_package_status(status_flag: int) -> typing.Optional[str]:
#     """ Map number status to descriptive string. """
#     for key, value in PACKAGE_STATUS_MAP.items():
#         if value == status_flag:
#             return key

#     return None


def install_package(package_name: str, package_version: typing.Optional[str] = None):
    cache = apt.Cache()

    user_package = find_package(package_name, package_version, cache)

    if not user_package:
        return

    user_package.mark_install()

    cache.commit()
