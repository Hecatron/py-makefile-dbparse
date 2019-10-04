'''
A wrapper class for launching make
'''

import os
import subprocess
import os.path as path


class MakeLauncher(object):
    '''A wrapper class for launching make

    Attributes:
        cmd: Path to the make executable.
        opts: Additional command line options to pass to make.
        makefile: Can be used to specify an alternative Makefile file name.
        workdir: Can be used to specify an alternative working directory.
        stdout: The returned standard output from make.
        stderr: The returned error output from make.
    '''

    def __init__(self, cmd='make', opts='', makefile='Makefile', workdir=''):
        '''Class initialiser
        Args:
            cmd: path to the make executable (default = make).
            opts: Additional options to pass to make (default = '').
            makefile: Name of the Makefile to use (default = Makefile).
            workdir: Working directory to use when running make (default = '' current directory).
        '''
        self.cmd = cmd
        self.opts = opts
        self.makefile = makefile
        self.workdir = workdir
        self.stdout = ''
        self.stderr = ''

    def run(self, localopts, stdin_txt=None):
        '''Launches make.
        Returns:
            The stdout from make.
        '''
        makeopts = self.opts + ' ' + localopts
        if self.workdir:
            makeopts += ' -C ' + self.workdir
        if self.makefile != 'Makefile':
            makeopts += ' -f ' + self.makefile
        makecmd = self.cmd + ' ' + makeopts
        self.stdout, self.stderr = self.__run_proc(makecmd, stdin_txt=stdin_txt)
        return self.stdout

    def read_makefile(self):
        '''Reads the content of a Makefile referenced by the class.
        Returns:
            The text of the Makefile.
        '''
        filepath = path.join(self.workdir, self.makefile)
        with open(filepath, 'r') as file:
            ret = file.read()
        return ret

    def write_makefile(self, contents):
        '''Writes the given content to the Makefile referenced by the class.
        Args:
            contents: the contents to write to the makefile.
        '''
        filepath = path.join(self.workdir, self.makefile)
        # Get the directory and create it if it doesn't exist
        dirpath = path.dirname(filepath)
        if not path.exists(dirpath):
            os.makedirs(dirpath)
        # Write the file
        with open(filepath, 'w') as file:
            ret = file.write(contents)
        return

    def __run_proc(self, cmdarray, workingdir='', stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin_txt=None, printresult=False):
        '''Wrapper for running a process'''
        if not workingdir:
            workingdir = os.getcwd()
        stdin_pipe = None
        stdin_bin = None
        if stdin_txt:
            stdin_pipe = subprocess.PIPE
            stdin_bin = stdin_txt.encode()
        proc = subprocess.Popen(cmdarray, cwd=workingdir, stdout=stdout, stderr=stderr, stdin=stdin_pipe, universal_newlines=True)
        proc_out, proc_err = proc.communicate(input=stdin_txt)
        if printresult:
            print(proc_out)
            print(proc_err)
        if proc.returncode != 0:
            raise RuntimeError("Failure to run command")
        return proc_out, proc_err
