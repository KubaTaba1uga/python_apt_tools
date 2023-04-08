import apt_pkg as pkg


def cmp_packages(os_package: pkg.Package, user_package: dict) -> bool:
    """ False if os package is not compatibile with user's package. """
    result: bool = False

    result = str(os_package.name) == user_package["name"]

    if user_package.get("version") and result is True:
        result = cmp_versions(os_package.current_ver, user_package["version"])

    return result


def cmp_versions(os_ver: pkg.Version, user_ver: str) -> bool:
    """ False if os version is not compatibile with user's version. """
    return os_ver.ver_str == user_ver
