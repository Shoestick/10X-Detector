import os

 # get annotate of specified file
repo_path = "C:/Users/oisin/Desktop/Forth-Year/FYP/extracted-repos/example"
cd_repo = "cd " + repo_path[2:54]


command = "cd " + repo_path[2:] + " && git shortlog -sn --all"
print(command)