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
repo_path = "C:/Users/oisin/Desktop/Forth-Year/FYP/extracted-repos/rspack"
cd_repo = "cd " + repo_path[2:]

command = cd_repo + " && git whatchanged"
whatchanged = subprocess.check_output(command, shell=True).decode('utf-8')

line = whatchanged.split("\n")
author = ""
files_pcommit = 0
files_pcommit_score = 0
highest_files_pcommit_score = 0
hfpcs = 0
hfc = 0
for i in range(500):#range(len(line) - 1):
    if line[i] != "":
        if line[i][0] == "A":
            if author != "":
                if files_pcommit_score / files_pcommit >= 0.52:
                    print("files ->", files_pcommit, "score ->",round(files_pcommit_score, 4))
                    #print("files_pcommit_score / 16 =", files_pcommit_score / 16)
                    #print("(files_pcommit_score / 16) + 1 =", (files_pcommit_score / 16) + 1)
                    #print("pow((files_pcommit_score / 16) + 1, files_pcommit) =", pow((files_pcommit_score / 16) + 1, files_pcommit))
                    #print("pow ->", round(pow(files_pcommit_score / files_pcommit + 1, files_pcommit / 8 + 1), 4))
                    final = round(pow(files_pcommit, files_pcommit_score / files_pcommit + 0.45), 4)
                    if final > 50:
                        final = 50
                    print("pow->", final)
                    print("------------")
                    
                    #final = round(pow(files_pcommit_score / files_pcommit + 1, files_pcommit / 8 + 1), 4)
                    
                    if final > highest_files_pcommit_score:
                        highest_files_pcommit_score = final
                        hfpcs = files_pcommit_score
                        hfc = files_pcommit
                    files_pcommit_score = 0
                    files_pcommit = 0
            
            author = line[i][8:line[i].find("<") - 1]
            #print(author)
        elif line[i][0] == ":":
            files_pcommit += 1
            #print(line[i])
            word = line[i].split(" ")
            temp = word[4].split('.')
            ftype = "?"
            ftype = temp[len(temp) - 1]
            #print(ftype, get_code_factor(ftype))
            files_pcommit_score += (get_code_factor(ftype) + 1) / 2
print("Highest: ", highest_files_pcommit_score)
print("code score", round(hfpcs / hfc + 0.45, 3))
print("no. files", hfc)