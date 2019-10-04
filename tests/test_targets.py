'''
Run tests for the Makefile targets
'''

import os
import pytest
from py_makefile_dbparse.makefile import MakeFile
from py_makefile_dbparse.target import MakeTarget


def test_init():
    '''Check class init'''
    tgt1 = MakeTarget('')
    assert tgt1.src_txtlist == ''
    assert tgt1.target == ''
    assert tgt1.sources == []
    assert tgt1.cmds_raw == []
    assert tgt1._varlist is None


def test_targets():
    '''Checks target property'''
    srcdir = os.path.abspath('tests/make_src')
    mk1 = MakeFile(srcdir)
    mk1.read_all()
    # Test the target names
    assert mk1.targets[0].target == '../build/hellomake'
    assert mk1.targets[1].target == '../build/hellomake.o'
    assert mk1.targets[2].target == 'info'
    assert mk1.targets[3].target == '../build/hellofunc.o'
    assert mk1.targets[4].target == 'clean'


def test_target_noext():
    '''Checks target_noext property'''
    srcdir = os.path.abspath('tests/make_src')
    mk1 = MakeFile(srcdir)
    mk1.read_all()
    assert mk1.targets[1].target_noext == '../build/hellomake'


def test_sources():
    '''Checks sources property'''
    srcdir = os.path.abspath('tests/make_src')
    mk1 = MakeFile(srcdir)
    mk1.read_all()
    assert mk1.targets[0].sources == ['../build/hellomake.o', '../build/hellofunc.o']


def test_sources_noheader():
    '''Checks sources_noheader property'''
    srcdir = os.path.abspath('tests/make_src')
    mk1 = MakeFile(srcdir)
    mk1.read_all()
    assert mk1.targets[1].sources_noheader == ['hellomake.c']


def test_sources_noext():
    '''Checks sources_noext property'''
    srcdir = os.path.abspath('tests/make_src')
    mk1 = MakeFile(srcdir)
    mk1.read_all()
    assert mk1.targets[0].sources_noext == ['../build/hellomake', '../build/hellofunc']


def test_cmds_expand():
    '''Checks cmds_expand property'''
    srcdir = os.path.abspath('tests/make_src')
    mk1 = MakeFile(srcdir)
    mk1.read_all()
    cmds_raw = mk1.targets[0].cmds_raw
    cmds_exp = mk1.targets[0].cmds_expand()
    assert cmds_exp[0] == 'gcc -o ../build/hellomake ../build/hellomake.o ../build/hellofunc.o -Iinclude -lm'


def test_cmds_expand_usemake():
    '''Checks cmds_expand property'''
    srcdir = os.path.abspath('tests/make_src')
    mk1 = MakeFile(srcdir)
    mk1.read_all()
    cmds_raw = mk1.targets[0].cmds_raw
    cmds_exp = mk1.targets[0].cmds_expand(usemake=True)
    assert cmds_exp[0] == 'gcc -o ../build/hellomake ../build/hellomake.o ../build/hellofunc.o -Iinclude -lm'
