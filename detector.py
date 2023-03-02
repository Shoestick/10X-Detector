import subprocess
import os

# various checks to see if the code actually contributed anything
def line_is_valid(codeline):
    # check if the line is empty or is just a close bracket
    if codeline == "" or codeline[0] == "}" or codeline[0] == "]" or codeline[0] == ")":
        return False
    # check if the line is just an close bracket
    else:
        # closed brackets on the first char are delt with above. Otherwise check if the
        # current char is empty, if so check the next char, if not empty, if it is a closed 
        # bracket then return false, otherwise move to next check
        for i in range(len(codeline) - 1):
            if codeline[i] == " ":
                if codeline[i + 1] == "}" or codeline[i + 1] == "]" or codeline[i + 1] == ")":
                    return False
                elif codeline[i + 1] != " ":
                    break
    # check to see if the line is a comment
    # check to see if the line is boilerplate
    # otherwise it's good
    return True

# calulate dev score
def get_score(devs, repo_path):
    #
    # calculation: (loc * avg_commits) / num_commits 
    #
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

    # get average number of commits per person
    avg_commits = total_commits // len(devs)

    for j in range(len(devs)):
        # use num_commits and loc to give a score to each name
        name = devs[j][0]
        loc = devs[j][1]
        num_commits = devs[j][2]
        score = loc / (num_commits / avg_commits)
        devs[j] = (name, score, loc)
        
# function to make sorting function usable                   
def takeSecond(elem):
    return elem[1]

# print rank, name and score of every dev
def print_rank(devs):
    # print based on loc
    devs.sort(reverse=True, key=takeSecond)
    rank = 1
    print("\n[PRINTING] Printing according to rank, name and score\n")
    for name, number, loc in devs:
        print(rank, name, number, loc)
        rank += 1
    print("\n[END]")

# initialise list to store dev names and loc
devs = []

# get annotate of specified file
repo_path = "C:/Users/oisin/Desktop/Forth-Year/FYP/extracted-repos/html5-boilerplate"
cd_repo = "cd " + repo_path[2:54]

print("[START]")
exclude = set(['.git'])
for root, dirs, files in os.walk(repo_path, topdown=True):
    dirs[:] = [d for d in dirs if d not in exclude]
    for filename in files:
        if (not filename[-4:] == '.ico' and not filename[-4:] == '.svg' and not filename[-4:] == '.png' and
            not filename[-4:] == '.jpg' and not filename[-4:] == 'jpeg' and not filename[-4:] == '.tif'):
            #print("[PROCESSING]", filename)
            command = cd_repo + root[54:] + " && git annotate " + filename
            annotation = subprocess.check_output(command, shell=True).decode('utf-8')

            # split paragraph string into lines
            segannotate = annotation.split("\n")

            # MAIN ### MAIN ### MAIN ### MAIN ### MAIN ### MAIN ### MAIN ### MAIN
            for i in range(len(segannotate) - 1):
                # split line to get code from the line
                word = segannotate[i].split("\t")
                codeline = word[3].split(")") # the line of code is actually codeline[1]
                # make sure something useful was actually committed
                if line_is_valid(codeline[1]):
                    # get name from line
                    name = word[1][1:]
                    # erase blank first characters
                    while name[0] == " ":
                        name = name[1:]
                    # deal with exception
                    if len(devs) == 0:
                        devs.append((name, 1, 0))
                    else:
                        for j in range(len(devs)):
                            # check to see if name is already on the list, if so +1
                            if devs[j][0] == name:
                                loc = devs[j][1]
                                loc += 1
                                devs[j] = (name, loc, 0)
                                break
                            #if not, create a new name with a single loc
                            elif j == len(devs) - 1:
                                devs.append((name, 1, 0))
                                
            print("[SUCCESS]", filename, "was successfully processed")

get_score(devs, repo_path)
    
print_rank(devs)