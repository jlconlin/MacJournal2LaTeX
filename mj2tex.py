# vim: set fileencoding=utf-8

from __future__ import print_function, division

"""
This script was written to export/convert MacJournal entries to (Xe|La)TeX.
"""

import os
import textwrap
import sys
sys.path.append("parser")

import MJParser
import LaTeX

def findJournal(Name, Journal):
    """
    findJournal will find a journal in the hierarchy. It searches from the top
    down and returns the first journal that matches.

    Name: Name of the journal
    Journal: Object containing journals.  Could be an macjournal.mjdoc instance
        or a journal/smart_journal instance.
    """

    for journal in Journal.Journals.values():
        if journal.name == Name:
            return journal

        # Look inside contained Journals
        elif journal.Journals:
            foundJournal = findJournal(Name, journal)
            if foundJournal:
                return foundJournal
            else:
                continue

    # If we get here, then we haven't found anything
    return None

def print_journals(mjDoc, args):
    """
    print_journals will print the journal names (and optionally the entry names)
    to the screen
    """
    print("\nJournals in MacJournal library:")
    MJParser.mjDoc.hierarchy(limit=args.print_journals)

def MakeLaTeX(Journal, texdir):
    """
    MakeLaTeX will create the directory structure for the LaTeX files and will
    create LaTeX files for each entry.

    Journal: Which Journal should be used
    texdir: Where should the files/folders be created
    """
    if not os.path.isdir(texdir):
        raise ( RuntimeError(
            "The path {} doesn't exist. I can't create LaTeX files there."
            .format(texdir) ) )

    texPath = os.path.join(texdir, "MacJournal")
    if not os.path.isdir(texPath):
        os.mkdir(texPath)

    # LaTeX template
    LT = LaTeX.LaTeXTemplate(
        title='This is the title',
        author="Jeremy Lloyd Conlin",
        date="\\today{}"
        )
    Journal.MakeLaTeX(LT, texPath, level=0)
    LT.write(os.path.join(texPath, "MacJournal.tex"))

    return LT

def ConvertFile(Name, path, outputPath):
    """
    ConvertFile will convert the file from the original format to something that
    can be "include"-d into LaTeX.

    Name: Name of the converted file (without the extension)
    path: Path of the original file (with extension)
    outputPath: Where the new file should be saved
    """
    pass

if __name__ == "__main__":
    print("\nI'm converting MacJournal data to (Xe|La)TeX.\n")

    import argparse
    parser = argparse.ArgumentParser(description="Extract Macjournal data")
    parser.add_argument('mjdoc', nargs='+', type=str,
        help='MacJournal document location.')
    parser.add_argument('-j', '--journals', type=str, default='all',
        help="Name of journal you want LaTeX'ed")

    info_group = parser.add_argument_group('Information')
    info_group.add_argument('--print-journals', type=str, default=None,
        help='Print the journals and the journal hierarchy.')

    LaTeX_group = parser.add_argument_group('LaTeX')
    LaTeX_group.add_argument('-c', '--compile', action='store_true',
        default=False, help='Compile LaTeX document')
    LaTeX_group.add_argument('--latex-dir', type=str, default=os.getcwd(),
        help=textwrap.dedent(
            """
            Where should the LaTeX file hieararchy be created.  If the directory
            exists a directory called MacJournal will be created at that
            location and everything will be created in the MacJournal directory.
            """)
        )
    LaTeX_group.add_argument('-l', '--latex', action='store_true',
        default=False,
        help="Create LaTeX documents in location specified by --latex-dir.")

    args = parser.parse_args()

    # Print out args
    print("\nOptions entered:")
    for key, value in args.__dict__.items(): print("\t%s:\t%s" %(key,value))
    print()

    # Create the mjdoc class
    mjDoc = MJParser.mjdoc(args.mjdoc[0], verbose=False)

    # Print journals
    if args.print_journals: print_journals(mjDoc, args)

    # Pick the right journal
    if args.journals == 'all':
        pickedJournal = mjDoc
    else:
        pickedJournal = findJournal(args.journals, mjDoc)
    if pickedJournal: pass

    # Create LaTeX files
    if args.latex:
        LT = MakeLaTeX(pickedJournal, args.latex_dir)

        if args.compile:
            LT.compile()




