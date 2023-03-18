import subprocess
import os
from datetime import date

# get the oldest commit an author has contributed
def get_oldest_commit(oldest_commit, cd_repo):
    command = cd_repo + " && git log --pretty=format:\"%an%x09%ad\" --date=format:\"%Y-%m-%d\""
    annotation = subprocess.check_output(command, shell=True).decode('utf-8')

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

# assigns value according to codeline complexity on average
def get_code_factor(ftype):
    vlow = set(['txt', 'md'])
    low = set(['css', 'html', 'xml', 'json'])
    middling = set(['js', 'java', 'cs', 'rb', 'py', 'kt'])
    high = set(['c', 'cpp', 'cc', 'h', 'hh'])
    vhigh = set(['rs', 'go', 'hs', 'lhs', '.ex'])
    
    # ordered by which it's most likely to be
    if(ftype in middling):
        return 1
    elif(ftype in high):
        return 1.3
    elif(ftype in low):
        return 0.1
    elif(ftype in vlow):
        return 0.05
    elif(ftype in vhigh):
        return 1.6
    
    return 1
    
# takes in oldest_commit and name, and return how old the oldest commit of that author is
def authors_oldest_commit(oldest_commit, name):
    for j in range(len(oldest_commit)):
        if oldest_commit[j][0] == name:
            return oldest_commit[j][1]
            
    print("[ERROR] Name not found in commit history, unkown how old their oldest commit is")
    return 0
    
# get the additions of each programmer and 
def get_additions_deletions(devs, repo_path):
    for i in range(len(devs)):
        command = "cd "+ repo_path[2:] + " && git log --author=\"" + devs[i][0] +"\" --format=tformat: --numstat"
        numstats = subprocess.check_output(command, shell=True).decode('utf-8')
        numstats_lines = numstats.split("\n")
        total_additions = 0
        total_deletions = 0
        for j in range(len(numstats_lines) - 1):
            numstats_split = numstats_lines[j].split("\t")
            addition = numstats_split[0]
            if addition != "-":
                total_additions += int(addition)
            deletion = numstats_split[1]
            if deletion != "-":
                total_deletions += int(addition)
        name = devs[i][0]
        loc = devs[i][1]
        age_score = devs[i][2]
        new_boost = devs[i][4]
        devs[i] = (name, loc, age_score, total_additions, new_boost, total_deletions)
        print("[SUCCESS]", name, "was successfully processed")
    
# calulate dev score
def get_score(devs, hloc, h_a_s, hadditions, h_boost, hdeletions):
    #
    # calculation: 
    #
    for j in range(len(devs)):
        # use num_commits and loc to give a score to each name
        name = devs[j][0]
        loc = devs[j][1]
        age_score = devs[j][2]
        additions = devs[j][3]
        new_boost = devs[j][4]
        deletions = devs[j][5]
        
        a = loc / hloc
        b = age_score / h_a_s
        if additions != 0:
            c = (loc * b) / additions # age score is inversly proportional to c, as I care less that their loc is small compared to additions if they have a large age score
        d = pow(new_boost, BOOST_FACTOR) / pow(h_boost, BOOST_FACTOR)
        e = additions / hadditions
        f = deletions / hdeletions
        score = 16*a + 16*b + 16*c + 16*d + 16*e + 16*f
        
        devs[j] = (name, round(score, 3), round(10*a, 2), round(10*b, 2), round(10*c, 2), round(10*d, 2), round(10*e, 2), round(10*f, 2))
        
# function to make sorting function usable                   
def takeSecond(elem):
    return elem[1]

# print rank, name and score of every dev
def print_rank(devs):
    # print based on loc
    devs.sort(reverse=True, key=takeSecond)
    rank = 1
    print("\n[PRINTING] Printing according to rank, name and score\n")
    for name, score, a, b, c, d, e, f in devs:
        print(rank, name, score, "|", a, b, c, d, e, f)
        rank += 1
        if rank > 50:
            break
    print("\n[END]")

devs = [] # initialise list to store devs, pre 'get_score' is currently "Name, code_score, age_score, total_additions, new_boost, deletions"
oldest_commit = []
#oldest_line = 0 # the oldest line of code
highest_age_score = 0

AGE_FACTOR = 3 # 2^AGE_FACTOR == how much more important a line is if it's twice as old as another
NEW_BOOST_PERIOD = 365 // 2
BOOST_FACTOR = 1.5

# get annotate of specified file
repo_path = "C:/Users/oisin/Desktop/Forth-Year/FYP/extracted-repos/html5-boilerplate"

print("[START]")

get_oldest_commit(oldest_commit, "cd " + repo_path[2:])

#get blame
exclude = set(['.git', '.gitlab', '.github'])
exclude_file = set(['ico', 'svg', 'png', 'jpg', 'jpeg', 'tif', 'woff', 'woff2', 
                    'ttf', 'bin', 'zip', 'tar', 'gz', 'webp'])
for root, dirs, files in os.walk(repo_path, topdown=True):
    dirs[:] = [d for d in dirs if d not in exclude]
    for filename in files:
        # to get the file type
        temp = filename.split('.')
        for i in range(len(temp)):
            ftype = temp[i]
        if not (ftype in exclude_file): # text file types
            print("[PROCESSING] Processing ", filename)
            command = "cd " + repo_path[2:54] + root[54:] + " && git annotate " + filename
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
                    # get name from line
                    name = word[1][1:]
                    # erase blank first characters
                    while name[0] == " ":
                        name = name[1:]
                    code_factor = get_code_factor(ftype)
                    # deal with exception
                    if len(devs) == 0:
                        codeline_age_score = pow(codeline_age, AGE_FACTOR)
                        new_boost = 0
                        days_oldest_commit = authors_oldest_commit(oldest_commit, name)
                        if (days_oldest_commit - NEW_BOOST_PERIOD) < codeline_age:
                            new_boost = code_factor
                    
                        devs.append((name, code_factor, codeline_age_score, 0, new_boost, days_oldest_commit))
                    else:
                        for j in range(len(devs)):
                            # check to see if name is already on the list, if so +1
                            if devs[j][0] == name:
                                loc = devs[j][1]
                                loc += code_factor
                                
                                days_oldest_commit = devs[j][5]
                                new_boost = devs[j][4]
                                if (days_oldest_commit - NEW_BOOST_PERIOD) < codeline_age:
                                    new_boost += code_factor
                                
                                codeline_age_score = devs[j][2]
                                codeline_age_score = codeline_age_score + pow(codeline_age, AGE_FACTOR)
                                
                                devs[j] = (name, loc, codeline_age_score, 0, new_boost, days_oldest_commit)
                                break
                            #if not, create a new name with a single loc
                            elif j == len(devs) - 1:
                                codeline_age_score = pow(codeline_age, AGE_FACTOR)
                                new_boost = 0
                                days_oldest_commit = authors_oldest_commit(oldest_commit, name)
                                if (days_oldest_commit - NEW_BOOST_PERIOD) < codeline_age:
                                    new_boost = code_factor
                                devs.append((name, code_factor, codeline_age_score, 0, new_boost, days_oldest_commit))
                                
            print("[SUCCESS]", filename, "was successfully processed")

get_additions_deletions(devs, repo_path)

highest_age_score = 1
highest_loc = 1
highest_additions = 1
highest_new_boost = 1
highest_deletions = 1

def highest(i, test_condition, highest_test):
    test = devs[i][test_condition]
    if test > highest_test:
        return test
    return highest_test
    
for i in range(len(devs)):
    highest_loc = highest(i, 1, highest_loc)
    highest_age_score = highest(i, 2, highest_age_score)
    highest_additions = highest(i, 3, highest_additions)
    highest_new_boost = highest(i, 4, highest_new_boost)
    highest_deletions = highest(i, 5, highest_deletions)

get_score(devs, highest_loc, highest_age_score, highest_additions, highest_new_boost, highest_deletions)
    
print_rank(devs)