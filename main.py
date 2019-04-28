# Other libraries
from pydriller import * 
import subprocess

from xml.dom import minidom
from xml.parsers.expat import ExpatError

# Our imports
from config import git_repo

# CONSTANTS
SRC_FILES = ["js", "c", "py", "rb"]

# Globals
counter = 0

#### Helper functions

#Takes a file name as an input and determines if it is a source file or not
def IsSourceFile(filename):
    is_src = False
    if(filename.find(".") >= 0):
        file_extention = m.filename.split(".")[1]
        if file_extention in SRC_FILES:
            is_src = True

    return is_src

# get srcML of file
def GetSRCML(source, filetype):
    result = subprocess.Popen(['srcml', '-X', '-t', source, '-l', filetype], stdout=subprocess.PIPE)
    tmp = result.stdout.read()
    return tmp

## MAIN ###

# Variables for tracking entire project
prj_num_of_lines        = 0
prj_total_line_length   = 0

variable_names          = []

gr = GitRepository(git_repo)

# Outer loop that steps through commits
for commit in RepositoryMining(git_repo).traverse_commits():
    counter = counter + 1

    # Inner loops that steps trough each modification in the current commit
    for m in commit.modifications:
        if IsSourceFile(m.filename): 

            # Calculate line length
            parsed_lines = gr.parse_diff(m.diff)
            added = parsed_lines['added']
            deleted = parsed_lines['deleted']

            for x in added:
                if(x[1] != ''):
                    prj_num_of_lines += 1
                    prj_total_line_length += len(x[1])

            for x in deleted:
                if(x[1] != ''):
                    prj_num_of_lines -= 1
                    prj_total_line_length -= len(x[1])

            #srcml stuff
            xml_string = GetSRCML(m.source_code, 'C')
            xml = minidom.parseString(xml_string)

            unit = xml.documentElement
            declarations = unit.getElementsByTagName("decl")

            for x in declarations:
                for child in x.childNodes:
                    if(child.nodeType != child.TEXT_NODE):
                        if(child.tagName == 'name'):
                            for y in child.childNodes: # get variable name
                                if(y.nodeValue != None):
                                    variable_names.append(y.nodeValue)

                    
            # In here, we can parse the code for style changes.
            # was thinking that instead of parsing the same text over and over again,
            # that we instead look at the modifications. With each modification, we can
            # add or subtract the number of times the author uses a certain style
            # (number of times they put '{' on the same line as 'if', # of times tabs is used, etc)


    print("Commit " + str(counter) + "\n")
    print("LOC: " + str(prj_num_of_lines))
    print("Average Line Length: " + str(prj_total_line_length / prj_num_of_lines))
    print("Variable names: ", variable_names)
    print()
