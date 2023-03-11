import subprocess
import os
from datetime import date

def takeSecond(elem):
    return elem[1]

def day_difference(timestamp):
    refined = timestamp.split(" ")
    sdate = refined[0].split("-")
    syear = sdate[0]
    smonth = sdate[1]
    sday = sdate[2]

    commit_date = date(int(syear), int(smonth), int(sday))
    
    today = date.today()
    delta = today - commit_date
    
    return delta.days

# get annotate of specified file
repo_path = "C:/Users/oisin/Desktop/Forth-Year/FYP/extracted-repos/html5-boilerplate"
cd_repo = "cd " + repo_path[2:54]

oldest_commit = []

print("[START]")
command = "cd " + repo_path[2:] + " && git log --pretty=format:\"%an%x09%ad\" --date=format:\"%Y-%m-%d\""
annotation = subprocess.check_output(command, shell=True).decode('utf-8')


# print(annotation)
# split paragraph string into lines
segannotate = annotation.split("\n")
for i in range(len(segannotate)):
    word = segannotate[i].split("\t")
    name = word[0]
    day_diff = day_difference(word[1])
    
    if len(oldest_commit) == 0:
        oldest_commit.append((name, day_diff))
    else:
        for j in range(len(oldest_commit)):
            # check to see if name is already on the list, if so +1
            if oldest_commit[j][0] == name:
                if oldest_commit[j][1] < day_diff:
                    oldest_commit[j] = (name, day_diff)
                break
            #if not, create a new name with a single loc
            elif j == len(oldest_commit) - 1:
                oldest_commit.append((name, day_diff))
            
oldest_commit.sort(reverse=True, key=takeSecond)
for name, delta in oldest_commit:
    print(name, delta)
