'''
A class that represents a Make target
'''

# https://www.gnu.org/software/make/manual/html_node/Automatic-Variables.html

import os
from py_linq import Enumerable


class MakeTarget(object):
    '''A class that represents a Make target

    Attributes:
        src_txtlist: The source block of text we extract everything else from.
        target: Destination target file.
        sources: Source files used to create the target.
        cmds_raw: Raw version of the commands outputted by make.
        _varlist: A MakeVarList class instance, a list of variables that can be used to expand out the cmd list.
    '''

    def __init__(self, src_txtlist=''):
        '''Class initialiser
        Args:
            src_txtlist: The source block of text we extract everything else from.
        '''
        self.src_txtlist = src_txtlist
        self.target = ''
        self.sources = []
        self.cmds_raw = []
        self._varlist = None

    def __repr__(self):
        '''Show the representation as the target for a debugger.'''
        return self.target

    @property
    def target_noext(self):
        '''Obtains the target file path without a file extension.
        Returns:
            The target file path without a file extension.
        '''
        root, ext = os.path.splitext(self.target)
        return root

    @property
    def sources_noheader(self):
        '''Obtains the list of sources with the .h header files removed.
        Returns:
            The list of sources with the .h header files removed.
        '''
        srcs = Enumerable(self.sources).where(lambda x: not x.endswith('.h')).to_list()
        return srcs

    @property
    def sources_noext(self):
        '''Obtain the list of sources with no file extensions.
        Returns:
            The list of sources with no file extensions.
        '''
        srcs = Enumerable(self.sources).select(lambda x: os.path.splitext(x)[0]).to_list()
        return srcs

    def cmds_expand(self, usemake=False):
        '''Try to expand the cmds_raw property into something readable.
        Args:
            usemake: If true then we use make to do the expansion.
        Returns:
            A list of commands for the target that are expanded.
        '''
        ret = []
        for item in self.cmds_raw:
            item = item.replace('$@', self.target)
            item = item.replace('$^', ' '.join(self.sources))
            ret.append(self._varlist.expand_expr(item, usemake=usemake)[0])
        return ret

    def parse(self):
        '''Parse the src_txtlist into all the fields.'''
        # Extract the Target
        firstline = self.src_txtlist[0].split(':')
        self.target = firstline[0].strip()
        # Extract the Sources
        srcs = firstline[1].strip().split(' ')
        self.sources = []
        for item in srcs:
            item = item.strip()
            self.sources.append(item)
        # Extract the raw command
        index = 0
        cmdsfound = False
        for line in self.src_txtlist:
            line = line.strip()
            if cmdsfound is True and line != '':
                self.cmds_raw.append(line)
            if line.startswith('#  commands to execute'):
                cmdsfound = True
            index += 1

    @staticmethod
    def parse_targets(txtdb, varlist=None):
        '''Parse the Makefile text database into a list of targets.
        Args:
            txtdb: The makefile database text to parse.
            varlist: This can be used to pass in a MakeVarList class instance for use with expansion later on.
        Returns:
            A list of targets.
        '''

        # Split the string into blocks based on double newline
        grp_txt = txtdb.split('\n\n')

        # Search for the stand and end block
        rules_start = -1
        rules_end = -1
        index = 0
        for line in grp_txt:
            if line.startswith('# Files'):
                rules_start = index
            if line.endswith('# VPATH Search Paths'):
                rules_end = index
            index += 1

        rules = []
        for i in range(rules_start + 1, rules_end):
            line = grp_txt[i]
            if not line.startswith('#'):
                tgt = MakeTarget(line.splitlines())
                tgt.parse()
                tgt._varlist = varlist
                if tgt.target == '.PHONY':
                    continue
                rules.append(tgt)
        return rules
