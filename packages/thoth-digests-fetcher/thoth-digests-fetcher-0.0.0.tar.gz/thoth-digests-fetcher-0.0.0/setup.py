import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


def get_install_requires():
    with open('requirements.txt', 'r') as requirements_file:
        res = requirements_file.readlines()
        return [req.split(' ', maxsplit=1)[0] for req in res if req]


def get_version():
    with open(os.path.join('thoth', 'digests_fetcher', '__init__.py')) as f:
        content = f.readlines()

    for line in content:
        if line.startswith('__version__ ='):
            # dirty, remove trailing and leading chars
            return line.split(' = ')[1][1:-2]
    raise ValueError("No version identifier found")


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


class Test(TestCommand):
    user_options = [
        ('pytest-args=', 'a', "Arguments to pass into py.test")
    ]

    def initialize_options(self):
        super().initialize_options()
        self.pytest_args = ['tests/', '--timeout=2', '--cov=./thoth', '--capture=no', '--verbose', '-l', '-s']

    def finalize_options(self):
        super().finalize_options()
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.pytest_args))


setup(
    name='thoth-digests-fetcher',
    version=get_version(),
    description='Gather digests for artifacts in Python ecosystem.',
    long_description=read('README.rst'),
    author='Fridolin Pokorny',
    author_email='fridolin@redhat.com',
    license='GPLv3+',
    packages=['thoth.digests_fetcher', 'thoth.digests_fetcher.python'],
    entry_points={
        'console_scripts': ['thoth-digests-fetcher=thoth.digests_fetcher.cli:cli']
    },
    zip_safe=False,
    install_requires=get_install_requires(),
    cmdclass={'test': Test},
)
