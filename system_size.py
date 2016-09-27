import os 

byte = 0

with open('systemlog', 'r') as file:
    for i, line in enumerate(file):
        try:
            filename = line.rstrip('\n')
        except:
            print "error"
                
        try:
            byte += float(os.stat(filename).st_size) # size is in bytes
            print filename
            print os.stat(filename).st_size
        except:
            print "could not get file size"
print byte