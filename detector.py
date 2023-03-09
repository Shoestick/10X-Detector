import subprocess
import os
from datetime import date

# various checks to see if the code actually contributed anything
def line_is_valid(codeline):
    j = 0 # will be pos in string of first none space character
    # to see if the line contains anything
    if codeline == "":
        return False
    # to see if the line is longer than 2 none space characters
    # also to see if line has any none space characters
    else:
        for i in range(len(codeline)):
            if codeline[i] != " ":
                if i + 3 > len(codeline):
                    return False
                else:
                    j = i
                    break
            elif i + 3 > len(codeline):
                return False
    # check to see if the line is a single line comment
    if codeline[j] == "#" or (codeline[j] == "/" and codeline[j + 1] == "/"):
        return False
    # check for multiline comments
    # check to see if the line is boilerplate
    # otherwise it's good
    return True

# calulates how old a line is in days based on blame info
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
    
# get the additions of each programmer and 
def get_additions(devs, repo_path):
    for i in range(len(devs)):
        command = "cd "+ repo_path[2:] + " && git log --author=\"" + devs[i][0] +"\" --format=tformat: --numstat"
        numstats = subprocess.check_output(command, shell=True).decode('utf-8')
        numstats_lines = numstats.split("\n")
        total_additions = 0
        for j in range(len(numstats_lines) - 1):
            numstats_split = numstats_lines[j].split("\t")
            addition = numstats_split[0]
            if addition != "-":
                total_additions += int(addition)
        name = devs[i][0]
        loc = devs[i][1]
        age_score = devs[i][2]
        devs[i] = (name, loc, age_score, total_additions)
        print("[SUCCESS]", name, "was successfully processed")
    
# calulate dev score
def get_score(devs, h_a_s, hloc):
    #
    # calculation: 50*((loc / highest_loc) + (age_score / highest_age_score))
    #
    for j in range(len(devs)):
        # use num_commits and loc to give a score to each name
        name = devs[j][0]
        loc = devs[j][1]
        age_score = devs[j][2]
        additions = devs[j][3]
        
        a = loc /hloc
        b = age_score / h_a_s
        if additions != 0:
            c = (loc * age_score) / additions # age score is inversly proportional to c, as I care less that their loc is small compared to additions if they have a large age score
        
        score = 50*a + 50*b + 0*c
        
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
        if rank > 50:
            break
    print("\n[END]")

devs = [] # initialise list to store devs, pre 'get_score' is currently "Name, loc, age_score, total_additions"
oldest_line = 0 # the oldest line of code
highest_age_score = 0
AGE_FACTOR = 3 # 2^AGE_FACTOR == how much more important a line is if it's twice as old as another

# get annotate of specified file
repo_path = "C:/Users/oisin/Desktop/Forth-Year/FYP/extracted-repos/html5-boilerplate"
cd_repo = "cd " + repo_path[2:54]

print("[START]")
exclude = set(['.git'])
for root, dirs, files in os.walk(repo_path, topdown=True):
    dirs[:] = [d for d in dirs if d not in exclude]
    for filename in files:
        if (not filename[-4:] == '.ico' and not filename[-4:] == '.svg' and not filename[-4:] == '.png' and
            not filename[-4:] == '.jpg' and not filename[-4:] == 'jpeg' and not filename[-4:] == '.tif' and
            not filename[-4:] == '.txt' and not filename[-3:] == '.md'):
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
                    # get age of line of code in days
                    codeline_age = day_difference(word[2])
                    # see if it's the oldest loc
                    if codeline_age > oldest_line:
                        oldest_line = codeline_age
                    # get name from line
                    name = word[1][1:]
                    # erase blank first characters
                    while name[0] == " ":
                        name = name[1:]
                    # deal with exception
                    if len(devs) == 0:
                        codeline_age_score = pow(codeline_age, AGE_FACTOR)
                        devs.append((name, 1, codeline_age_score, 0))
                    else:
                        for j in range(len(devs)):
                            # check to see if name is already on the list, if so +1
                            if devs[j][0] == name:
                                loc = devs[j][1]
                                loc += 1
                                
                                codeline_age_score = devs[j][2]
                                codeline_age_score = codeline_age_score + pow(codeline_age, AGE_FACTOR)
                                
                                devs[j] = (name, loc, codeline_age_score, 0)
                                break
                            #if not, create a new name with a single loc
                            elif j == len(devs) - 1:
                                codeline_age_score = pow(codeline_age, AGE_FACTOR)
                                devs.append((name, 1, codeline_age_score, 0))
                                
            print("[SUCCESS]", filename, "was successfully processed")
            
get_additions(devs, repo_path)

highest_age_score = 0
highest_loc = 0
for i in range(len(devs)):
    loc = devs[i][1]
    codeline_age_score = devs[i][2]
    if loc > highest_loc:
        highest_loc = loc
    if codeline_age_score > highest_age_score:
        highest_age_score = codeline_age_score

get_score(devs, highest_age_score, highest_loc)
    
print_rank(devs)