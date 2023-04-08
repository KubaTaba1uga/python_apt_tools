import pytest

import apt_pkg as pkg


@pytest.fixture
def apt_pkg():
    pkg.init_config()
    pkg.init_system()
    return pkg
