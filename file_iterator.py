import os
 
# assign directory
directory = 'C:/Users/oisin/Desktop/Forth-Year/FYP/extracted-repos/html5-boilerplate'
 
# iterate over files in
# that directory
exclude = set(['.git'])
for root, dirs, files in os.walk(directory, topdown=True):
    dirs[:] = [d for d in dirs if d not in exclude]
    for filename in files:
        print(root[54:], "SUCCESS")