import subprocess

# assigns value according to codeline complexity on average
def get_code_factor(ftype):
    vlow = set(['txt', 'md'])
    low = set(['css', 'html', 'xml', 'json', 'yaml'])
    middling = set(['js', 'java', 'cs', 'rb', 'py', 'kt', 'ts'])
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

 # get annotate of specified file

# function to make sorting function usable                   
def takeSecond(elem):
    return elem[1]

def print_rank(devs):
    # print based on loc
    devs.sort(reverse=True, key=takeSecond)
    rank = 1
    print("\n[PRINTING] Printing according to rank, name and score\n")
    for name, score in devs:
        print(rank, name, score)
        rank += 1
        if rank > 50:
            break
    print("\n[END]")
    
def print_order(devs):
    # print based on loc
    devs.sort(reverse=True, key=takeSecond)
    rank = 1
    print("\n[PRINTING] Printing according to rank, name and score\n")
    for name, score in devs:
        print(name)
        rank += 1
        if rank > 50:
            break
    print("-----")
    rank = 1
    for name, score in devs:
        print(score)
        rank += 1
        if rank > 50:
            break
    print("\n[END]")
    
repo_path = "C:/Users/oisin/Desktop/Forth-Year/FYP/extracted-repos/rspack"
cd_repo = "cd " + repo_path[2:]

command = cd_repo + " && git whatchanged"
whatchanged = subprocess.check_output(command, shell=True).decode('utf-8')

devs = []

line = whatchanged.split("\n")
author = ""
files_pcommit = 0
files_pcommit_score = 0
highest_files_pcommit_score = 0
hfpcs = 0
hfc = 0
for i in range(len(line) - 1):
    if line[i] != "":
        if line[i][0] == "A":
            if author != "":
                if files_pcommit_score / files_pcommit >= 0.52:
                    #calulate score for this commit
                    score = pow(files_pcommit, files_pcommit_score / files_pcommit + 0.45)
                    #cap score
                    if score > 50:
                        score = 50
                    #add score to authors total score
                    if len(devs) == 0:
                        devs.append((author, score))
                    else:
                        for j in range(len(devs)):
                            # check to see if name is already on the list, if so +1
                            if devs[j][0] == author:
                                temp = devs[j][1]
                                temp += score
                                
                                devs[j] = (author, temp)
                                break
                            #if not, create a new name with a single loc
                            elif j == len(devs) - 1:
                                devs.append((author, score))
                    #reset
                    files_pcommit_score = 0
                    files_pcommit = 0
            
            author = line[i][8:line[i].find("<") - 1]
        elif line[i][0] == ":":
            files_pcommit += 1
            #print(line[i])
            word = line[i].split(" ")
            temp = word[4].split('.')
            ftype = "?"
            ftype = temp[len(temp) - 1]
            #print(ftype, get_code_factor(ftype))
            files_pcommit_score += (get_code_factor(ftype) + 1) / 2
            
print_order(devs)