"""
This module defines constants commonly used in scikit-build.
"""

import os
import sys

from distutils.util import get_platform

CMAKE_DEFAULT_EXECUTABLE = "cmake"
"""Default path to CMake executable."""

_SKBUILD_PLAT_NAME = get_platform()


def set_skbuild_plat_name(plat_name):
    """Set platform name associated with scikit-build functions returning a path:

    * :func:`SKBUILD_DIR()`
    * :func:`SKBUILD_MARKER_FILE()`
    * :func:`CMAKE_BUILD_DIR()`
    * :func:`CMAKE_INSTALL_DIR()`
    * :func:`CMAKE_SPEC_FILE()`
    * :func:`SETUPTOOLS_INSTALL_DIR()`
    """
    global _SKBUILD_PLAT_NAME
    _SKBUILD_PLAT_NAME = plat_name


def skbuild_plat_name():
    """Get platform name.

    Default value corresponds to :func:`distutils.util.get_platform()` and can be overridden
    with :func:`set_skbuild_plat_name()`.
    """
    return _SKBUILD_PLAT_NAME


def SKBUILD_DIR():
    """Top-level directory where setuptools and CMake directories are generated."""
    return os.path.join(
        "_skbuild",
        "{}-{}".format(_SKBUILD_PLAT_NAME, '.'.join(map(str, sys.version_info[:2]))),
    )


def SKBUILD_MARKER_FILE():
    """Marker file used by :func:`skbuild.command.generate_source_manifest.generate_source_manifest.run()`."""
    return os.path.join(SKBUILD_DIR(), "_skbuild_MANIFEST")


def CMAKE_BUILD_DIR():
    """CMake build directory."""
    return os.path.join(SKBUILD_DIR(), "cmake-build")


def CMAKE_INSTALL_DIR():
    """CMake install directory."""
    return os.path.join(SKBUILD_DIR(), "cmake-install")


def CMAKE_SPEC_FILE():
    """CMake specification file storing CMake version, CMake configuration arguments and
    environment variables ``PYTHONNOUSERSITE`` and ``PYTHONPATH``.
    """
    return os.path.join(CMAKE_BUILD_DIR(), "CMakeSpec.json")


def SETUPTOOLS_INSTALL_DIR():
    """Setuptools install directory."""
    return os.path.join(SKBUILD_DIR(), "setuptools")
