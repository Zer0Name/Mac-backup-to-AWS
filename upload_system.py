import os

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


