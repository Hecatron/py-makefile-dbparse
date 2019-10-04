'''
Run tests for the Make launcher
'''

import os
import pytest
from py_makefile_dbparse.launcher import MakeLauncher

mktxt_compare = 'IDIR =include\nCC=gcc\nCFLAGS=-I$(IDIR)\n\nODIR=../build\nLDIR =../build/lib\n\nLIBS=-lm\n\n_DEPS = hellomake.h\nDEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))\n\n_OBJ = hellomake.o hellofunc.o \nOBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))\n\n\n$(ODIR)/%.o: %.c $(DEPS)\n\t$(CC) -c -o $@ $< $(CFLAGS)\n\n$(ODIR)/hellomake: $(OBJ)\n\t$(CC) -o $@ $^ $(CFLAGS) $(LIBS)\n\n.PHONY: clean\n\nclean:\n\trm -f $(ODIR)/*.exe $(ODIR)/*.o *~ core $(INCDIR)/*~\n\ninfo:\n\t$(info OBJ=$(OBJ))\n\t$(info OBJ=$(OBJ))\n'


def test_init():
    '''Check class init'''
    launcher1 = MakeLauncher(cmd='make2', opts='-v', makefile='Makefile2', workdir='.')
    assert launcher1.cmd == 'make2'
    assert launcher1.opts == '-v'
    assert launcher1.makefile == 'Makefile2'
    assert launcher1.workdir == '.'
    assert launcher1.stdout == ''
    assert launcher1.stderr == ''


def test_readmakefile():
    '''Read in a makefile and check it matches the hard coded value'''
    srcdir = os.path.abspath('tests/make_src')
    launcher1 = MakeLauncher(workdir=srcdir)
    mktxt = launcher1.read_makefile()
    assert mktxt_compare == mktxt


def test_writemakefile():
    '''Try reading / writing a makefile'''
    # Read in the makefile
    srcdir = os.path.abspath('tests/make_src')
    launcher1 = MakeLauncher(workdir=srcdir)
    mktxt = launcher1.read_makefile()
    # Write out the makefile
    outdir = os.path.abspath('tests/build-temp')
    launcher2 = MakeLauncher(workdir=outdir)
    launcher2.write_makefile(mktxt)
    # Re-read the written makefile
    mktxt2 = launcher2.read_makefile()
    # Check everything matches up
    assert mktxt_compare == mktxt2


def test_run():
    '''Test launching make'''
    srcdir = os.path.abspath('tests/make_src')
    launcher1 = MakeLauncher(workdir=srcdir)
    # Launch make with --version just to check we're getting a output / returned value
    stdout = launcher1.run('--version')
    assert launcher1.stdout == stdout
    splitlines = stdout.splitlines()
    assert splitlines[0].startswith('GNU Make')
