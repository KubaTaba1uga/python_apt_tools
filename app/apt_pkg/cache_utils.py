import apt_pkg as pkg

from apt.progress.base import InstallProgress


def commit_cache(cache: pkg.Cache):
    dep_cache = pkg.DepCache(cache)
    acquire_progress, install_progress = (pkg.Acquire(), InstallProgress())

    dep_cache.commit(acquire_progress, install_progress)
