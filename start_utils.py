import functools

from app.apt.apt_utils import is_package_installed as apt_is_package_installed
from app.apt_pkg.package_utils import (
    describe_package_selection_status as apt_pkg_describe_package_selection_status,
)
from app.apt_pkg.apt_pkg_utils import find_package as apt_pkg_find_package


def print_result_dec(func):
    @functools.wraps(func)
    def _wrap(*args, **kwargs):
        print()
        _ = "*" * 50
        print(_ + " RESULTS " + _)
        return func(*args, **kwargs)

    return _wrap


def print_is_installed_success(package_name, package_version, result):
    if package_version is not None:
        package_name = f"{package_name!s}=={package_version!s}"

    is_installed = "installed" if result is True else "not installed"

    print(f"{package_name!s} is {is_installed}.")


def print_is_installed_failure(package_name, package_version, error):
    if package_version is not None:
        package_name = f"{package_name!s}=={package_version!s}"

    print(f"Could not check if {package_name!s} is installed. Reason: {error!s}.")


@print_result_dec
def print_install_package_success(package_name, package_version, result):
    is_installed = apt_is_package_installed(package_name, package_version)

    if package_version is not None:
        package_name = f"{package_name!s}=={package_version!s}"

    print(result)

    if is_installed is True:
        print(f"{package_name!s} is now installed.")
    else:
        print(f"Unable to install {package_name!s}.")


@print_result_dec
def print_install_package_failure(package_name, package_version, error):
    if package_version is not None:
        package_name = f"{package_name!s}=={package_version!s}"

    print(f"Could not install {package_name!s}. Reason: {error!s}.")


@print_result_dec
def print_mark_package_immutable_success(package_name, package_version, result):
    package = apt_pkg_find_package(package_name, package_version)
    package_status = apt_pkg_describe_package_selection_status(package)

    if package_version is not None:
        package_name = f"{package_name!s}=={package_version!s}"

    print(f"{package_name!s} is now {package_status}.")


@print_result_dec
def print_mark_package_immutable_failure(package_name, package_version, error):
    if package_version is not None:
        package_name = f"{package_name!s}=={package_version!s}"

    print(f"Could not mark as immutable {package_name!s}. Reason: {error!s} .")
