import subprocess

# get annotate of specified file
repo_path = "cd /Users/oisin/Desktop/Forth-Year/FYP/extracted-repos/mynetworks"
file_name = "Hospital_server.py"
command = repo_path + " && git annotate " + file_name
annotation = subprocess.check_output(command, shell=True).decode('utf-8')

# split paragraph string into lines
segannotate = annotation.split("\n")
# initialise list to store dev names and loc
devs = []
for i in range(len(segannotate) - 1):
    # split line to get name
    word = segannotate[i].split("\t")
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