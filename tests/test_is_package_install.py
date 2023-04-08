from unittest.mock import patch

import pytest

from app.apt_utils import is_package_installed


@pytest.mark.parametrize(
    "pkg_name, expected", [("dpkg", True), ("non-exsisting-package99", False)]
)
def test_is_package_installed_no_ver(apt_pkg, pkg_name, expected):
    received = is_package_installed(apt_pkg, pkg_name)

    assert received == expected


@pytest.mark.parametrize(
    "pkg_name, pkg_ver, expected",
    [("dpkg", "1.20.12", True), ("non-exsisting-package99", "1.1.1", False)],
)
@patch("app.apt_utils.cmp_versions", lambda _, __: True)
def test_is_package_installed_ver(apt_pkg, pkg_name, pkg_ver, expected):
    received = is_package_installed(apt_pkg, pkg_name, pkg_ver)

    assert received == expected
