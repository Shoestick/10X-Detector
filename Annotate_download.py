import pygit2

num = pygit2.GIT_BLAME_IGNORE_WHITESPACE

#repo = pygit2.clone_repository("https://github.com/h5bp/html5-boilerplate.git", "C:/Users/oisin/Desktop/Forth-Year/FYP/extracted-repos/html5-boilerplate")

# open the repository
repo = pygit2.Repository("C:/Users/oisin/Desktop/Forth-Year/FYP/extracted-repos/example")

# read the blame information for a file
blame = repo.blame('README.md')

# list to save names and numlines 
devs =[]
for hunk in blame:
    # deal with first case
    if len(devs) == 0:
        devs.append(hunk.final_committer)
        #print("fir dev", hunk.final_committer)
    else:
        for i in range(len(devs)):
            # check to see if name is already on the list, if so add loc
            if devs[i] == hunk.final_committer:
                break
            # if not, append a new dev
            elif i == len(devs) - 1:
                devs.append(hunk.final_committer)
                #print("new dev", hunk.final_committer, i)

#print("")
for name in devs:
    print(name)
