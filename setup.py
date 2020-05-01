'''Setup file'''

import os
import sys
import re
from setuptools import setup
from codecs import open
from os import path
from pypandoc import convert_file

package_name = 'py_makefile_dbparse'
package_name_dash = 'py-makefile-dbparse'


def get_long_description(package):
    try:
        readme = convert_file('Readme.md', 'rst', format='markdown_github')
        change_log = convert_file('Changelog.md', 'rst', format='markdown_github')
        long_description = readme + '\n\n' + change_log
    except:
        currentdir = path.abspath(path.dirname(__file__))
        with open(path.join(currentdir, 'Readme.md'), encoding='utf-8') as f:
            long_description = f.read()
    return long_description


def get_version(package):
    '''Return package version as listed in `__version__` in `init.py`.'''
    init_py = open(path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    '''Return root package and all sub-packages.'''
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if path.exists(path.join(dirpath, '__init__.py'))]


if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep wheel"):
        print("wheel not installed.\nUse `pip install wheel`.\nExiting.")
        sys.exit()
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    print("  git tag -a {0} -m 'version {0}'".format(get_version(package_name)))
    print("  git push --tags")
    sys.exit()

setup(
    name=package_name_dash,
    version=get_version(package_name),
    url='http://Hecatron.github.io/' + package_name_dash,
    license='MIT License',
    description='Tool for extracting information from Makefiles for use with python build systems.',
    long_description=get_long_description(package_name),
    author='hecatrons.workshop@gmail.com',
    author_email='hecatrons.workshop@gmail.com',
    packages=get_packages(package_name),
    include_package_data=True,
    install_requires=[
        "py-linq>=1.0.1",
    ],
    python_requires='>=3.0.0,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    classifiers=[
        #   3 - Alpha, 4 - Beta, 5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        'Topic :: Documentation',
        'Topic :: Text Processing',
    ],
    zip_safe=False,
    keywords="pip package, scons, makefile, make",
    setup_requires=[
        'pytest-runner',
        'pypandoc'
    ],
    tests_require=[
        'pytest-cov',
        'pytest-pycodestyle',
        'pytest-runner',
        'pytest-colordots',
    ],
)
