import typing

import apt


def cmp_packages(os_package: apt.Package, user_package: dict) -> bool:
    """ False if os package is not compatibile with user's package. """
    result: bool = False

    result = str(os_package.name) == user_package["name"]

    if user_package.get("version") and result is True:
        result = cmp_versions(os_package.versions, user_package["version"])

    return result


def cmp_versions(os_verions: typing.List[apt.Version], user_ver: str) -> bool:
    """ False if os version is not compatibile with user's version. """

    for version in os_verions:
        if is_version_eq(version.version, user_ver):
            return True

    return False


def is_version_eq(version_a: str, version_b: str) -> bool:
    return version_a == version_b
