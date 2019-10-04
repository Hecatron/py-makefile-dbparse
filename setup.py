'''Setup file'''

# TODO
# 1. depends

import os
from setuptools import setup
from codecs import open  # To use a consistent encoding
from os import path
from pypandoc import convert

def get_long_description(package):
    try:
        readme = convert('Readme.md', 'rst', format='markdown_github')
        change_log = convert('Changelog.md', 'rst', format='markdown_github')
        long_description = readme + '\n\n' + change_log
    except:
        currentdir = path.abspath(path.dirname(__file__))
        with open(path.join(currentdir, 'Readme.md'), encoding='utf-8') as f:
            long_description = f.read()
    return long_description

def get_version(package):
    '''Return package version as listed in `__version__` in `init.py`.'''
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

def get_packages(package):
    '''Return root package and all sub-packages.'''
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]

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
    print("  git tag -a {0} -m 'version {0}'".format(get_version('py_makefile_dbparse')))
    print("  git push --tags")
    sys.exit()

setup(
    name='py-makefile-dbparse',
    version=get_version('py_makefile_dbparse'),
    url='http://Hecatron.github.io/py-makefile-dbparse',
    license='MIT License',
    description='Tool for extracting information from Makefiles for use with python build systems.',
    long_description=get_long_description('py_makefile_dbparse'),
    author='hecatrons.workshop@gmail.com',
    author_email='hecatrons.workshop@gmail.com',
    packages=get_packages('py_makefile_dbparse'),
    include_package_data=True,
    install_requires=[
        "mkdocs>=0.16.3",
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
    ],
    tests_require=[
        'pytest-cov',
        'pytest-pycodestyle',
        'pytest-runner',
        'pytest-colordots',
    ],
)
