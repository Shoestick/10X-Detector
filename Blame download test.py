#https://bitbucket.org/kevzettler/git-blame-example.git
from git import Repo

# clone the repository
#repo = Repo.clone_from("https://bitbucket.org/kevzettler/git-blame-example.git", "C:/Users/oisin/Desktop/Forth-Year/FYP/test")

# open the repository
repo = Repo("C:/Users/oisin/Desktop/Forth-Year/FYP/extracted-repos/mynetworks")

# read the blame information for a file
file_path = "C:/Users/oisin/Desktop/Forth-Year/FYP/extracted-repos/mynetworks/Hospital_server.py"
blame = repo.blame('HEAD', file_path)

# iterate through blame information
for hunk in blame:
    print(hunk)