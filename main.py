from pydriller import * 
import subprocess

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
    result = subprocess.run(['srcml', '-t', source, '-l', filetype])
    return result.stdout

## MAIN ###

# Outer loop that steps through commits
for commit in RepositoryMining(git_repo).traverse_commits():
    counter = counter + 1
    print("Commit " + str(counter) + "\n")

    # Inner loops that steps trough each modification in the current commit
    for m in commit.modifications:

        if IsSourceFile(m.filename): #Determine if the file is a source file or not
            print(m.filename + " " + str(m.change_type))
            print(GetSRCML(m.source_code, 'C'))

            # In here, we can parse the code for style changes.
            # was thinking that instead of parsing the same text over and over again,
            # that we instead look at the modifications. With each modification, we can
            # add or subtract the number of times the author uses a certain style
            # (number of times they put '{' on the same line as 'if', # of times tabs is used, etc)

    print()

