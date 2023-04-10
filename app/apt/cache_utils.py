import typing

import apt


def create_cache() -> apt.Cache:
    return apt.Cache()


def commit_changes(cache: apt.Cache):
    cache.commit()


def is_cache(anything: typing.Any) -> bool:
    return isinstance(anything, apt.Cache)
