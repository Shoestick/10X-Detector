import os

 # get annotate of specified file
repo_path = "C:/Users/oisin/Desktop/Forth-Year/FYP/extracted-repos/html5-boilerplate"
cd_repo = "cd " + repo_path[2:54]

exclude = set(['.git'])
for root, dirs, files in os.walk(repo_path, topdown=True):
    dirs[:] = [d for d in dirs if d not in exclude]
    for filename in files:
        #print(filename, "SUCCESS")
        if not filename[-4:] == '.png' and not filename[-4:] == '.svg' and not filename[-4:] == '.ico': # add '.jpg', 'jpeg', '.tif'
            command = cd_repo + root[54:] + " && git annotate " + filename
            print(command)