from pydriller import * 
import json

commits, source = [], []

commit_code = ""

for commit in RepositoryMining("/home/bauerj/Projects/sudoku").traverse_commits():
    commit_code = ""
    for m in commit.modifications:
        commit_code += m.source_code + "\n"

    source.append(commit_code)

for x in source:
    print("COMMMMMMITTTT")
    print("~~~~~~~~~~~~~")
    test = [{"commit": x}]
    print(x)
    print()
    print()
    print()


