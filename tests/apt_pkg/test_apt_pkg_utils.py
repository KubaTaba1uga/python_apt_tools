import pytest

import apt_pkg as pkg

from app.apt_pkg.apt_pkg_utils import find_package


@pytest.mark.parametrize(
    "pkg_name, expected_type",
    [("dpkg", pkg.Package), ("non-exsisting-package99", type(None))],
)
def test_find_package_apt_pkg_no_ver(pkg_name, expected_type):
    os_package = find_package(pkg_name)

    assert isinstance(os_package, expected_type) is True


@pytest.mark.parametrize(
    "pkg_name, pkg_ver, expected_type",
    [
        ("dpkg", "1.20.12", pkg.Package),
        ("non-exsisting-package99", "1.1.1", type(None)),
    ],
)
def test_find_package_apt_pkg_ver(pkg_name, pkg_ver, expected_type):
    os_package = find_package(pkg_name, pkg_ver)

    assert isinstance(os_package, expected_type) is True
