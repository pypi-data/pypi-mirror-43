#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Taken from https://github.com/kennethreitz/setup.py under MIT licence

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command
from setuptools.command.test import test as TestCommand

NAME = 'stacksplit'
DESCRIPTION = 'A simple Python library to generate all combinations of possible splits for a stack with given height.'
URL = 'https://gitlab.com/felixwallner/stacksplit'
EMAIL = 'felix.wallner@protonmail.com'
AUTHOR = 'Felix Wallner'
REQUIRES_PYTHON = '>=3.4.0'
VERSION = None  # Use the __version__.py file to handle version

REQUIRED = [
    # none
]

EXTRAS = {
    # none
}

# ------------------------------------------------

here = os.path.abspath(os.path.dirname(__file__))
project_slug = NAME.lower().replace("-", "_").replace(" ", "_")

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    if type(VERSION) in [str]:
        about['__version__'] = VERSION
    elif type(VERSION) in [list, tuple]:
        about['__version__'] = '.'.join(map(str, VERSION))
    else:
        raise ValueError('Version must be a tuple or a string.')


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package with twine.'
    user_options = [
        ('test', 't', 'deploay to test.pypi.org instead'),
    ]

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        self.test = 0

    def finalize_options(self):
        pass

    def run(self):
        self.status('Checking for git tags')
        if os.system('git tag -l --points-at=HEAD > /tmp/stacksplit_git_tags') != 0:
            print('Git lookup failed. Is git installed?', file=sys.stderr)
            sys.exit(-1)

        with open('/tmp/stacksplit_git_tags', 'r') as f:
            tags = f.read()

        if tags.find(about['__version__']) < 0:
            self.status('The version {0} is not tagged to this commit. (Tags are: {1}) Please tag before uploading'.format(about['__version__'], tags))
            exit(-1)

        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        if self.test:
            self.status('Uploading the package to TEST PyPI (Legacy) via Twine…')
            if os.system('twine upload --verbose --repository-url https://test.pypi.org/legacy/ dist/*') != 0:
                print('Twine upload failed. Is twine installed?', file=sys.stderr)
                sys.exit(-1)
        else:
            self.status('Uploading the package to PyPI via Twine…')
            if os.system('twine upload --verbose dist/*') != 0:
                print('Twine upload failed. Is twine installed?', file=sys.stderr)
                sys.exit(-1)

        sys.exit()


class PyTest(TestCommand):
    """Support setup.py test."""

    # description = 'Execute all tests with pytest.'
    user_options = [
        ('all', 'a', 'run all with additional options'),
        ('coverage', 'c', 'run tests with coverage'),
        ('doctest', 'd', 'run tests with doctests'),
        ('flake8', 'f', 'run tests with flake8'),
    ]

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        TestCommand.initialize_options(self)
        try:
            from multiprocessing import cpu_count
            self.pytest_args = ['-n', str(cpu_count()), '--boxed']
        except (ImportError, NotImplementedError):
            self.pytest_args = ['-n', '1', '--boxed']

        self.all = 0

        self.coverage = 0
        self.doctest = 0
        self.flake8 = 0

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

        # set all other options if all is set
        if self.all:
            self.coverage = 1
            self.doctest = 1
            self.flake8 = 1

        # init commandline options
        if self.coverage:
            self.pytest_args.append('--cov={}'.format(project_slug))
            self.pytest_args.append('--cov-fail-under={}'.format(90))

        if self.doctest:
            self.pytest_args.append('--doctest-modules')

        if self.flake8:
            self.pytest_args.append('--flake8')
            # options for flake8 set in tox.ini
        # finished init options

    def run(self):
        import pytest
        self.status("Running pytest {}".format(' '.join(self.pytest_args)))
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords=[
        'stack',
        'split',
        'partition',
        'combinations',
        'NIM',
        'Laskers-NIM',
        'gametheorie',
        'coins',
        'sum',
    ],
    cmdclass={
        'twineup': UploadCommand,
        'test': PyTest,
    },
)
