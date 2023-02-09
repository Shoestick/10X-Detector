import subprocess

# get annotate of specified file
repo_path = "cd /Users/oisin/Desktop/Forth-Year/FYP/extracted-repos/example"
file_name = "README.md"
command = repo_path + " && git annotate " + file_name
annotation = subprocess.check_output(command, shell=True).decode('utf-8')

segannotate = annotation.split("\n")

word = segannotate[10].split("(")
name = ""
i = 0
for j in segannotate:
    
    if word[1][i] == '2':
        name = word[1][0:i]
        break
    i += 1
    
print(name)