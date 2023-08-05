#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""test_hello_pure
----------------------------------

Tries to build and test the `hello-pure` sample project.
"""

import glob
import tarfile

from skbuild.constants import SKBUILD_DIR
from skbuild.utils import push_dir

from zipfile import ZipFile

from . import check_wheel_content, project_setup_py_test


@project_setup_py_test("hello-pure", ["build"], disable_languages_test=True)
def test_hello_pure_builds(capsys):
    out, _ = capsys.readouterr()
    assert "skipping skbuild (no CMakeLists.txt found)" in out


# @project_setup_py_test("hello-pure", ["test"])
# def test_hello_cython_works():
#     pass


@project_setup_py_test("hello-pure", ["sdist"], disable_languages_test=True)
def test_hello_pure_sdist():
    sdists_tar = glob.glob('dist/*.tar.gz')
    sdists_zip = glob.glob('dist/*.zip')
    assert sdists_tar or sdists_zip

    member_list = None
    expected_content = None
    if sdists_tar:
        expected_content = [
            'hello-pure-1.2.3',
            'hello-pure-1.2.3/hello',
            'hello-pure-1.2.3/hello/__init__.py',
            'hello-pure-1.2.3/setup.py',
            'hello-pure-1.2.3/PKG-INFO'
        ]
        member_list = tarfile.open('dist/hello-pure-1.2.3.tar.gz').getnames()

    elif sdists_zip:
        expected_content = [
            'hello-pure-1.2.3/hello/__init__.py',
            'hello-pure-1.2.3/setup.py',
            'hello-pure-1.2.3/PKG-INFO'
        ]
        member_list = ZipFile('dist/hello-pure-1.2.3.zip').namelist()

    assert expected_content and member_list
    assert sorted(expected_content) == sorted(member_list)


@project_setup_py_test("hello-pure", ["bdist_wheel"], disable_languages_test=True)
def test_hello_pure_wheel():
    expected_content = [
        'hello/__init__.py'
    ]

    expected_distribution_name = 'hello_pure-1.2.3'

    whls = glob.glob('dist/*.whl')
    assert len(whls) == 1
    check_wheel_content(whls[0], expected_distribution_name, expected_content, pure=True)


def test_hello_clean(capfd):
    with push_dir():

        @project_setup_py_test("hello-pure", ["build"], disable_languages_test=True)
        def run_build():
            pass

        tmp_dir = run_build()[0]

        assert tmp_dir.join(SKBUILD_DIR()).exists()

        @project_setup_py_test("hello-pure", ["clean"], tmp_dir=tmp_dir, disable_languages_test=True)
        def run_clean():
            pass

        run_clean()

        assert not tmp_dir.join(SKBUILD_DIR()).exists()

        out = capfd.readouterr()[0]
        assert 'Build files have been written to' not in out
