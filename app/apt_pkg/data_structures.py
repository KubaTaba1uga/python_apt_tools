import apt_pkg

# Each package has it's INSTALLATION STATUS represented as int.
# The status the currently installed version is in.
# This map is usefull to recognize what number means in real.
INSTALLATION_STATUS_MAP = {
    "The package is put on hold.": apt_pkg.INSTSTATE_HOLD,
    "The package is put on hold, but broken and has to be reinstalled.": apt_pkg.INSTSTATE_HOLD_REINSTREQ,
    "The package is ok.": apt_pkg.INSTSTATE_OK,
    "The poackage is broken and has to be reinstalled.": apt_pkg.INSTSTATE_REINSTREQ,
}

# Each package has it's SELECTION STATUS represented as int.
# The status we want it to be.
# This map is usefull to recognize what number means in real.
SELECTION_STATUS_MAP = {
    "The package in selected for deinstallation.": apt_pkg.SELSTATE_DEINSTALL,
    "The package is marked to be on hold and will not be modified.": apt_pkg.SELSTATE_HOLD,
    "The package is selected for installation.": apt_pkg.SELSTATE_INSTALL,
    "The package is selected to be purged.": apt_pkg.SELSTATE_PURGE,
    "The package is in an unknown state": apt_pkg.SELSTATE_UNKNOWN,
}
