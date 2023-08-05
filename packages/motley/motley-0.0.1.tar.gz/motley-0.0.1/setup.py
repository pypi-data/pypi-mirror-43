#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2019 Frootlab Developers
#
# This file is part of Motley, https://github.com/frootlab/motley
#
#  Motley is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Motley is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
#  A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License along with
#  Motley. If not, see <http://www.gnu.org/licenses/>.
#
"""Setuptools based installation."""

__license__ = 'GPLv3'
__copyright__ = 'Copyright (C) 2019 Frootlab Developers'
__email__ = 'frootlab@gmail.com'
__docformat__ = 'google'
__authors__ = ['Patrick Michl <patrick.michl@gmail.com>']

import pathlib
import re
import setuptools

def install() -> None:
    """Setuptools based installation script."""

    # Get module variables from the package's top level module
    text = pathlib.Path('./motley/__init__.py').read_text()
    rekey = "__([a-zA-Z][a-zA-Z0-9_]*)__"
    reval = r"['\"]([^'\"]*)['\"]"
    pattern = f"^[ ]*{rekey}[ ]*=[ ]*{reval}"
    pkg_vars = {}
    for mo in re.finditer(pattern, text, re.M):
        pkg_vars[str(mo.group(1))] = str(mo.group(2))

    # Install package
    setuptools.setup(
        name='motley',
        version=pkg_vars['version'],
        description='motley code catalog',
        long_description=pathlib.Path('.', 'README.rst').read_text(),
        long_description_content_type='text/x-rst',
        classifiers=[
            'Development Status :: 1 - Planning',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Programming Language :: Python :: 3',
    		'Programming Language :: Python :: 3.7',
            'Operating System :: OS Independent',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            'Topic :: Software Development :: Libraries :: Python Modules'],
        keywords=(
            'catalog '
            'catalog-software '),
        url='https://github.com/frootlab/motley',
        author=pkg_vars['author'],
        author_email=pkg_vars['email'],
        license=pkg_vars['license'],
        packages=setuptools.find_packages(exclude=['docs', 'tests']),
        package_dir={
            'motley': 'motley'},
        python_requires='>=3.7',
        install_requires=[
            'numpy>=1.15',
            'flib>=0.9',
            'pandb>=0.1.8',
            'nemoa>=0.5.581']
    )

if __name__ == '__main__':
    install()
