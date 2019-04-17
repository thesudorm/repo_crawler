from pydriller import * 
from config import git_repo

counter = 0

# Outer loop that steps through commits
for commit in RepositoryMining(git_repo).traverse_commits():
    counter = counter + 1
    print("Commit " + str(counter) + "\n")
    commit_code = ""

    # Inner loops that steps trough each modification in the current commit
    for m in commit.modifications:
        print(m.filename + " " + str(m.change_type))
        #print(m.source_code)

        # In here, we can parse the code for style changes.
        # was thinking that instead of parsing the same text over and over again,
        # that we instead look at the modifications. With each modification, we can
        # add or subtract the number of times the author uses a certain style
        # (number of times they put '{' on the same line as 'if', # of times tabs is used, etc)

    print()
