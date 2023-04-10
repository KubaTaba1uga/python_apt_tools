import apt_pkg


def find_package(
    package_name: str,
    package_version: typing.Optional[str] = None,
    cache: typing.Optional[apt_pkg.Cache] = None,
) -> apt_pkg.Cache:

    if cache is None:
        cache = apt_pkg.Cache()

    for package in cache.packages:
        pass
