import os 

byte = 0

def mapping():
    folder = os.walk(os.getcwd())
    lenth = len(os.getcwd())
    f = open('systemlog', 'w')
    for file in folder:
        for i in range(len(file[2])):
            y = file[0] +"/" + file[2][i]
            y = y[lenth:]
            if  y[0] == "/":
                y = y[1:]
            f.write( y +"\n")
    f.close()
    
mapping()
    
    
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
            

print "File system in bytes: " +   str(byte/1024) + " Megabyte"