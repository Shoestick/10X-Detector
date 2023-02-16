import subprocess

# get annotate of specified file
repo_path = "cd /Users/oisin/Desktop/Forth-Year/FYP/extracted-repos/mynetworks"
file_name = "regional.py"
command = repo_path + " && git annotate " + file_name
annotation = subprocess.check_output(command, shell=True).decode('utf-8')

# split paragraph string into lines
segannotate = annotation.split("\n")

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

# MAIN ### MAIN ### MAIN ### MAIN ### MAIN ### MAIN ### MAIN ### MAIN
# initialise list to store dev names and loc
devs = []
for i in range(len(segannotate) - 1):
    # split line to get code from the line
    word = segannotate[i].split("\t")
    codeline = word[3].split(")") # the line of code is actually codeline[1]
    # make sure something useful was actually committed
    if line_is_valid(codeline[1]):
        # get name from line
        name = word[1][1:]
        # deal with exception
        if len(devs) == 0:
            devs.append((name, 1))
        else:
            for j in range(len(devs)):
                # check to see if name is already on the list, if so +1
                if devs[j][0] == name:
                    loc = devs[j][1]
                    loc += 1
                    devs[j] = (name, loc)
                    break
                #if not, create a new name with a single loc
                elif j == len(devs) - 1:
                    devs.append((name, 1))
                    
# function to make sorting function usable                   
def takeSecond(elem):
    return elem[1]

# print based on loc
devs.sort(reverse=True, key=takeSecond)
rank = 1
for name, number in devs:
    print(rank, name, number)
    rank += 1