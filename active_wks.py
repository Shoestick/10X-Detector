# getting a total number of commits? and then total number of weeks?
# or getting a number of commits per each individual week?
# or I could get a number of commits per author per week, so they only have to beat their own metrics rather than the collective

# then something needs to be done to that to establish a baseline, as in if above half that or something

# "git log --format=pretty" to get a date of a commit
# day-diff back to the very first commit
# divide by seven to find out which week it's in
# add one to that name
# add the name to another list, list saying who already commited that week

# return the date of the oldest commit
def get_oldest_commit(cd_repo):
    command = cd_repo + " && git log --pretty=format:\"%an%x09%ad\" --date=format:\"%Y-%m-%d\""
    annotation = subprocess.check_output(command, shell=True).decode('utf-8', errors="replace")

    segannotate = annotation.split("\n")
    word = segannotate[len(segannotate) - 1].split("\t")
    sdate = word[1].split("-")
    syear = sdate[0]
    smonth = sdate[1]
    sday = sdate[2]
    commit_date = date(int(syear), int(smonth), int(sday))
    return commit_date

# difference between two given dates
def day_difference(timestamp, oldest_commit_date):
    refined = timestamp.split(" ")
    sdate = refined[0].split("-")
    syear = sdate[0]
    smonth = sdate[1]
    sday = sdate[2]
    commit_date = date(int(syear), int(smonth), int(sday))
    
    delta = commit_date - oldest_commit_date
    
    return delta.days

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

from datetime import date
import subprocess

devs = [] # list to save developers names and number of active weeks
wk_devs = [] # list to save developers names if they've commited within the week

print("[START]")
repo_path = "C:/Users/oisin/Desktop/Forth-Year/FYP/extracted-repos/rspack"
command = "cd" + repo_path[2:] + " && git log --pretty=format:\"%an%x09%ad\" --date=format:\"%Y-%m-%d\""
log = subprocess.check_output(command, shell=True).decode('utf-8', errors="replace")

oldest_commit_date = get_oldest_commit("cd" + repo_path[2:])
seglog = log.split("\n")
curr_wk_no = -1
wk_no = -1
for i in range(len(seglog) - 1):
    if i % 5 == 0:
        print("[PROCESSING] ", i + 1, "/", len(seglog) - 1)
    # process lines of log
    word = seglog[i].split("\t")
    author = word[0]
    unprocessed_date = word[1]
    
    # checking to see if it is the next week
    wk_no = day_difference(unprocessed_date, oldest_commit_date) // 7
    
    if wk_no != curr_wk_no:
        wk_devs.clear()
        curr_wk_no = wk_no
    
    # handle exception
    if len(devs) == 0:
        devs.append((author, 1))
        wk_devs.append(author)
    else:
        # check to see if the author has already been seen this week
        skip = False
        for j in range(len(wk_devs)):
            if wk_devs[j] == author:
                skip = True
                break
        if skip == False:
        # otherwise process the name
            for j in range(len(devs)):
                # check to see if name is already on the list, if so +1
                if devs[j][0] == author:
                    temp = devs[j][1]
                    temp += 1
                    
                    devs[j] = (author, temp)
                    wk_devs.append(author)
                    break
                #if not, create a new name with a single commit
                elif j == len(devs) - 1:
                    devs.append((author, 1))
                    wk_devs.append(author)
                
print_order(devs)