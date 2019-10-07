'''
Run tests for the Make Vars
'''

import os
import pytest
from py_makefile_dbparse.vars import MakeVarList
from py_makefile_dbparse.makefile import MakeFile


def test_init():
    '''Check class init'''
    vars1 = MakeVarList()
    assert vars1.values == []
    assert vars1.origin == ['environment', 'makefile']


def test_parse_vars():
    '''Check the parsing of variables'''
    # First extract the make database
    srcdir = os.path.abspath('tests/make_src')
    mk1 = MakeFile(srcdir)
    mk1.read_db()
    # Next lets parse some varaibles from the database text
    mk1.parse_vars()
    mkvars = mk1.vars.values['makefile']
    # Lets check some values against the Makefile in the test directory
    assert mkvars['CC'] == 'gcc'
    assert mkvars['CFLAGS'] == '-I$(IDIR)'
    assert mkvars['DEPS'] == '$(patsubst %,$(IDIR)/%,$(_DEPS))'
    assert mkvars['IDIR'] == 'include'
    assert mkvars['LDIR'] == '../build/lib'
    assert mkvars['LIBS'] == '-lm'
    assert mkvars['MAKEFILE_LIST'] == 'makefile'
    assert mkvars['MAKEFLAGS'] == 'wpn'
    assert mkvars['OBJ'] == '$(patsubst %,$(ODIR)/%,$(_OBJ))'
    assert mkvars['ODIR'] == '../build'
    assert mkvars['_DEPS'] == 'hellomake.h'
    assert mkvars['_OBJ'] == 'hellomake.o hellofunc.o'


def test_expand_var():
    '''Check the Expansion of variables locally'''
    # First extract the make database
    srcdir = os.path.abspath('tests/make_src')
    mk1 = MakeFile(srcdir)
    mk1.read_db()
    # Next lets try some local expansion
    # this will handle variable substitution but not make functions, but is quicker
    mk1.parse_vars()
    test1 = mk1.vars.expand_var(['CFLAGS', 'LIBS'])
    assert test1['CFLAGS'] == '-Iinclude'
    assert test1['LIBS'] == '-lm'
    test2 = mk1.vars.expand_var('CFLAGS')
    assert test2 == '-Iinclude'


def test_expand_expr():
    '''Check the Expansion of expressions locally'''
    # First extract the make database
    srcdir = os.path.abspath('tests/make_src')
    mk1 = MakeFile(srcdir)
    mk1.read_db()
    # Next lets try some local expressions
    # this will handle variable substitution but not make functions, but is quicker
    mk1.parse_vars()
    test1 = mk1.vars.expand_expr(['$(CFLAGS)', '$(CFLAGS) $(LIBS)'])
    assert test1[0] == '-Iinclude'
    assert test1[1] == '-Iinclude -lm'
    test2 = mk1.vars.expand_expr('$(CFLAGS) $(LIBS)')
    assert test2[0] == '-Iinclude -lm'


def test_expand_var_usemake():
    '''Check the Expansion of variables using make'''
    # First extract the make database
    srcdir = os.path.abspath('tests/make_src')
    mk1 = MakeFile(srcdir)
    mk1.read_db()
    # Next lets try expanding some variables using make
    mk1.parse_vars()
    test1 = mk1.vars.expand_var(['DEPS', 'CFLAGS'], usemake=True)
    assert test1['DEPS'] == 'include/hellomake.h'
    assert test1['CFLAGS'] == '-Iinclude'
    test2 = mk1.vars.expand_var('DEPS', usemake=True)
    assert test2 == 'include/hellomake.h'


def test_expand_expr_usemake():
    '''Check the Expansion of expressions using make'''
    # First extract the make database
    srcdir = os.path.abspath('tests/make_src')
    mk1 = MakeFile(srcdir)
    mk1.read_db()
    # Next lets try expanding some expressions using make
    mk1.parse_vars()
    test1 = mk1.vars.expand_expr(['$(DEPS)', '$(CFLAGS) $(DEPS)'], usemake=True)
    assert test1[0] == 'include/hellomake.h'
    assert test1[1] == '-Iinclude include/hellomake.h'
    test2 = mk1.vars.expand_expr('$(DEPS)', usemake=True)
    assert test2[0] == 'include/hellomake.h'
