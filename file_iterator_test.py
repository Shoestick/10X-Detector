import os
import subprocess

 # get annotate of specified file
repo_path = "C:/Users/oisin/Desktop/Forth-Year/FYP/extracted-repos/html5-boilerplate"
cd_folder = "cd " + repo_path[2:54]
cd_repo = "cd " + repo_path[2:]

devs = [("Paul Irish", 0, 0), ("Paul Irish", 0, 0), ("Rob Larsen", 0, 0)]

for i in range(len(devs)):
    command = cd_repo + " && git log --author=\"" + devs[i][0] +"\" --format=tformat: --numstat"
    numstats = subprocess.check_output(command, shell=True).decode('utf-8')
    numstats_lines = numstats.split("\n")
    total_additions = 0
    for i in range(len(numstats_lines) - 1):
        numstats_split = numstats_lines[i].split("\t")
        addition = numstats_split[0]
        if addition != "-":
            total_additions += int(addition)
    print (total_additions)
    
    #next thing to do is run the command and check it works
    #see how to the output is outputted, like the one in the other file
    #see how to split it
    #split it and get the first column
    # turn those nums to ints and add them up
    #compare with github to see if it's about right
    
    command = "cd " + repo_path[2:] + " && git shortlog -sn --all"
    annotation = subprocess.check_output(command, shell=True).decode('utf-8')

    # split paragraph string into lines
    segannotate = annotation.split("\n")
    total_commits = 0
    # split lines into usable chunks
    for i in range(len(segannotate) - 1):
        word = segannotate[i].split("\t")
        num_commits = word[0]
        name = word[1]
        for j in range(len(devs)):
            # check if new name has appeared on the devs list,
            if devs[j][0] == name:
                # add the num of commits to the total_commits
                total_commits += int(num_commits)
                loc = devs[j][1]
                # append the number of commits by the dev to a new list beside it
                devs[j] = (name, loc, int(num_commits))
                break
    