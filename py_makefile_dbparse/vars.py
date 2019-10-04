'''
Represents a collection of variables extracted from a Makefile.
'''

import re
import sys


class MakeVarList(object):
    '''Represents a collection of variables extracted from a Makefile.

    Attributes:
        values: The make database parsed as a collection of values.
        launcher: If a launcher is specified then we can use that for extracting more info later on.
    '''

    def __init__(self, launcher=None):
        '''Class initialiser.
        Args:
            launcher: If a launcher is specified then we can use that for extracting more info later on.
        '''
        self.values = []
        self.launcher = launcher

        ## @property origin
        # Which variable types (origins) to include / look for. <br>
        # 'automatic', 'environment', 'default', 'override', 'makefile'. <br>
        # None returns all origins. The default is ['environment', 'makefile'].
        self.origin = ['environment', 'makefile']

    def parse_vars(self, dbtxt):
        '''Parse the Makefile text database.
           Generate the (key,value) dict of all variables defined in make process.
        Args:
            dbtxt: The database text to use / parse.
        Returns:
            The parsed variables.
        '''
        # Split the string up into lines
        split_txt = dbtxt.splitlines()

        # Find the start / end of the variable segment
        re_start = re.compile(r"^#\s*Variables\b")  # start of variable segment
        re_end = re.compile(r"^#\s*variable")  # end of variable segment
        startseg, endseg = self.__find_segment_range(split_txt, re_start, re_end)

        # Extract out the variables
        extracted_vars = {}
        mname = None
        for i in range(startseg + 1, endseg):
            line = split_txt[i].strip()

            # find the type of variable
            if line.startswith("#"):
                q = line.split()
                mname = q[1]

            # If the type of variable has been found, assume the line below is the definition
            elif mname is not None:
                # Check if the type of variable is one we're interested in
                if self.origin is not None and mname not in self.origin:
                    continue
                # Create a variable type entry if it doesn't exist
                if mname not in extracted_vars:
                    extracted_vars[mname] = {}
                # Extract the variable
                q = line.split(maxsplit=2)   # key =|:= value
                if len(q) == 2:
                    extracted_vars[mname][q[0]] = ''
                else:
                    extracted_vars[mname][q[0]] = q[2]
                mname = None

        self.values = extracted_vars
        return extracted_vars

    def __find_segment_range(self, lines, re_start, re_end):
        '''Find the beginning and end line of a segment within the Makefile database.
        Args:
            lines: A list of lines of text to search through.
            re_start: regex for the start.
            re_end: regex for the end.
        Returns:
            The start / end segment indexes.
        '''
        startseg = endseg = -1
        index = 0
        for line in lines:
            if startseg == -1 and re_start.search(line):
                startseg = index
            if endseg == -1 and re_end.search(line):
                endseg = index
            index += 1
        return startseg, endseg

    def expand_var(self, vals, usemake=False):
        '''Expand a given variable (or list of variables) within the Makefile database.
        Args:
            vals: A variable name, or list of variable names.
            usemake: if to use make to do the expansion.
        Returns:
            The expanded variable(s).
        '''
        ret = {}
        retlist = True
        if not isinstance(vals, list):
            vals = [vals]
            retlist = False
        if usemake:
            ret = self.__expand_make_vars(vals)
        else:
            for item in vals:
                expandeditem = '$(%s)' % item
                ret[item] = self.__expand_local(expandeditem)
        if retlist:
            return ret
        else:
            return ret.get(vals[0])

    def expand_expr(self, vals, usemake=False):
        '''Expand a given expression (or list of expressions) within the Makefile database.
        Args:
            vals: An expression, or list of expressions.
            usemake: if to use make to do the expansion.
        Returns:
            The expanded expression(s).
        '''
        ret = []
        if not isinstance(vals, list):
            vals = [vals]
        if usemake:
            for item in vals:
                ret.append(self.__expand_make_expression(item))
        else:
            for item in vals:
                ret.append(self.__expand_local(item))
        return ret

    def __expand_local(self, val):
        '''Expand all $(var) variables in val using local expansion.
        Args:
            val: The expression / variable to expand.
        Returns:
            A dictionary result from in memory values.
        '''
        if self.values is None:
            return None
        rev = re.compile(r"\$\((\w+)\)")
        s = val
        p1 = p2 = 0
        cnt = 0
        while True:
            # position p2 search starts - default=0
            m = rev.search(s, p2)
            if m is None:
                break
            k = m.group(1)
            p1, p2 = m.span(0)

            # new value
            v = None
            # search for key in multikey dictinary
            for o in self.values:
                if k in self.values[o]:
                    v = self.values[o][k]
                    break

            if v is not None:
                s = s[:p1] + v + s[p2:]
                p2 = p1  # at position p1 it may be new replacement $(...)
            # on None - no replacement but search starts from position p2

            cnt += 1
            if cnt > 1000:
                print("Error maybe loop detected cnt: {}".format(cnt))
                sys.exit(1)
        #print("cnt=", cnt)
        return s

    def __expand_make_vars(self, varset):
        '''Expand a specific set of variables in varset by running make.
           This can give a better expansion than expand_var.
           but requires calling make to expand out the variable so takes longer.
        Args:
            varset: The variables to expand.
        Returns:
            A dictionary result from make.
        '''
        # Build up a list of info lines we want to run
        mkin = ''
        for item in varset:
            mkin += '\t$(info %s:=$(%s))' % (item, item) + '\n'
        # Launch make with a dummy target to gather the info
        mkout = self.__run_make(mkin)
        # Parse the output
        lines = mkout.splitlines()
        ret = {}
        for line in lines:
            vals = line.split(':=')
            ret[vals[0]] = vals[1]
        return ret

    def __expand_make_expression(self, expr):
        '''Use make to expand a given expression.
        Args:
            expr: The expression to expand.
        Returns:
            The output from make.
        '''
        # Build up the expression we want to run
        mkin = '\t$(info %s)' % (expr) + '\n'
        # Launch make with a dummy target to gather the info
        mkout = self.__run_make(mkin).strip()
        return mkout

    def __run_make(self, mkin):
        '''Launch make with an in memory modified Makefile to gather / extract information.
        Args:
            mkin: The make commands to add to the dummy target.
        Returns:
            The output from make.
        '''
        mktxt = self.launcher.read_makefile()
        mktxt += '\n\n'
        mktxt += 'py_makefile_dbparse_info:\n'
        mktxt += mkin
        # We're going to pipe the altered makefile in via stdin
        result_txt = self.launcher.run('-ns -f - py_makefile_dbparse_info', stdin_txt=mktxt)
        return result_txt
