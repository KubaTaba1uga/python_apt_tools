import functools
import typing

import apt_pkg as pkg

from app.errors import PackageNotFoundError
from app.apt_pkg.package_utils import cmp_packages
from app.apt_pkg.package_utils import mark_package_immutable
from app.apt_pkg.cache_utils import commit_cache


def _create_cache_if_needed(func):
    @functools.wraps(func)
    def _wrapped_func(*args, **kwargs):

        is_cache_in_args, is_cache_in_kwargs = (
            any(is_cache(arg) for arg in args),
            is_cache(kwargs.get("cache")),
        )

        if is_cache_in_kwargs is False:
            apt_pkg = create_apt_pkg()
            kwargs["cache"] = apt_pkg.Cache()

        if is_cache_in_args is True:
            args = tuple(arg for arg in args if is_cache(arg) is False)

        return func(*args, **kwargs)

    return _wrapped_func


@_create_cache_if_needed
def find_package(
    package_name: str,
    package_version: typing.Optional[str] = None,
    cache: typing.Optional[pkg.Cache] = None,
) -> typing.Optional[pkg.Package]:
    """ Looks for a package among all cached packages."""
    user_package = {"name": package_name}

    if package_version:
        user_package["version"] = package_version

    for package in cache.packages:
        if cmp_packages(package, user_package) is True:
            return package

    return None


@_create_cache_if_needed
def hold_package(
    package_name: str,
    package_version: typing.Optional[str] = None,
    cache: typing.Optional[pkg.Cache] = None,
):
    user_package = find_package(package_version, package_name, cache)

    if not user_package:
        raise PackageNotFoundError()

    mark_package_hold(user_package)

    commit_cache(cache)


def is_apt_pkg(obj_: typing.Any) -> bool:
    return obj_ is pkg


def is_cache(obj_: typing.Any) -> bool:
    return isinstance(obj_, pkg.Cache)


def create_apt_pkg() -> pkg:
    pkg.init_config()
    pkg.init_system()
    return pkg


def is_apt_pkg(obj_: typing.Any) -> bool:
    return obj_ is pkg


def is_cache(obj_: typing.Any) -> bool:
    return isinstance(obj_, pkg.Cache)
