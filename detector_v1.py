#what am I currently trying to do?
#take in the blame, and count lines
    #input from blame directly rather than text file
    #allow for variable size of name (start at 10 and read up until you hit a number?)
    #detect empty lines
        #don't count them
        
#structure to store name of dev and num of lines written by them
devs = []

#open blame which has been downloaded and put into a txt file
with open('Sample Blame.txt') as f:
    line = f.readline()
    while line:
        #deal with exception
        if len(devs) == 0:
            devs.append((line[10:24], 1))
            #print("new dev", line[10:21])
        else:
            for i in range(len(devs)):
                #check to see if name is already on the list, if so +1
                if devs[i][0] == line[10:24]:
                    loc = devs[i][1]
                    loc += 1
                    devs[i] = (line[10:24], loc)
                    #print("+1 to", devs[i][0])
                    break
                #if not, create a new name with a single loc
                elif i == len(devs) - 1:
                    devs.append((line[10:24], 1))
                    #print("new dev", line[10:21])
        line = f.readline()
    
    for name, number in devs:
        print(name, number)
    