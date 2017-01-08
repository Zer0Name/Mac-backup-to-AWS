import os
from socket import error as socket_error
# install and update all packages

f = open('tmp/info', 'w')
f.write("Starting install and update")

try:
    os.system("sudo apt-get update")                # update server 
    os.system("sudo apt-get -y install python-pip") # install pip 
    os.system("sudo pip install boto")              # intall boto
    os.system("sudo pip install Django==1.9.6")     # install Django
    os.system("sudo pip install FileChunkIO")       # install FileChunkIO
    os.system("sudo apt-get install -y htop")       # install htop 
except Exception as e:     # most generic exception you can catch
    f.write(str(e))
    exit()
    

f.write("all packages installed and updated")

import pip
import zipfile
import math
from multiprocessing.pool import ThreadPool as Pool
from filechunkio import FileChunkIO
from django.utils.encoding import smart_str, smart_unicode

LOCAL_PATH = 'tmp/' #file in the server which the program will download too.

aws_access_key_id = " """+aws_access_key_id+""" "                                   """  #get rid of this
aws_access_key_id = aws_access_key_id.strip()


aws_secret_access_key = " """+aws_secret_access_key+""" "                           """ #get rid of this
aws_secret_access_key = aws_secret_access_key.strip()

bucket_name = " """+bucket_name+""" "                                               """ #get rid of this
bucket_name = bucket_name.strip()


# connect to the bucket
conn = boto.connect_s3(aws_access_key_id, aws_secret_access_key)

bucket = conn.get_bucket(bucket_name)


folder =" """ +folder+ """ "                                                        """ #get rid of this
folder = folder.strip()


bucket_list = bucket.list(prefix=folder)
m = 0 # keep count of how many files 

for l in bucket_list:
    m = m + 1
    print m
    keyString = smart_str(l.key) 
    path = LOCAL_PATH + keyString
    try:
        l.get_contents_to_filename(path)
    except socket_error:
        import time
        time.sleep(10)
        l.get_contents_to_filename(path)
    except OSError:
        if not os.path.exists(path):
            print os.path.basename(path)
            x = os.path.basename(path)
            z = path
            y = z.replace(x,"")
            os.makedirs(y)
            # check if dir exist
        try:
            l.get_contents_to_filename(path)
        except socket_error:
            import time
            time.sleep(10)
            l.get_contents_to_filename(path)
        except OSError:
            print "error"
            print path
            print "error"  
        except Exception:
            import time
            time.sleep(10)
            l.get_contents_to_filename(path)
    except Exception:
        import time
        time.sleep(10)
        l.get_contents_to_filename(path)




f.write("finished downloading all files from S3 bucket")

f.write("starting zipping proccess")



def zipper(dir, zip_file):
    x = 0
    zip = zipfile.ZipFile(zip_file, 'w', compression=zipfile.ZIP_DEFLATED, allowZip64=True)
    root_len = len(os.path.abspath(dir))
    for root, dirs, files in os.walk(dir):
        archive_root = os.path.abspath(root)[root_len:]
        for f in files:
            fullpath = os.path.join(root, f)
            archive_name = os.path.join(archive_root, f)
            print f
            zip.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
            x = x + 1
            print x
    zip.close()
    return zip_file
zipper('tmp/' + folder, 'tmp/'+folder+'.zip')

f.write("finished zipping files")



f.write("checking to see if zip file is completed")

zip_file = 'tmp/' + folder + '.zip'
the_zip_file = zipfile.ZipFile(zip_file, 'r', compression=zipfile.ZIP_DEFLATED, allowZip64=True)
ret = the_zip_file.testzip()

f.write(str(ret))


f.write("done checking zipfile")


f.write("Starting upload price")



f.write("starting upload file")
file_path = "tmp/" + folder + ".zip"


# Get file info
source_path = file_path
source_size = os.stat(source_path).st_size
        

# Create a multipart upload request
mp = bucket.initiate_multipart_upload("zipbackup/" + folder + ".zip")

# Use a chunk size of 50 MiB (feel free to change this)
chunk_size = 5242880
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
    print "upload_file done"
else:
    mp.cancel_upload()
    print "upload_file failed"