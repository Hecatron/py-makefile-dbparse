'''
Run tests for the Makefile wrapper class
'''

import os
import pytest
from py_makefile_dbparse.makefile import MakeFile


def test_init():
    '''Check class init'''
    srcdir = os.path.abspath('tests/make_src')
    mk1 = MakeFile(srcdir)
    mk1.read_all()

    srcfile = os.path.abspath('tests/make_src/Makefile')
    mk2 = MakeFile(srcfile)
    mk2.read_all()
