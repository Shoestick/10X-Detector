
def line_is_valid(codeline):
    j = 0
    if codeline == "":
        return False
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
    if codeline[j] == "#" or (codeline[j] == "/" and codeline[j + 1] == "/"):
        return False
    
    return True

zero = "" #F
one = " " #F
two = "c" #F
three = "     " #F
four = " c" #F
six = "ccccc" #P
seven = "     c" #F
eight = " ccccc" #P
nine = "     ccccc" #P
ten = "#cccccccc" #F
eleven = "   #ccccc" #F
twelve = "//cccc" #F
thirteen = "       //ccccc" #F

if line_is_valid(zero):
    print("[0][WRONG] true ")
    
if line_is_valid(one):
    print("[1][WRONG] true ")
    
if line_is_valid(two):
    print("[2][WRONG] true ")
    
if line_is_valid(three):
    print("[3][WRONG] true ")
    
if line_is_valid(four):
    print("[4][WRONG] true ")
    
if line_is_valid(seven):
    print("[7][WRONG] true ")
    
if not line_is_valid(six):
    print("[6][WRONG] false")
    
if not line_is_valid(eight):
    print("[8][WRONG] false")
    
if not line_is_valid(nine):
    print("[9][WRONG] false")

if line_is_valid(ten):
    print("[10][WRONG] true ")
else:
    print("[10][RIGHT] false")
    
if line_is_valid(eleven):
    print("[11][WRONG] true ")
else:
    print("[11][RIGHT] false")
    
if line_is_valid(twelve):
    print("[12][WRONG] true ")
else:
    print("[12][RIGHT] false")
    
if line_is_valid(thirteen):
    print("[13][WRONG] true ")
else:
    print("[13][RIGHT] false")