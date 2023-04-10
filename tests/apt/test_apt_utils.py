from unittest.mock import patch

import pytest

import apt

from app.apt.apt_utils import is_package_installed
from app.apt.apt_utils import find_package
from app.apt.apt_utils import install_package
from app.errors import PackageNotFoundError


@pytest.mark.parametrize(
    "pkg_name, expected", [("dpkg", True), ("non-exsisting-package99", False)]
)
def test_is_package_installed_no_ver(pkg_name, expected):
    received = is_package_installed(pkg_name)

    assert received == expected


@pytest.mark.parametrize(
    "pkg_name, pkg_ver, expected",
    [("dpkg", "1.20.12", True), ("non-exsisting-package99", "1.1.1", False)],
)
@patch("app.apt.apt_utils.cmp_versions", lambda _, __: True)
def test_is_package_installed_ver(pkg_name, pkg_ver, expected):
    received = is_package_installed(pkg_name, pkg_ver)

    assert received == expected


@pytest.mark.parametrize(
    "pkg_name, expected_type",
    [("dpkg", apt.Package), ("non-exsisting-package99", type(None))],
)
def test_find_package_no_ver(pkg_name, expected_type):
    os_package = find_package(pkg_name)

    assert isinstance(os_package, expected_type) is True


@pytest.mark.parametrize(
    "pkg_name, pkg_ver, expected_type",
    [
        ("dpkg", "1.20.12", apt.Package),
        ("non-exsisting-package99", "1.1.1", type(None)),
    ],
)
def test_find_package_ver(pkg_name, pkg_ver, expected_type):
    os_package = find_package(pkg_name, pkg_ver)

    assert isinstance(os_package, expected_type) is True


@pytest.mark.parametrize(
    "pkg_name",
    [("dpkg")],
)
def test_install_package_exsists(pkg_name):
    with patch("app.apt.apt_utils.mark_install") as mark_install:
        with patch("app.apt.apt_utils.commit_changes") as commit_changes:
            install_package(pkg_name)

    assert mark_install.call_count == 1
    assert commit_changes.call_count == 1


@pytest.mark.parametrize(
    "pkg_name",
    [
        ("non-exsisting-package99"),
    ],
)
def test_install_package_not_exsists(pkg_name):
    with pytest.raises(PackageNotFoundError):
        install_package(pkg_name)
