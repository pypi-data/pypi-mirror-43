"""This module defines custom implementation of ``sdist`` setuptools command."""

import os

from distutils import log as distutils_log
from distutils.command.sdist import sdist as _sdist

from . import set_build_base_mixin
from ..utils import distribution_hide_listing, new_style


class sdist(set_build_base_mixin, new_style(_sdist)):
    """Custom implementation of ``sdist`` setuptools command."""

    def make_release_tree(self, base_dir, files):
        """Handle --hide-listing option."""
        with distribution_hide_listing(self.distribution):
            super(sdist, self).make_release_tree(base_dir, files)
        distutils_log.info("%s %d files" % (
            "hard-linked" if hasattr(os, 'link') else "copied", len(files)))

    # pylint:disable=too-many-arguments, unused-argument
    def make_archive(self, base_name, _format, root_dir=None, base_dir=None,
                     owner=None, group=None):
        """Handle --hide-listing option."""
        distutils_log.info("creating '%s' %s archive and adding '%s' to it",
                           base_name, _format, base_dir)
        with distribution_hide_listing(self.distribution):
            super(sdist, self).make_archive(
                base_name, _format, root_dir, base_dir)

    def run(self, *args, **kwargs):
        """Force :class:`.egg_info.egg_info` command to run."""
        self.run_command('generate_source_manifest')
        super(sdist, self).run(*args, **kwargs)
