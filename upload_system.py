import os
import boto
import math
from filechunkio import FileChunkIO   #  pip install FileChunkIO
from multiprocessing.pool import ThreadPool as Pool



aws_access_key_id = ""
aws_secret_access_key = ""

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
    
    
def upload_seqence(worker,folder,bucket):
        
             
    pool_size = int(worker) # "parallelness"
    pool = Pool(pool_size)

    with open('systemlog', 'r') as file:
            
        for i, line in enumerate(file):
            try:
                filename = line.rstrip('\n')
            except:
                print "error"
            if filename == "main_program.py" or filename == "systemlog":
                print "not uploading"
            else: 
                try:
                    pool.apply_async(upload_file, (filename, folder, i , bucket))
                except:
                    print "error"
    file.close() 
    pool.close() 
    pool.join()


# folder =  location you wish to place system backup in S3
# number = display current file number being uploaded
# bucket = aws bucket you with to uplaod too

def upload_file(file_path, folder,number, bucket): 

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
        print number
        print "upload_file done"
    else:
        mp.cancel_upload()
        print "upload_file failed"
    

