# Other libraries
from pydriller import * 
import subprocess
import os

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
def GetSRCML(source):
    result = subprocess.check_output(['srcml', source])
    return result

def GetVariableNamesFromSRCML(xml_string):
    toReturn = []

    xml = minidom.parseString(xml_string)

    unit = xml.documentElement
    declarations = unit.getElementsByTagName("decl_stmt")

    for x in declarations:
        decl = x.childNodes
        for child in decl[0].childNodes:
            if(child.nodeType != child.TEXT_NODE):
                if(child.tagName == 'name'):
                    for y in child.childNodes: # get variable name
                        if(y.nodeValue != None):
                            toReturn.append(y.nodeValue)
    return toReturn

# Determines if a string is in camelCase or not
def IsCamelCase(s):
    return s != s.lower() and s != s.upper() and "_" not in s and s[0] != s[0].upper()

# Determines if a string is in snake_case or not
def IsSnakeCase(s):
    return s.find('_') > 0 and s[-1] != '_'

def CountLeadingSpaces(s):
    return len(s) - len(a.lstrip(' '))

def CountLeadingTabs(s):
    return len(s) - len(a.lstrip('\t'))

## MAIN ###

# Creating files and directories
current_dir = os.path.dirname(os.path.abspath(__file__)) + "/data"
added_file_name = current_dir + "/added.c"
deleted_file_name = current_dir + "/deleted.c"

if not os.path.exists(current_dir):
    os.makedirs(current_path)

# Variables for tracking entire project
prj_num_of_lines        = 0
prj_num_of_vars         = 0
prj_total_line_length   = 0
prj_camel_case          = 0
prj_snake_case          = 0

gr = GitRepository(git_repo)

# Outer loop that steps through commits
for commit in RepositoryMining(git_repo).traverse_commits():
    counter = counter + 1
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print("Commit " + str(counter))
    print("Hash " + commit.hash + '\n')

    added_source_code = ''
    deleted_source_code = ''
    added_variable_names    = []
    deleted_variable_names   = []

    # Inner loops that steps trough each modification in the current commit
    for m in commit.modifications:
        if IsSourceFile(m.filename): 
            print(m.filename)

            temp = open(added_file_name, 'w')
            temp.close()

            temp = open(deleted_file_name, 'w')
            temp.close()

            added_file = open(added_file_name, "r+")
            deleted_file = open(deleted_file_name,"r+")

            # Calculate line length
            parsed_lines = gr.parse_diff(m.diff)
            added = parsed_lines['added']
            deleted = parsed_lines['deleted']

            for x in added:
                if(x[1] != ''):
                    prj_num_of_lines += 1
                    prj_total_line_length += len(x[1])
                    added_file.write(x[1])
                    added_file.write('\n')

            for x in deleted:
                if(x[1] != ''):
                    prj_num_of_lines -= 1
                    prj_total_line_length -= len(x[1])
                    deleted_file.write(x[1])
                    deleted_file.write('\n')

            added_file.close()
            deleted_file.close()
                    
            #srcml stuff
            added_xml = GetSRCML(added_file_name)
            deleted_xml = GetSRCML(deleted_file_name)

            added_variable_names = GetVariableNamesFromSRCML(added_xml)
            deleted_variable_names = GetVariableNamesFromSRCML(deleted_xml)

            for added in added_variable_names:
                prj_num_of_vars += 1
                print("Added:", added)

                if IsCamelCase(added):
                    prj_camel_case += 1
                    print("Camel: " + added)
                elif IsSnakeCase(added):
                    prj_snake_case += 1
                    print("Snake: " + added)

            for deleted in deleted_variable_names:
                prj_num_of_vars -= 1
                print("Deleted:", deleted)

                if IsCamelCase(deleted):
                    prj_camel_case -= 1
                    print("Camel: " + deleted)
                elif IsSnakeCase(deleted):
                    prj_snake_case -= 1
                    print("Snake: " + deleted)


    print("LOC: " + str(prj_num_of_lines))
    if(prj_num_of_lines > 0):
        print("Average Line Length: " + str(prj_total_line_length / prj_num_of_lines))
    print("Number of Variables: ", prj_num_of_vars)
    print("Number of Snake Case Vars: ", prj_snake_case)
    print("Number of Camel Case Vars: ", prj_camel_case)
    print()
