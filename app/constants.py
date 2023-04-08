import apt_pkg

PACKAGE_STATUS_MAP = {
    "Only the configuration files of the package exist on the system.": apt_pkg.CURSTATE_CONFIG_FILES,
    "The package is unpacked and configuration has been started, but not yet completed.": apt_pkg.CURSTATE_HALF_CONFIGURED,
    "The installation of the package has been started, but not completed.": apt_pkg.CURSTATE_HALF_INSTALLED,
    (
        PACKAGE_INSTALLED_STATUS := "The package is installed, configured and OK."
    ): apt_pkg.CURSTATE_INSTALLED,
    "The package is not installed.": apt_pkg.CURSTATE_NOT_INSTALLED,
    "The package is unpacked, but not configured.": apt_pkg.CURSTATE_UNPACKED,
}
