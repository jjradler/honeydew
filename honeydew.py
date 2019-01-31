#!/bin/env python3
#honeydew.py
"""
Script that will search all files in a directory for `TODO` and
`FIXME` comments, grouping them by filename and eventually dirname.

No input arguments. Simply invoke `python3 honeydew.py`

The parser is searching for comment lines containing `#` followed by any number
of spaces, then `TODO` OR `FIXME` followed by spaces. The pattern match regexp
terminates with a colon `:` and will print the entire line out in `TODO.md`.

TODO.md is generated if it does not exist, and ignored by the parser if it does.
As of 2019.01.30 the script does not modify `TODO.md` in place if it does exist.
However, additional functionality may be added to automatically update your
`TODO.md` list by scanning it for completed tasks (indicated by the `- [x] `
at the beggining of the line in TODO.md).

Written by:  Joseph J. Radler, University of Washington
Date Written:   2019.01.24
Date Appended:  2019.01.30
Version:        0.3
Status:         Prototype
"""
import re
import textwrap
import datetime
from os import getcwd as cwd
from os import listdir as ldir
from os import chdir as chdir
from os.path import isdir as isd
from os.path import isfile as isf

def main():
    """
    Main program function executing function calls for each process.
    Input Args:
                        None
    Return Args:
                        None
    """
    print("Greetings! Now rifling through your source files!")
    ## first make the list of directories
    dirs_only = sep_dirs()    # TODO: add functionality to search subdirs.
    #TODO: add function for recursively navigating subdirectories
    ## then make the list of files in the current working directory
    files_only = sep_files()
    files_only = files_filter(files_only)
    print(files_only)       ## test print after filtering
    ## generate the header for the output file
    print("Writing TODO.md header...")
    write_todoheader()
    ## now iterate over the filtered list of files to scan for targets
    print("Scanning files...")
    read_todos(files_only)
    print("Scan Complete! Your list is ready in `TODO.md`!")


def sep_files():
    """
    Description:

    Isolates a list of file objects for parsing.

    Input Args:
                None

    Return Args:
                None
    """
    print("Generating files list...")
    return [i for i in ldir(cwd()) if isf(i)]   # list of files

def files_filter(fi_list):
    """
    Description:

    Filters the file list in `main()` to remove anything on the list of `excludes`

    Input Args:
                ex_list      list,strings: excludes list
                fi_list      list,strings: files list in current working directory

    Return Args:
                filtered  list,strings: files in current directory minus excludes
    """
    #TODO: Set up external configuration file to populate excludes.
    #TODO: add source file detection in this function.
    excludes = ['honeydew.py', 'TODO.md', '.gitignore', 'LICENSE', 'README.md']
    src_suffix = ['*.py', '*.cpp' '*.h', '*.c', '*.html', '*.md']   # sourcefile globs
    #TODO: use `glob` library to parse the file extension types and filter them.
    print(fi_list)       ## test print
    print(excludes)         ## test print
    #for item in excludes:
    #    if item in fi_list:
    #        fi_list.remove(item)
    return [fi_list.remove(item) for item in excludes if item in excludes]
    # return fi_list

def sep_dirs():
    """
    Description:

    Isolates a list of only directory objects for further operations.

    Notes:

    Additional features will be added with upcoming versions of this script
    whereby the various folders will also be scanned for source files in a number
    of languages containing `TODO` and `FIXME`s.

    Input Args:
                None

    Return Args:
                None
    """
    print("Generating directories list...")
    return [i for i in ldir(cwd()) if isd(i)]   # list of dirs


def read_todos(files):
    """
    Description:

    Reads `TODO` and `FIXME` entries in comments in each file generated in the
    filtered working directory list, then writes them to the output_file via
    the `write_todolist` function.

    Input Args:
                    files:      List of File Objects

    Return Args:
                    None

    Functions Called:
                    write_todolist()
    """
    print("Entering read_todos...")
    pattern_match = r'^#*\s*(todo|fixme)\s*:'   ## regex pattern for re.match()
    for target_file in files:                   ## iterate over all obj on list
        print("Opening file %s..." % target_file)
        todolist = []                           ## temporary list of todo items
        with open(target_file) as file:
            lines = file.readlines()            ## read lines of file object
            for line in lines:
                form_line = line.lower()        ## lowercase of `line`
                if re.match(pattern_match, form_line):
                    todolist.append(line)       ## append to list of todo items
        ## call the `write_todolist` function for the current `file` object.
        write_todolist(target_file, todolist)


def write_todoheader():
    """
    Description:

    Writes the header for the TODO list file `TODO.md`.

    Input Args:
                    None

    Return Args:
                    None
    """
    print("Writing text header for `TODO.md`...")
    this_dir = cwd()
    todays_date = datetime.datetime.today().strftime('%Y-%m-%d')
    header = '''\
             # TODO.md
             ---\n
             ## Your Honeydew List for Your %s
             ## Source Directory
             ### as generated on %s
             ---\n
             '''
    with open("TODO.md", 'w') as file: ## opens output file for writing.
        file.write(textwrap.dedent(header % (this_dir, todays_date)))


def write_todolist(f_name, todos):
    """
    Description:

    Generates the output TODO.md list based on parsed comment blocks in the
    file object passed in from `read_todos()`.

    Input Args:
                f_name:     name of target file passed in from `read_todos()`
                todos:      list of extracted `to-do` and `fix-me` items for file

    Return Args:
                None
    """
    chkbox = r"- [ ] "     ## checkbox character in markdown.
    with open("TODO.md", 'a') as file: ## opens "TODO.md" for appending
        file.write("### %s \n---\n" % (f_name))
        ## for loop over items in todos for this file object
        print("\nThe TODO list for %s is:\t%s\n" % (f_name, todos))
        for item in todos:
            # FIXME: remove leading "#" character from the line before appending
            item = chkbox + "\t" + item    # adds appropriate .md formatting
            file.write(item)

        file.write("---\n")
        print("Entries for %s source file in TODO.md have been generated!" % f_name)


main()  # runs the main program as defined above.


# if __name__ == "__main__":
#     print("Initializing...")
#     files_only = sep_files()
#     print(files_only)       ###TESTPRINT
#     # dirs_only = sep_dirs()
#     print(dirs_only)        ###TESTPRINT
#
#     read_todos(files_only)
