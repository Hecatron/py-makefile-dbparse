#! python3
import os
import sys
import subprocess
import shutil
from os import path

class SphinxBuild(object):
    '''Sphinx Build Script'''

    def __init__(self):
        '''Class Init'''
        self.SOURCEDIR = path.abspath('source')
        self.BUILDDIR = path.abspath('build')
        self.SPHINXBUILD = 'sphinx-build'
        self.DOXYGENDIR = path.abspath('../doxygen')
        if 'SOURCEDIR' in os.environ:
            self.SOURCEDIR = os.environ.get('SOURCEDIR')
        if 'BUILDDIR' in os.environ:
            self.BUILDDIR = os.environ.get('BUILDDIR')
        if 'SPHINXBUILD' in os.environ:
            self.SPHINXBUILD = os.environ.get('SPHINXBUILD')

    def check_exe(self):
        '''Check to make sure sphinx-build exists on the path'''
        if not shutil.which(self.SPHINXBUILD):
            print("")
            print("The 'sphinx-build' command was not found. Make sure you have Sphinx")
            print("installed, then set the SPHINXBUILD environment variable to point")
            print("to the full path of the 'sphinx-build' executable. Alternatively you")
            print("may add the Sphinx directory to PATH.")
            print("")
            print("If you don't have Sphinx installed, grab it from http://sphinx-doc.org/")
            return False
        return True

    def usage(self):
        '''Print the Usage'''
        print('sphinx python build wrapper script (make.py)')
        cmdopts = [self.SPHINXBUILD, '-M', 'help', self.SOURCEDIR, self.BUILDDIR]
        self.run_cmd(cmdopts, '.')
        print("\nAdditional commands include - make.py <target> where <target> is one of")
        abs_build_path = path.abspath(self.BUILDDIR)
        print("  clean         to clean the output directory: " + abs_build_path)
        print("  serve         Serve the site out on a port for a demo / development")
        print("  doxygen       to build Doxygen related files")
        print("  build         does a clean followed by a html build")
        print("  publish       publish the site to the gh-pages branch")

    def run_cmd(self, cmdarray, workingdir, captureout=False):
        '''Run a command'''
        stdout = stderr = None
        if captureout:
            stdout = stderr = subprocess.PIPE
        proc = subprocess.Popen(cmdarray, cwd=workingdir, stdout=stdout, stderr=stderr, universal_newlines=True)
        proc_out, proc_err = proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError('Failure to run command')
        return stdout, stderr

    def emptydir(self, top):
        '''Empty a directory'''
        if(top == '/' or top == "\\"): return
        else:
            for root, dirs, files in os.walk(top, topdown=False):
                for name in files:
                    os.remove(path.join(root, name))
                for name in dirs:
                    os.rmdir(path.join(root, name))

    def clean(self):
        '''Clean the build directory'''
        abs_build_path = path.abspath(self.BUILDDIR)
        self.emptydir(abs_build_path)
        print ("Clean finished")

    def serve(self):
        '''Serve the site out locally for a demo / development'''
        self.clean()
        htmldir = path.join(self.BUILDDIR, 'html')
        cmdopts = ['sphinx-autobuild', '-b', 'html', self.SOURCEDIR, htmldir]
        self.run_cmd(cmdopts, '.')
        print("Server Closed.")

    def run_doxygen(self):
        '''Regenerate the xml files exported from doxygen, these are used by sphinx'''
        self.run_cmd(['doxygen'], self.DOXYGENDIR)
        # Filter the xml for the types of parameters
        self.run_cmd(['python', 'filter_types.py'], self.DOXYGENDIR)

    def run_sphinxbuild(self, args):
        '''Assuming one of the commands here isn't needed, instead pass the arguments to sphinx-build'''
        cmdopts = [self.SPHINXBUILD, '-M'] + args + [self.SOURCEDIR, self.BUILDDIR]
        self.run_cmd(cmdopts, '.')

    def publish(self):
        '''Publish / upload files to github pages'''
        htmldir = path.join(self.BUILDDIR, 'html')
        cmdopts = ['ghp-import', '-p', htmldir]
        self.run_cmd(cmdopts, '.')

    def main(self):
        if not self.check_exe():
            return
        if len(sys.argv) < 2:
            self.usage()
            return
        if sys.argv[1] == 'clean':
            self.clean()
            return
        if sys.argv[1] == 'serve':
            self.serve()
            return
        if sys.argv[1] == 'doxygen':
            self.run_doxygen()
            return
        if sys.argv[1] == 'build':
            self.clean()
            self.run_sphinxbuild(['html'])
            return
        if sys.argv[1] == 'publish':
            self.publish()
            return
        # If no command here is specified then just pass the args to sphinx-build
        self.run_sphinxbuild(sys.argv[1:])

if __name__ == "__main__":
    SphinxBuild().main()
