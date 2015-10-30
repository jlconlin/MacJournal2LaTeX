# vim: set fileencoding=utf-8

from __future__ import print_function, division

"""
This module can be used to create LaTeX files. It is intended for use in the
mj2tex.py script.
"""

import textwrap
import os

LaTeXLevels = ['section', 'subsection', 'subsubsection', 'paragraph']

class LaTeXTemplate(object):
    """
    LaTeXTemplate is a class that handles the creation of a LaTeX file.
    """
    _preamble = textwrap.dedent("""
    \\documentclass[letterpaper,12pt]{{{docClass}}}
    \\usepackage[T1]{{fontenc}}
    \\usepackage[colorlinks]{{hyperref}}
    \\usepackage{{color}}
    \\usepackage{{fancyhdr}}
    
    \\title{{ {title} }}
    \\author{{ {author} }}
    \\date{{ {date} }}
    """
    ).lstrip()

    def __init__(self, title='', author='', date='', docClass='article',
        **kwargs):
        super(LaTeXTemplate, self).__init__()

        # Set some defaults
        templateArgs = {'title':title, 'author':author, 'date': date,
                'docClass': docClass}
        templateArgs.update(kwargs)

        self.preamble = self._preamble.format(**templateArgs)

        self.lines = []

        self.includes = []

    def append(self, LaTeXPath):
        """
        append will append a path (of a LaTeX file) to the list of inclued
        files.
        """
        self.includes.append(LaTeXPath)

    def write(self, filename):
        """
        write will write the LaTeX file to the location indicated in the path
        variable.

        What to call the LaTeX filename
        """
        self.filename = filename
        self.file = open(filename, 'w')

        self.file.write(self.preamble)
        self.file.write("\\begin{document}\n")
        self.file.write("\\maketitle")

        self.file.writelines(self.lines)

        self.file.write("\n\\end{document}")

        self.file.close()

    def compile(self, command="latexmk -pdf"):
        """
        compile will compile the LaTeX file with the given command.
        """
        parent, filename = os.path.split(self.filename)
        print("Parent directory: {}".format(parent))
        curdir = os.getcwd()
        os.chdir(parent)
        os.system(u"{} {}".format(command, filename))
        os.chdir(curdir)
        
if __name__ == "__main__":
    print("\nI'm LaTeX'ing some stuff.\n")
