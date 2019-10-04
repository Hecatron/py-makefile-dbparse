'''
Represents a Makefile database
'''

import re
import sys
import os.path as path
from py_makefile_dbparse.launcher import MakeLauncher
from py_makefile_dbparse.target import MakeTarget
from py_makefile_dbparse.vars import MakeVarList


class MakeFile(object):
    '''Represents a Makefile database

    Attributes:
        makefile_path: The path to the Makefile (file or directory).
        launcher: The launcher used for running make.
        dbtxt: The result of a dump of the Makefile database as text.
        targets: A list of Makefile targets.
        vars: A collection of variables within the makefile.
    '''

    def __init__(self, makefile_path):
        '''Class initialiser.
        Args:
            makefile_path: The path to the Makefile (file or directory).
        '''
        self.makefile_path = makefile_path
        self.launcher = None
        if path.isdir(makefile_path):
            # If the path is a directory then assume the makefile is called "Makefile"
            # Pass in the directory
            self.launcher = MakeLauncher(workdir=makefile_path)
        else:
            # If the path is a file then extract the directory / filename and pass this in
            workdir = path.dirname(makefile_path)
            makefilename = path.basename(makefile_path)
            self.launcher = MakeLauncher(workdir=workdir, makefile=makefilename)
        self.dbtxt = ''
        self.targets = []
        self.vars = MakeVarList(launcher=self.launcher)

    def read_db(self):
        '''Read in the Makefile database as text.
        Returns:
            The Makefile database as text.'''
        self.dbtxt = self.launcher.run('-pn')
        return self.dbtxt

    def dump_db(self, filepath):
        '''Write the Makefile database output as a text file
        Args:
            filepath: The path to the file to write to.
        '''
        with open(filepath, 'w', encoding='utf-8') as outfile:
            outfile.write(self.dbtxt)

    def parse_targets(self):
        '''Generate a list of all targets defined in the make process
        Returns:
            The targets parsed from the Makefile database.'''
        self.targets = MakeTarget.parse_targets(self.dbtxt, self.vars)
        return self.targets

    def parse_vars(self):
        '''Generate the (key,value) dict of all variables defined in the make process.
        Returns:
            The (key,value) dict of all variables defined in the make process.'''
        self.vars.parse_vars(self.dbtxt)
        return self.vars

    def read_all(self):
        '''Read / Parse all from the Makefile database'''
        self.read_db()
        self.parse_vars()
        self.parse_targets()
