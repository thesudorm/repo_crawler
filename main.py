# Other libraries
from pydriller import * 
import subprocess
import xml.etree.ElementTree as ET

# Our imports
from config import git_repo

# CONSTANTS
SRC_FILES = ["js", "c", "py", "rb"]

# Globals
counter = 0

#Helper functions
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

# Outer loop that steps through commits
for commit in RepositoryMining(git_repo).traverse_commits():
    counter = counter + 1
    print("Commit " + str(counter) + "\n")

    # Inner loops that steps trough each modification in the current commit
    for m in commit.modifications:

        if IsSourceFile(m.filename): #Determine if the file is a source file or not
            print(m.filename + " " + str(m.change_type))
            xml_string = GetSRCML(m.source_code, 'C')
    
            xml = ET.fromstring(xml_string)

            for x in xml.findall('.//{http://www.srcML.org/srcML/src}if'):
                print(x.tag, x.attrib)

            # In here, we can parse the code for style changes.
            # was thinking that instead of parsing the same text over and over again,
            # that we instead look at the modifications. With each modification, we can
            # add or subtract the number of times the author uses a certain style
            # (number of times they put '{' on the same line as 'if', # of times tabs is used, etc)

    print()
