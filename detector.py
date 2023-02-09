import subprocess

# get annotate of specified file
repo_path = "cd /Users/oisin/Desktop/Forth-Year/FYP/extracted-repos/example"
file_name = "README.md"
command = repo_path + " && git annotate " + file_name
annotation = subprocess.check_output(command, shell=True).decode('utf-8')

# split paragraph string into lines
segannotate = annotation.split("\n")

# various checks to see if the code actually contributed anything
def line_is_valid(codeline):
    # check if the line is empty
    if codeline == "":
        return False
    # check to see if the line is a comment
    # check to see if the line is boilerplate
    else:
        return True

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

for name, number in devs:
    print(name, number)