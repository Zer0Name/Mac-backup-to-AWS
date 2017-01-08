import os

folder = os.walk(os.getcwd())
print folder
for file in folder:
    print file[2][0]