#!/bin/env python3
#honeydew.py
"""
Script that will search all files in a directory for `TODO` and
`FIXME` comments, grouping them by filename.

No input arguments. Simply invoke `python3 honeydew.py`

The parser is searching for comment lines containing `#` followed by any number
of spaces, then `TODO` OR `FIXME` followed by spaces. The pattern match regexp
terminates with a colon `:` and will print the entire line out in `TODO.md`.

TODO.md is generated if it does not exist, and ignored by the parser if it does.
As of 2019.01.30 the script does not modify `TODO.md` in place if it does exist.

Written by:  Joseph J. Radler, University of Washington
Date Written:   2019.01.24
Date Appended:  2019.01.30
Version:        0.4
Status:         Prototype
"""
import re
import os
from os import getcwd as cwd
# import glob
import textwrap
import datetime

def main():
    """
    Main program function executing function calls for each process.
    Input Args:
                        None
    Return Args:
                        None
    """
    print("Greetings! Now rifling through your source files!")

    # generate file and directory lists
    f_list = gen_fileslist()

    ## generate the header for the output file
    write_todoheader()

    ## now iterate over the filtered list of files to scan for targets
    print("Scanning files for items...")
    read_todos(f_list)
    print("Scan Complete! Your list is ready in `TODO.md`!")


def gen_fileslist():
    """
    Uses os.walk() to generate a list of filenames down through subdirectoriesi.
    List comprehensions are used to remove subdirectories from the scannable list.

    Input Args:         None
    Output Args:        dir_list        list of directories scannable
                        file_list       filtered list of files to be scanned
    """
    root_dir = os.getcwd()
    dir_excludes = ['.git']
    subdir_excludes = ['.git']
    file_list = []
    #TODO: Set this up as a call to an external .config-type file
    file_excludes = ['.gitignore', 'TODO.md', 'honeydew.py']

    for dir_name, subdir_names, file_names in os.walk(root_dir):
        if dir_name in dir_excludes:
            continue
        else:
            print("\nScanning directory %s ...\n" % dir_name)
            # dir_list.append(dir_name)
            subdir_names = [subdir_names.remove(subdir) for subdir in \
                    subdir_names if subdir in subdir_excludes]
            for fname in file_names:
                if fname in file_excludes:
                    continue
                else:
                    file_list.append(os.path.join(dir_name, fname))
    return file_list

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
        for item in todos:
            ## adds the appropriate Markdown formatting for radio button boxes
            item = chkbox + "\t" + item.strip("#")
            file.write(item)

        file.write("---\n")
        print("Entries for %s source file in TODO.md have been generated!" \
                % f_name)


main()  # runs the main program as defined above.
