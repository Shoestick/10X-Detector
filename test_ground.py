import subprocess
import os
from datetime import date

# calulates how old a line is in days based on blame info
def day_difference(timestamp):
    refined = timestamp.split(" ")
    sdate = refined[0].split("-")
    syear = sdate[0]
    smonth = sdate[1]
    sday = sdate[2]
    commit_date = date(int(syear), int(smonth), int(sday))
    
    today = date.today()
    delta = today - commit_date
    
    return delta.days

# various checks to see if the code actually contributed anything
def line_is_valid(codeline):
    j = 0 # will be pos in string of first none space character
    # to see if the line contains anything
    if codeline == "":
        return False
    # to see if the line is longer than 2 none space characters
    # also to see if line has any none space characters
    else:
        for i in range(len(codeline)):
            if codeline[i] != " ":
                if i + 3 > len(codeline):
                    return False
                else:
                    j = i
                    break
            elif i + 3 > len(codeline):
                return False
    # check to see if the line is a single line comment
    if codeline[j] == "#" or (codeline[j] == "/" and codeline[j + 1] == "/"):
        return False
    # check for multiline comments
    # check to see if the line is boilerplate
    # otherwise it's good
    return True

# takes in oldest_commit and name, and return how old the oldest commit of that author is
def authors_oldest_commit(oldest_commit, name):
    for j in range(len(oldest_commit)):
        if oldest_commit[j][0] == name:
            return oldest_commit[j][1]
            
    print("[ERROR] Name not found in commit history, unkown how old their oldest commit is")
    return 0

devs =[]
oldest_commit = []
NEW_BOOST_PERIOD = 365 // 2
AGE_FACTOR = 3

# get annotate of specified file
repo_path = "C:/Users/oisin/Desktop/Forth-Year/FYP/extracted-repos/ruby"

print("[START]")

def get_code_factor(ftype):
    # ts, tsx, less, toml, sh, h, expect, cc, dat, glsl, cmake, osl, xml, kt, webp, po, gitignore
    # 1000+: xml, kt, sh, h, dat
    # 500+: po, glsl, hh
    # 250+: h, webp, json, h
    # 100+: yml, rdoc, depend, ts, tsx, build, gitignore, am, xcf, cmake, osl
    # misc: gitignore, editorconfig, gitattributes
    # h, xml, cc, dat, kt, *sh*, glsl, po, hh, webp, json
    vlow = set(['txt', 'md', 'rdoc', 'y', 'pem',  'markdown'])
    low = set(['css', 'html', 'xml', 'json', 'yml', 'depend', 'gemspec', 'src', 'm4', '1'])
    middling = set(['js', 'java', 'cs', 'rb', 'py', 'kt'])
    high = set(['c', 'cpp', 'cc', 'h', 'hh'])
    vhigh = set(['rs', 'go', 'hs', 'lhs', '.ex'])
    
    score = 0
    if(ftype in vlow):
        score = 1#0.05
    elif(ftype in low):
        score = 2
    elif(ftype in middling):
        score = 3#1
    elif(ftype in high):
        score = 4#1.3
    elif(ftype in vhigh):
        score = 5#1.6
    
    return score

zero = 0
one = 0
two = 0
three = 0
four = 0
five=0
total = 0
file_types = []
#get blame
exclude = set(['.git', '.gitlab', '.github'])
for root, dirs, files in os.walk(repo_path, topdown=True):
    dirs[:] = [d for d in dirs if d not in exclude]
    for filename in files:
        if (not filename[-4:] == '.ico' and not filename[-4:] == '.svg' and not filename[-4:] == '.png' and # image file types
            not filename[-4:] == '.jpg' and not filename[-4:] == 'jpeg' and not filename[-4:] == '.tif' and # ...
            not filename[-4:] == 'woff' and not filename[-4:] == 'off2' and not filename[-4:] == '.ttf' and # font storage file types
            not filename[-4:] == '.bin' and not filename[-3:] == '.gz' and not filename[-4:] == 'webp'):
            
            temp = filename.split('.')
            for i in range(len(temp)):
                ftype = temp[i]
                
            if len(file_types) == 0:
                file_types.append((ftype, 1))
            else:
                for i in range(len(file_types)):
                    if file_types[i][0] == ftype:
                        counter = file_types[i][1]
                        counter += 1
                        file_types[i] = ((ftype, counter))
                        break
                    elif i == len(file_types) - 1:
                        file_types.append((ftype, 1))
                        
            code_factor = get_code_factor(ftype)
            
            if code_factor == 0:
                zero += 1
            elif code_factor == 1:
                one += 1
            elif code_factor == 2:
                two += 1
            elif code_factor == 3:
                three += 1
            elif code_factor == 4:
                four += 1
            elif code_factor == 5:
                five += 1
            total += 1
         
pzero = zero / total
pone = one / total  
ptwo = two / total  
pthree = three / total  
pfour = four / total     
pfive = five / total            
print("[OUTPUT]", zero, "undocced", 100*round(pzero, 3))
print("[OUTPUT]", one, "vlow", 100*round(pone, 3))
print("[OUTPUT]", two, "low", 100*round(ptwo, 3))
print("[OUTPUT]", three, "mids", 100*round(pthree, 3))
print("[OUTPUT]", four, "high", 100*round(pfour, 3))
print("[OUTPUT]", five, "vhigh", 100*round(pfive, 3))

print("[OUTPUT]", total, "total")

def takeSecond(elem):
    return elem[1]
file_types.sort(reverse=True, key=takeSecond)
i = 0
for ftype, number in file_types:
    print("[T20]", ftype, number)
    if i > 20:
        break
    i += 1

print("[END]")