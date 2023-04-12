import typing
import functools

import apt

from app.errors import PackageNotFoundError
from app.apt.package_utils import cmp_packages
from app.apt.package_utils import cmp_versions
from app.apt.package_utils import is_version_eq
from app.apt.package_utils import create_package_name_ver_str
from app.apt.package_utils import mark_install
from app.apt.cache_utils import create_cache
from app.apt.cache_utils import is_cache
from app.apt.cache_utils import commit_changes


def _create_cache_if_needed(func):
    @functools.wraps(func)
    def _wrapped_func(*args, **kwargs):

        is_cache_in_args, is_cache_in_kwargs = (
            any(is_cache(arg) for arg in args),
            is_cache(kwargs.get("cache")),
        )

        if is_cache_in_args is True or is_cache_in_kwargs is True:
            pass
        else:
            kwargs["cache"]: apt.Cache = create_cache()

        return func(*args, **kwargs)

    return _wrapped_func


@_create_cache_if_needed
def is_package_installed(
    package_name: str,
    package_version: typing.Optional[str] = None,
    cache: typing.Optional[apt.Cache] = None,
) -> bool:
    """Looks for a package among all cached packages."""
    user_package = find_package(package_name, package_version, cache)

    return (
        _is_package_installed(user_package, package_version) if user_package else False
    )


@_create_cache_if_needed
def find_package(
    package_name: str,
    package_version: typing.Optional[str] = None,
    cache: typing.Optional[apt.Cache] = None,
) -> typing.Optional[apt.Package]:
    """Looks for a package among all cached packages."""

    user_package = {"name": package_name}

    if package_version:
        user_package["version"] = package_version

    for os_package_name in cache.keys():

        package = cache[os_package_name]

        if cmp_packages(package, user_package) is True:
            return package

    return None


def _is_package_installed(
    package: apt.Package, package_version: typing.Optional[str] = None
) -> bool:
    """Determines if package is installed."""
    is_installed = package.installed is not None

    if package_version is not None:
        is_installed = is_version_eq(package.installed, package_version)

    return is_installed


@_create_cache_if_needed
def install_package(
    package_name: str,
    package_version: typing.Optional[str] = None,
    cache: typing.Optional[apt.cache.Cache] = None,
):

    user_package = find_package(package_name, package_version, cache)

    if not user_package:
        raise PackageNotFoundError()

    mark_install(user_package)

    commit_changes(cache)
