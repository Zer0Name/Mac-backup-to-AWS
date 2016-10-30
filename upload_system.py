import os
import pip

def imports_installs(): # install required imports 
    os.system("sudo apt-get -y install python-pip")
    try:
        os.system("sudo pip install boto")
        os.system("sudo pip install FileChunkIO")
    except Exception as e:     # most generic exception you can catch
        print e
        exit()
        
imports_installs() #install all required imports for the program

import boto #pip install boto
import math
from filechunkio import FileChunkIO   #  pip install FileChunkIO
from multiprocessing.pool import ThreadPool as Pool



aws_access_key_id = ""  # access key 
aws_secret_access_key = "" # secret key
worker = 15  #amount of simulatumallys threads uploading 
files = 0



# maps the entire computer
def mapping(files):
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
    
    with open('systemlog', 'r') as file:
        for i, line in enumerate(file):
            files = files + 1
    return files


def upload_seqence(worker,folder,bucket,files):
        
    pool_size = int(worker) # "parallelness"
    pool = Pool(pool_size)

    with open('systemlog', 'r') as file:
            
        for i, line in enumerate(file):
            try:
                filename = line.rstrip('\n')
            except:
                print "error"
            try:
                pool.apply_async(upload_file, (filename, folder, i , bucket, files))
            except:
                print "error"
                
    file.close() 
    pool.close() 
    pool.join()


# folder =  location you wish to place system backup in S3
# number = display current file number being uploaded
# bucket = aws bucket you with to uplaod too

def upload_file(file_path, folder, number, bucket, files): 

    # connect to  amazon 
    conn = boto.connect_s3(aws_access_key_id , aws_secret_access_key ) 
    
    # creates a buckets
    bucketname = conn.get_bucket(bucket,validate=False)
    # Get file info
    source_path = file_path
    source_size = os.stat(source_path).st_size
    
    filename = folder +'/'+file_path
        # Create a multipart upload request
    mp = bucketname.initiate_multipart_upload(filename)

        # Use a chunk size of 50 MiB (feel free to change this)
    chunk_size = 52428800 
    chunk_count = int(math.ceil(source_size / float(chunk_size)))

        # Send the file parts, using FileChunkIO to create a file-like object
        # that points to a certain byte range within the original file. We
        # set bytes to never exceed the original file size.
    for i in range(chunk_count):
        offset = chunk_size * i
        bytes = min(chunk_size, source_size - offset)
        part = i + 1
        print "uploading part " + str(part) + " of " + str(chunk_count)
        with FileChunkIO(source_path, 'r', offset=offset,
                    bytes=bytes) as fp:
            mp.upload_part_from_file(fp, part_num=i + 1)

    if len(mp.get_all_parts()) == chunk_count:
        mp.complete_upload()
        print str(number) + " out of:" + str(files)
    else:
        mp.cancel_upload()
        print "upload_file failed"
    

def run(worker, files, bucket, folder):
    imports_installs() # install required files
    files = mapping(files) # maps the computers 
    files = files - 1
    upload_seqence(worker,folder,bucket,files) # starts to the uplaod sequence
    
if __name__ == "__main__":
    bucket = raw_input("Enter bucket name: ")
    folder = raw_input("Folder name you wish to upload system too: ")
    run(worker, files, bucket, folder)