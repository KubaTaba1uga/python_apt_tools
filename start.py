#!/usr/bin/env python3
"""
        Usage:
                start.py install_package <package_name> [<package_version>]
                start.py is_package_installed <package_name> [<package_version>]
                start.py mark_package_immutable <package_name> [<package_version>]
"""
import functools

from docopt import docopt
from apt_pkg import Error as AptPkgError

from app.apt.apt_utils import is_package_installed
from app.apt.apt_utils import install_package
from app.apt_pkg.apt_pkg_utils import mark_package_immutable
from app.errors import PackageNotFoundError

from start_utils import (
    print_install_package_failure,
    print_install_package_success,
    print_is_installed_failure,
    print_is_installed_success,
    print_mark_package_immutable_success,
    print_mark_package_immutable_failure,
)


APT_UTILS_ARGUMENTS_MAP = {
    "is_package_installed": {
        "function": is_package_installed,
        "exceptions": [],
        "success_function": print_is_installed_success,
        "failure_function": print_is_installed_failure,
    },
    "install_package": {
        "function": install_package,
        "exceptions": [PackageNotFoundError],
        "success_function": print_install_package_success,
        "failure_function": print_install_package_failure,
    },
    "mark_package_immutable": {
        "function": mark_package_immutable,
        "exceptions": [PackageNotFoundError],
        "success_function": print_mark_package_immutable_success,
        "failure_function": print_mark_package_immutable_failure,
    },
}


def _read_docopt_args() -> dict:
    return docopt(__doc__, argv=None, help=True, version=None, options_first=False)


def _map_arguments_to_apt_utils(arguments: dict) -> tuple:
    package_name, package_version = arguments["<package_name>"], arguments.get(
        "<package_version>"
    )

    for key, func_d in APT_UTILS_ARGUMENTS_MAP.items():
        if arguments[key] is True:
            return func_d, {
                "package_name": package_name,
                "package_version": package_version,
            }

    raise Exception("Unsupported CLI arguments {arguments!s}")


def _add_indent(s: str) -> str:
    return "   " + s


def _butify_apt_pkg_error_msg(error_msg: str) -> str:
    beautiful_msg = error_msg.split("E:")
    beautiful_msg = "\n".join(_add_indent(msg) for msg in beautiful_msg)

    return beautiful_msg


def _butify_app_error_message(error_msg: str) -> str:
    beautiful_msg = "\n" + _add_indent(error_msg.replace(".", ""))

    return beautiful_msg


if __name__ == "__main__":
    arguments = _read_docopt_args()

    apt_utils_funcs, apt_utils_arguments = _map_arguments_to_apt_utils(arguments)

    try:
        result = apt_utils_funcs["function"](**apt_utils_arguments)
    except AptPkgError as err:
        apt_utils_funcs["failure_function"](
            **apt_utils_arguments, error=_butify_apt_pkg_error_msg(str(err))
        )
    except tuple(apt_utils_funcs["exceptions"]) as err:
        apt_utils_funcs["failure_function"](
            **apt_utils_arguments, error=_butify_app_error_message(str(err))
        )
    else:
        apt_utils_funcs["success_function"](**apt_utils_arguments, result=result)
