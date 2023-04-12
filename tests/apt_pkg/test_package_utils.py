from unittest.mock import patch, MagicMock

import pytest

from app.apt_pkg.package_utils import describe_package_selection_status

from apt_pkg import (
    SELSTATE_DEINSTALL,
    SELSTATE_HOLD,
    SELSTATE_INSTALL,
    SELSTATE_PURGE,
    SELSTATE_UNKNOWN,
)


@pytest.mark.parametrize(
    "status, expected_description",
    [
        (SELSTATE_DEINSTALL, "The package in selected for deinstallation."),
        (
            SELSTATE_HOLD,
            "The package is marked to be on hold and will not be modified.",
        ),
        (SELSTATE_INSTALL, "The package is selected for installation."),
        (SELSTATE_PURGE, "The package is selected to be purged."),
        (SELSTATE_UNKNOWN, "The package is in an unknown state"),
    ],
)
def test_describe_package_selection_status_known(status, expected_description):
    with patch("app.apt_pkg.package_utils._get_selection_status", return_value=status):
        received_description = describe_package_selection_status(object)

    assert received_description == expected_description


def test_describe_package_selection_status_unknown():
    non_exsisting_status_int, non_exsisting_obj_name = 696969696969696, "My obj"

    with patch(
        "app.apt_pkg.package_utils._get_selection_status",
        return_value=non_exsisting_status_int,
    ):

        with patch(
            "app.apt_pkg.package_utils._get_name",
            return_value=non_exsisting_obj_name,
        ):

            with pytest.raises(ValueError):
                describe_package_selection_status(object)
